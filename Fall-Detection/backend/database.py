"""Small SQLite persistence layer for the CARE LOOP MVP.

SQLite is suitable for a single-node prototype. Use a managed database and
migration tooling before multi-instance/production deployment.
"""
from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional

DEFAULT_DB = Path(os.getenv("CARE_LOOP_DB_PATH", "data/care_loop.db"))


class EventStore:
    def __init__(self, db_path: str | Path = DEFAULT_DB):
        self.db_path = Path(db_path)
        if str(self.db_path) != ":memory:":
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @contextmanager
    def _connection(self):
        conn = self._connect()
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _initialize(self) -> None:
        with self._connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    household_id TEXT,
                    device_id TEXT,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL CHECK(severity IN ('P0','P1','P2')),
                    status TEXT NOT NULL CHECK(status IN ('NEW','ACKNOWLEDGED','RESOLVED','FALSE_ALARM')),
                    source TEXT NOT NULL DEFAULT 'api',
                    track_id INTEGER,
                    confidence REAL CHECK(confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
                    occurred_at TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    acknowledged_at TEXT,
                    acknowledged_by TEXT,
                    resolved_at TEXT,
                    resolved_by TEXT,
                    resolution_note TEXT,
                    metadata_json TEXT NOT NULL DEFAULT '{}'
                );
                CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_events_status ON events(status, severity);
                CREATE TABLE IF NOT EXISTS audit_logs (
                    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
                    action TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    details_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_audit_event ON audit_logs(event_id, audit_id);
                CREATE TABLE IF NOT EXISTS devices (
                    device_id TEXT PRIMARY KEY,
                    household_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    device_type TEXT NOT NULL DEFAULT 'camera',
                    status TEXT NOT NULL DEFAULT 'unknown',
                    last_seen_at TEXT,
                    created_at TEXT NOT NULL
                );
                """
            )

    @staticmethod
    def _event(row: sqlite3.Row) -> dict[str, Any]:
        item = dict(row)
        item["metadata"] = json.loads(item.pop("metadata_json") or "{}")
        return item

    def create_event(self, event: dict[str, Any]) -> dict[str, Any]:
        with self._connection() as conn:
            conn.execute(
                """INSERT INTO events (
                    event_id, household_id, device_id, event_type, severity, status,
                    source, track_id, confidence, occurred_at, created_at, metadata_json
                ) VALUES (?, ?, ?, ?, ?, 'NEW', ?, ?, ?, ?, ?, ?)""",
                (event["event_id"], event.get("household_id"), event.get("device_id"),
                 event["event_type"], event["severity"], event.get("source", "api"),
                 event.get("track_id"), event.get("confidence"), event["occurred_at"],
                 event["created_at"], json.dumps(event.get("metadata", {}), ensure_ascii=False)),
            )
            self._audit(conn, event["event_id"], "CREATED", event.get("actor", "system"),
                        {"status": "NEW", "severity": event["severity"]}, event["created_at"])
            row = conn.execute("SELECT * FROM events WHERE event_id = ?", (event["event_id"],)).fetchone()
            return self._event(row)

    def get_event(self, event_id: str) -> Optional[dict[str, Any]]:
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM events WHERE event_id = ?", (event_id,)).fetchone()
            return self._event(row) if row else None

    def list_events(self, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        sql, args = "SELECT * FROM events", []
        if status:
            sql += " WHERE status = ?"
            args.append(status)
        sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        args.extend([limit, offset])
        with self._connection() as conn:
            return [self._event(row) for row in conn.execute(sql, args).fetchall()]

    def transition_event(self, event_id: str, target: str, actor: str, note: Optional[str], now: str) -> Optional[dict[str, Any]]:
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM events WHERE event_id = ?", (event_id,)).fetchone()
            if row is None:
                return None
            current = row["status"]
            allowed = {
                "ACKNOWLEDGED": {"NEW", "ACKNOWLEDGED"},
                "RESOLVED": {"ACKNOWLEDGED", "NEW"},
                "FALSE_ALARM": {"NEW", "ACKNOWLEDGED"},
            }
            if current not in allowed[target]:
                raise ValueError(f"Cannot transition event from {current} to {target}")
            if target == "ACKNOWLEDGED":
                conn.execute("UPDATE events SET status=?, acknowledged_at=?, acknowledged_by=? WHERE event_id=?",
                             (target, now, actor, event_id))
            else:
                conn.execute("UPDATE events SET status=?, resolved_at=?, resolved_by=?, resolution_note=? WHERE event_id=?",
                             (target, now, actor, note, event_id))
            self._audit(conn, event_id, target, actor, {"from": current, "note": note}, now)
            updated = conn.execute("SELECT * FROM events WHERE event_id=?", (event_id,)).fetchone()
            return self._event(updated)

    def escalate_event(self, event_id: str, now: str, actor: str = "system") -> Optional[dict[str, Any]]:
        """Escalate an active suspected fall to a confirmed-fall priority."""
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM events WHERE event_id = ?", (event_id,)).fetchone()
            if row is None:
                return None
            if row["status"] not in {"NEW", "ACKNOWLEDGED"}:
                raise ValueError(f"Cannot escalate an event in status {row['status']}")
            metadata = json.loads(row["metadata_json"] or "{}")
            previous_severity = row["severity"]
            metadata["detector_state"] = "CONFIRMED_FALL"
            conn.execute(
                "UPDATE events SET event_type=?, severity='P0', metadata_json=? WHERE event_id=?",
                ("FALL_CONFIRMED", json.dumps(metadata, ensure_ascii=False), event_id),
            )
            self._audit(
                conn, event_id, "ESCALATED", actor,
                {"from_severity": previous_severity, "to_severity": "P0",
                 "event_type": "FALL_CONFIRMED"}, now,
            )
            updated = conn.execute("SELECT * FROM events WHERE event_id=?", (event_id,)).fetchone()
            return self._event(updated)

    def list_audit(self, event_id: str) -> list[dict[str, Any]]:
        with self._connection() as conn:
            rows = conn.execute("SELECT * FROM audit_logs WHERE event_id=? ORDER BY audit_id", (event_id,)).fetchall()
            result = []
            for row in rows:
                item = dict(row)
                item["details"] = json.loads(item.pop("details_json") or "{}")
                result.append(item)
            return result

    @staticmethod
    def _audit(conn: sqlite3.Connection, event_id: str, action: str, actor: str,
               details: dict[str, Any], created_at: str) -> None:
        conn.execute("INSERT INTO audit_logs(event_id, action, actor, details_json, created_at) VALUES(?,?,?,?,?)",
                     (event_id, action, actor, json.dumps(details, ensure_ascii=False), created_at))
