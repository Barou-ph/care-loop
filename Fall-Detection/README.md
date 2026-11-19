# CARE LOOP V3 — AI Fall Detection & Caregiver Alert Prototype

CARE LOOP is a local prototype that combines camera/video-based human pose estimation, fall-event screening, a caregiver event API, and a browser dashboard. It is **not a medical device** and does not automatically contact emergency services.

## 1. Actual runtime architecture

```text
Webcam / Video / Synthetic Demo
              |
              v
       Tkinter Desktop GUI
              |
              v
     app.DetectionSession
              |
              v
 fall_detection_all_in_one.FallDetectionPipeline
   |          |          |          |
 YOLO Pose  Tracker  Kinematics  Occlusion
              |
              v
       Fall State Machine
              |
              v
         EventPublisher
        (HTTP, background queue)
              |
              v
      FastAPI backend API
              |
              v
       SQLite EventStore
              |
              v
     Caregiver HTML Dashboard
```

**Important source-of-truth note:** the desktop GUI imports `app/` and the active fall-detection implementation in `fall_detection_all_in_one.py`. The root `main.py` and `core/` directory contain an older modular implementation; `run.py` does not use that implementation. They are retained for reference and should not be mistaken for a second active inference path.

## 2. Features present

- Webcam, video-file, and synthetic-demo input.
- YOLO pose detection with 17 COCO keypoints.
- Multi-person track lifecycle (tentative / confirmed), normalized motion features, torso angle, and temporal fall state machine.
- Keypoint occlusion estimation for visualization and furniture-zone handling.
- Annotated output video and desktop alert log.
- Optional asynchronous event publishing to a local FastAPI service.
- SQLite event storage and audit history.
- Caregiver actions: Acknowledge, Resolve, False alarm, and Audit; confirmed falls escalate the same open event to P0.
- Dashboard refreshes events automatically every five seconds while the page is visible.

## 3. Requirements and installation

- Python 3.10+ recommended.
- Windows 10/11 for the supplied `.bat` / PowerShell launchers.
- A webcam is optional; video files and the synthetic demo can be used instead.
- The bundled pose weights are `yolo11s-pose.pt` and `yolov8n-pose.pt`. The GUI defaults to YOLO11s and falls back to the bundled YOLOv8n model if the preferred weights cannot be loaded. Actual model loading requires the Ultralytics runtime and compatible PyTorch dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Run on Windows

### One-command local startup

```powershell
.\start_care_loop.bat
```

The launcher checks the local API at `127.0.0.1:8000`, starts it if needed, opens the caregiver dashboard, and then starts the desktop GUI.

### Manual startup

Terminal 1 — API:

```powershell
$env:CARE_LOOP_API_URL = "http://127.0.0.1:8000"
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Terminal 2 — desktop detector:

```powershell
$env:CARE_LOOP_API_URL = "http://127.0.0.1:8000"
python run.py
```

Optional shared API key (set the same value in both processes):

```powershell
$env:CARE_LOOP_API_KEY = "replace-with-a-long-random-secret"
```

The API key is a development shared secret, not user-level authentication. Keep the API bound to loopback. Do not expose this prototype to the public internet.

## 5. Useful API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/` | Caregiver dashboard |
| POST | `/api/v1/events` | Create an event |
| GET | `/api/v1/events` | List events |
| GET | `/api/v1/events/{event_id}` | Event detail |
| POST | `/api/v1/events/{event_id}/acknowledge` | Acknowledge |
| POST | `/api/v1/events/{event_id}/resolve` | Resolve |
| POST | `/api/v1/events/{event_id}/false-alarm` | Mark false alarm |\n| POST | `/api/v1/events/{event_id}/escalate` | Escalate an open event to P0 confirmed-fall priority |
| GET | `/api/v1/events/{event_id}/audit` | Audit history |

Interactive API docs: `http://127.0.0.1:8000/docs`.

## 6. Tests

Run from the repository root:

```powershell
python -m pytest -q
```

The test suite covers SQLite event lifecycle, API routes and API-key guard, publisher episode de-duplication, and synthetic state-machine cases including bending, sitting, forward/side falls, and loss of visibility behind furniture.

## 7. Known limitations

- Real YOLO inference, camera access, and end-to-end video-to-dashboard delivery must be verified on the target Windows machine with the installed Ultralytics runtime and an actual camera/video.
- The current publisher is best-effort. Failed HTTP delivery is logged; there is no durable outbox, guaranteed retry, or delivery acknowledgement to the detector.
- The backend uses SQLite for a single local process. There is no production migration system, multi-user account system, household/role authorization, consent flow, or device provisioning workflow.
- The dashboard is a lightweight HTML/JavaScript console, not a production React application. It does not include care profiles or care plans.
- AI-generated fall alerts are suspicions, not diagnoses. Caregivers must verify the situation. No SMS, push, phone call, or emergency-service dispatch is integrated.
- A single 2D camera cannot reliably distinguish every fall from intentional lying down, a fall onto a bed, push-ups, or other similar movement.

## 8. Project layout

```text
CARE_LOOP_V3/
├── app/                       # Active session and source configuration
├── backend/                   # FastAPI, SQLite store, publisher, static dashboard
│   └── static/index.html
├── core/                      # Earlier modular inference implementation (not active in GUI)
├── gui/                       # Tkinter GUI and thread-safe event bridge
├── tests/                     # Unit and API tests
├── fall_detection_all_in_one.py
├── main.py                    # Earlier modular pipeline entry point
├── run.py
├── start_care_loop.bat
├── start_care_loop.ps1
├── requirements.txt
└── docs/
    ├── ARCHITECTURE.md
    ├── IMPLEMENTATION_STATUS.md
    └── TEST_REPORT.md
```

See `docs/IMPLEMENTATION_STATUS.md`, `docs/TEST_REPORT.md`, and `SECURITY.md` before relying on this prototype.
