# CARE LOOP V3 — Architecture Notes

## Active application path

1. `run.py` imports and launches `gui.launch()`.
2. `gui/main_window.py` builds the Tkinter application and creates `app.DetectionSession`.
3. `app/session.py` owns capture, the worker thread, the output writer, and optional `backend.publisher.EventPublisher`.
4. `fall_detection_all_in_one.py` performs YOLO pose inference, tracking, kinematic feature extraction, occlusion processing, state transitions, and HUD rendering.
5. The session publishes one event on entry to an active fall episode. If the same track later reaches `CONFIRMED_FALL`, the publisher escalates that same event to P0 instead of creating a duplicate. The publisher uses a bounded in-memory queue and HTTP POST to `/api/v1/events` and `/api/v1/events/{event_id}/escalate`.
6. `backend/main.py` validates API input and delegates persistence to `backend/database.py`.
7. `backend/static/index.html` reads event data and submits caregiver lifecycle actions.

## Module responsibilities

| Module | Responsibility | Active? |
|---|---|---|
| `gui/main_window.py` | Desktop GUI | Yes |
| `gui/bridge.py` | Worker-to-Tkinter thread-safe event bridge | Yes |
| `app/services.py` | Input selection, model choices, session config | Yes |
| `app/session.py` | Capture loop, inference orchestration, publisher lifecycle | Yes |
| `fall_detection_all_in_one.py` | Active YOLO + tracking + kinematics + occlusion + state machine | Yes |
| `backend/publisher.py` | Async best-effort event delivery | Yes, when `CARE_LOOP_API_URL` is set |
| `backend/main.py` | FastAPI routes and shared-key guard | Yes |
| `backend/database.py` | SQLite events and audit history | Yes |
| `backend/static/index.html` | Caregiver dashboard | Yes |
| `core/*.py`, root `main.py` | Earlier modular inference version | No, not used by `run.py` |

## Fall-state logic

`MONITORING -> RAPID_DESCENT -> FALL_DETECTED -> CONFIRMED_FALL`, with recovery back to `MONITORING`. The state machine uses normalized vertical velocity, torso angular velocity, head/body displacement, torso orientation, bounding-box shape, hip displacement, and visibility context.

Occlusion imputation is for rendering/statistics; the kinematics extractor reads observed raw keypoints. A newly added guard prevents a track that simply disappears inside a furniture zone from being declared fallen unless the last observed pose already met the state machine's down-posture evidence check.

## Event lifecycle

`NEW -> ACKNOWLEDGED -> RESOLVED` or `NEW/ACKNOWLEDGED -> FALSE_ALARM`. An open event may also receive a system escalation to P0; the escalation is written to the audit log. Actions are recorded in `audit_logs`. The current backend is a local single-node prototype; it does not provide caregiver identities, role permissions, device enrollment, or a durable delivery queue.
