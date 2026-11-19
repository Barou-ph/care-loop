# CARE LOOP — INTEGRATION DESIGN

**Version:** 1.0  
**Date:** 19 November 2026  
**Scope:** Fall Detection, IoT Devices, Event Publisher, Backend and Dashboard

---

## 1. Integration Objectives

CARE LOOP uses a modular integration architecture to connect different event sources to a common event management platform.

The main objectives are:

- Integrate the existing Fall Detection prototype.
- Support future SOS and IoT devices.
- Standardize event payloads.
- Separate AI inference from event coordination.
- Prevent duplicate events.
- Support failure handling.
- Keep hardware and AI models replaceable.

---

## 2. Integration Architecture

```text
+----------------------------+
|       INPUT SOURCES        |
|                            |
| Webcam / Video / SOS / IoT |
+----------------------------+
              |
              v
+----------------------------+
|     FALL DETECTION /       |
|       DEVICE ADAPTER       |
|                            |
| YOLO Pose                  |
| Person Tracking            |
| Kinematic Analysis         |
| Fall State Machine         |
+----------------------------+
              |
              v
+----------------------------+
|       EVENT PUBLISHER      |
|                            |
| Event Mapping              |
| Metadata Validation        |
| Source Event ID            |
| HTTP Delivery              |
+----------------------------+
              |
              v
+----------------------------+
|        FASTAPI BACKEND     |
|                            |
| POST /api/v1/events        |
| Validation                 |
| Authentication             |
+----------------------------+
              |
              v
+----------------------------+
|       EVENT ENGINE         |
|                            |
| Classification             |
| Lifecycle                  |
| Escalation                 |
+----------------------------+
              |
              v
+----------------------------+
|       SQLITE DATABASE      |
|                            |
| Events                     |
| Audit Logs                 |
+----------------------------+
              |
              v
+----------------------------+
|     CAREGIVER DASHBOARD    |
|                            |
| Event Queue                |
| Acknowledge                |
| Resolve                    |
| False Alarm                |
+----------------------------+
```

---

## 3. Fall Detection Integration

### 3.1. Existing Prototype

The current Fall Detection repository contains:

- YOLO Pose inference.
- Multi-person tracking.
- Kinematic feature analysis.
- Fall state machine.
- Occlusion handling.
- Desktop GUI.
- Event Publisher.
- Backend integration.

The existing detection pipeline should remain independent of household and caregiver management logic.

### 3.2. Event Generation

The AI module should generate an event when the configured detection state qualifies for publishing.

Example event:

```json
{
  "event_type": "SUSPECTED_FALL",
  "source": "AI",
  "priority": "P1",
  "device_id": "camera_001",
  "source_event_id": "session_001-person_007-fall_001",
  "metadata": {
    "session_id": "session_001",
    "person_track_id": 7,
    "detection_state": "FALL_DETECTED",
    "confidence_band": "HIGH",
    "torso_angle": 86.5
  }
}
```

The payload is illustrative. Actual fields must match the existing Event Publisher and backend schemas.

### 3.3. Identity Separation

The system must distinguish:

- `profile_id`: CARE LOOP elderly user.
- `device_id`: Physical camera or sensor.
- `session_id`: Detection session.
- `person_track_id`: Temporary tracking identity.
- `event_id`: Backend event identity.

A tracking ID is not a permanent person identifier.

Tracking IDs may change between videos or detection sessions.

The integration layer must never automatically map `person_track_id = 7` to the same elderly person across unrelated video files.

A profile association must come from an explicitly configured device-to-household mapping or an authorized operator workflow.

---

## 4. IoT Device Integration

### 4.1. Device Adapter

Each hardware provider should be integrated through a device adapter.

Responsibilities:

- Receive hardware data.
- Validate device identity.
- Normalize incoming signals.
- Convert device-specific messages into CARE LOOP event format.
- Report connectivity information.

### 4.2. Example Device Event

