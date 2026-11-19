"""CARE LOOP MVP API. Run with: uvicorn backend.main:app --host 127.0.0.1 --port 8000"""
from __future__ import annotations

import os
import secrets
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.database import EventStore, DEFAULT_DB
from backend.schemas import EventAction, EventCreate

store = EventStore(DEFAULT_DB)
app = FastAPI(title="CARE LOOP API", version="0.1.0", description="MVP event intake and caregiver acknowledgement API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require_api_key(authorization: Optional[str] = Header(default=None)) -> None:
    """Optional shared-key guard. Set CARE_LOOP_API_KEY outside local development."""
    configured = os.getenv("CARE_LOOP_API_KEY")
    if not configured:
        return  # local development only; production must configure a key and TLS
    scheme, _, supplied = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not secrets.compare_digest(supplied, configured):
        raise HTTPException(status_code=401, detail="Missing or invalid bearer token")


@app.get("/", include_in_schema=False)
def caregiver_dashboard():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "care-loop-api", "mode": "development" if not os.getenv("CARE_LOOP_API_KEY") else "api-key"}


@app.post("/api/v1/events", status_code=201, dependencies=[Depends(require_api_key)])
def create_event(payload: EventCreate):
    now = utc_now()
    data = payload.model_dump()
    data.update(event_id=str(uuid.uuid4()), occurred_at=data.get("occurred_at") or now, created_at=now)
    try:
        return store.create_event(data)
    except Exception as exc:
        raise HTTPException(status_code=409, detail="Could not persist event") from exc


@app.get("/api/v1/events", dependencies=[Depends(require_api_key)])
def list_events(status: Optional[str] = Query(default=None), limit: int = Query(default=50, ge=1, le=200), offset: int = Query(default=0, ge=0)):
    if status and status not in {"NEW", "ACKNOWLEDGED", "RESOLVED", "FALSE_ALARM"}:
        raise HTTPException(status_code=422, detail="Unsupported event status")
    return {"items": store.list_events(status, limit, offset), "limit": limit, "offset": offset}


@app.get("/api/v1/events/{event_id}", dependencies=[Depends(require_api_key)])
def get_event(event_id: str):
    event = store.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/api/v1/events/{event_id}/acknowledge", dependencies=[Depends(require_api_key)])
def acknowledge_event(event_id: str, payload: EventAction):
    try:
        event = store.transition_event(event_id, "ACKNOWLEDGED", payload.actor, payload.note, utc_now())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/api/v1/events/{event_id}/resolve", dependencies=[Depends(require_api_key)])
def resolve_event(event_id: str, payload: EventAction):
    try:
        event = store.transition_event(event_id, "RESOLVED", payload.actor, payload.note, utc_now())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/api/v1/events/{event_id}/false-alarm", dependencies=[Depends(require_api_key)])
def mark_false_alarm(event_id: str, payload: EventAction):
    try:
        event = store.transition_event(event_id, "FALSE_ALARM", payload.actor, payload.note, utc_now())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/api/v1/events/{event_id}/escalate", dependencies=[Depends(require_api_key)])
def escalate_event(event_id: str):
    try:
        event = store.escalate_event(event_id, utc_now(), "system")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.get("/api/v1/events/{event_id}/audit", dependencies=[Depends(require_api_key)])
def event_audit(event_id: str):
    if store.get_event(event_id) is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"items": store.list_audit(event_id)}
