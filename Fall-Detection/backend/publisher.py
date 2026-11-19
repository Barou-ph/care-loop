"""Non-blocking HTTP publisher from the local detector to the CARE LOOP API."""
from __future__ import annotations

import json
import logging
import os
import queue
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

log = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 3.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._queue: queue.Queue[dict[str, Any] | None] = queue.Queue(maxsize=100)
        self._active_events: dict[int, str] = {}
        self._closed = False
        self._thread = threading.Thread(target=self._run, name="CareLoopEventPublisher", daemon=True)
        self._thread.start()

    @classmethod
    def from_env(cls):
        url = os.getenv("CARE_LOOP_API_URL", "").strip()
        if not url:
            return None
        return cls(url, os.getenv("CARE_LOOP_API_KEY"))

    def publish_detection_alert(self, alert: dict[str, Any]) -> bool:
        state = str(alert.get("state", "FALL_DETECTED"))
        confirmed = state == "CONFIRMED_FALL"
        features = alert.get("features") or {}
        payload = {
            "_action": "create",
            "event_type": "FALL_CONFIRMED" if confirmed else "FALL_SUSPECTED",
            "severity": "P0" if confirmed else "P1",
            "source": "yolo_pose_edge",
            "track_id": int(alert.get("track_id", 0)),
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "detector_state": state,
                "torso_angle": features.get("torso_angle"),
                "note": "AI-generated suspicion; caregiver verification required. Not a medical diagnosis.",
            },
        }
        return self._enqueue(payload)

    def publish_escalation(self, alert: dict[str, Any]) -> bool:
        return self._enqueue({
            "_action": "escalate",
            "track_id": int(alert.get("track_id", 0)),
        })

    def _enqueue(self, job: dict[str, Any]) -> bool:
        if self._closed:
            return False
        try:
            self._queue.put_nowait(job)
            return True
        except queue.Full:
            log.warning("CARE LOOP event queue full; alert was not published")
            return False

    def close(self, timeout: float = 1.0):
        if self._closed:
            return
        self._closed = True
        try:
            self._queue.put(None, timeout=max(timeout, 0.1))
        except queue.Full:
            log.warning("CARE LOOP publisher could not enqueue shutdown marker before timeout")
            return
        self._thread.join(timeout=max(timeout, 0.1))

    def _request(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(
            self.base_url + path, data=body, headers=headers, method="POST"
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            raw = response.read()
            return json.loads(raw.decode("utf-8")) if raw else {}

    def _run(self):
        while True:
            job = self._queue.get()
            if job is None:
                return
            action = job.get("_action")
            track_id = int(job.get("track_id", 0))
            try:
                if action == "create":
                    payload = {key: value for key, value in job.items() if not key.startswith("_")}
                    result = self._request("/api/v1/events", payload)
                    event_id = result.get("event_id")
                    if event_id:
                        self._active_events[track_id] = event_id
                elif action == "escalate":
                    event_id = self._active_events.get(track_id)
                    if not event_id:
                        log.warning("Cannot escalate track %s: no published event ID is available", track_id)
                        continue
                    self._request(f"/api/v1/events/{event_id}/escalate", {})
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                log.warning("Could not publish CARE LOOP event (%s): %s", action, exc)