```json
{
  "event_type": "SOS",
  "source": "DEVICE",
  "device_id": "sos_001",
  "priority": "P0",
  "metadata": {
    "button_state": "PRESSED",
    "battery_level": 85
  }
}
```

### 4.3. Device Heartbeat

A future device integration should periodically report:

- Device identifier.
- Timestamp.
- Connection status.
- Battery level where supported.
- Firmware version where supported.

A missed heartbeat should be treated as a device health issue, not evidence that the elderly person is safe.

---

## 5. Backend Integration

The current development interface uses HTTP.

Example:

```http
POST http://127.0.0.1:8000/api/v1/events
Content-Type: application/json
```

Integration requirements:

1. Validate payload before submission.
2. Authenticate the source where configured.
3. Generate an idempotency key.
4. Submit the event.
5. Check HTTP response.
6. Record delivery result.
7. Retry only according to a bounded policy when implemented.

The AI desktop application should not directly write to the backend database.

---

## 6. Event Publisher Reliability

The Event Publisher should support the following capabilities.

| Capability            | Purpose                                     |
| --------------------- | ------------------------------------------- |
| Event mapping         | Convert AI alerts to CARE LOOP events       |
| Unique source ID      | Prevent duplicate events                    |
| Non-blocking delivery | Avoid freezing video inference              |
| Error logging         | Record failed requests                      |
| Retry                 | Handle temporary API failure                |
| Queue                 | Preserve events during temporary outages    |
| Delivery tracking     | Distinguish accepted and failed submissions |

Current implementation notes:

- The repository has a non-blocking publisher.
- Failed HTTP delivery is logged.
- Guaranteed delivery and persistent retry are not established.
- The current publisher sends local API event metadata.
- These limitations must remain explicit until the relevant mechanisms are implemented and tested.

---

## 7. Dashboard Integration

The dashboard consumes event information from the backend.

Expected flow:

```text
Backend Event Created
         |
         v
Dashboard Requests Event List
         |
         v
Display New Event
         |
         v
Caregiver Opens Event
         |
         v
Acknowledge
         |
         v
Backend Updates Status
         |
         v
Dashboard Refreshes
         |
         v
Resolve / False Alarm
```

Current dashboard:

- Browser-based lightweight console.
- Event retrieval.
- Event acknowledgement.
- Event resolution.
- False alarm action.

Future improvements:

- Real-time WebSocket updates.
- Profile information.
- Contact tree.
- Device status.
- Escalation history.
- Role-aware views.

---

## 8. Failure Handling

| Failure                  | Expected Handling                                      |
| ------------------------ | ------------------------------------------------------ |
| YOLO model unavailable   | Report AI service failure                              |
| Video source unavailable | Stop inference and report source issue                 |
| No person detected       | Do not create a fall event without qualifying evidence |
| Tracker ID reset         | Create a new session-specific tracking context         |
| Backend unavailable      | Log failed delivery; retry/queue when implemented      |
| Invalid event payload    | Reject and record validation error                     |
| Duplicate event          | Identify using idempotency                             |
| Dashboard unavailable    | Preserve event in backend                              |
| Device disconnected      | Record device health issue                             |

---

## 9. Integration Testing

Minimum integration tests:

1. Generate a synthetic fall event.
2. Convert the alert to an API payload.
3. Submit the payload.
4. Verify backend acceptance.
5. Verify database persistence.
6. Verify dashboard display.
7. Acknowledge the event.
8. Resolve the event.
9. Verify audit history.
10. Simulate backend failure.
11. Simulate repeated event delivery.
12. Test different video sessions with reused tracking IDs.

---

## 10. Integration Acceptance Criteria

- AI can publish a structured event.
- Backend receives valid events.
- Invalid payloads are rejected.
- Events are persisted.
- Dashboard displays the corresponding event.
- Acknowledgement and resolution work.
- Duplicate submission behavior is tested.
- Tracking IDs are not mistaken for user identities.
- Failure conditions are recorded.
- No unsupported delivery guarantees are claimed.

**Integration principle: AI modules detect and report signals; CARE LOOP manages the incident and coordinates the human response.**
