# CARE LOOP — SYSTEM ARCHITECTURE

**Version:** 1.0  
**Date:** 19 November 2026  
**Architecture Type:** Modular Home Safety & Care Coordination Platform

---

## 1. Architecture Overview

CARE LOOP is designed as a modular platform that connects home safety signals with a coordinated human response workflow.

The architecture separates sensing, event processing, communication, user interaction, and external service coordination.

The system follows this logical flow:

```text
ELDERLY PERSON / HOUSEHOLD
          |
          v
+-------------------------+
|      INPUT LAYER        |
|                         |
| SOS / App / IoT / AI    |
| Sensor / Device Events  |
+-------------------------+
          |
          v
+-------------------------+
|    EDGE PROCESSING      |
|                         |
| Fall Detection          |
| Sensor Filtering        |
| Local Event Generation  |
+-------------------------+
          |
          v
+-------------------------+
|       API LAYER         |
|                         |
| FastAPI                 |
| Authentication          |
| Event Validation        |
+-------------------------+
          |
          v
+-------------------------+
|    APPLICATION LAYER    |
|                         |
| Event Engine            |
| Contact Management      |
| Escalation Rules        |
| Care Coordination       |
+-------------------------+
          |
          v
+-------------------------+
|      DATA LAYER         |
|                         |
| SQLite / Future DB      |
| Events                  |
| Audit Logs              |
| Care Profiles           |
| Device Records          |
+-------------------------+
          |
          v
+-------------------------+
|   PRESENTATION LAYER    |
|                         |
| Caregiver Dashboard     |
| Family Interface        |
| Coordinator Console     |
+-------------------------+
          |
          v
+-------------------------+
|   RESPONSE ECOSYSTEM    |
|                         |
| Family / Caregiver      |
| Community Support       |
| External Providers      |
+-------------------------+
```

---

## 2. Architecture Principles

### 2.1. Modular Design

Each major capability should be implemented as a separate module.

Examples:

- Event Management.
- Care Profile Management.
- Device Management.
- Notification Management.
- Audit Logging.
- Fall Detection Integration.

A change in the camera model should not require rewriting the event management system.

### 2.2. Event-Driven Communication

CARE LOOP uses events to communicate safety-related information between components.

An event contains:

- Unique identifier.
- Event type.
- Source.
- Timestamp.
- Related user or household.
- Priority.
- Processing status.
- Relevant metadata.

The platform should distinguish event generation from event notification and human acknowledgement.

### 2.3. Human-in-the-Loop

AI-generated alerts are signals for human verification.

The platform must not treat an AI prediction as a confirmed medical condition.

### 2.4. Privacy by Design

- Collect only necessary data.
- Avoid continuous video transmission.
- Prefer local edge processing.
- Separate consent for different data purposes.
- Restrict access based on authorization.

### 2.5. Hardware Independence

The platform should support multiple device manufacturers through adapters.

A camera, SOS button, or radar device should communicate with the same logical event interface.

---

## 3. Logical System Layers

### Layer 1 — Input and Sensing

Responsibilities:

- Receive SOS signals.
- Receive device events.
- Collect sensor metadata.
- Detect device connectivity changes.
- Generate simulated events during development.

Supported or planned sources:

| Source               | Role                     | Stage  |
| -------------------- | ------------------------ | ------ |
| SOS button           | Manual emergency signal  | MVP    |
| Application          | Manual SOS simulation    | MVP    |
| Event simulator      | Development and testing  | MVP    |
| PIR sensor           | Presence information     | Pilot  |
| Wearable             | Movement and SOS signals | Pilot  |
| mmWave               | Presence and movement    | Pilot  |
| Camera               | Optional fall detection  | Pilot  |
| External partner API | Service-related events   | Future |

### Layer 2 — Edge Processing

Responsibilities:

- Run local inference.
- Process sensor inputs.
- Filter invalid signals.
- Generate event metadata.
- Buffer events during temporary network outages where supported.

Fall Detection integration:

```text
Camera / Video
      |
      v
YOLO Pose
      |
      v
Person Tracking
      |
      v
Kinematic Analysis
      |
      v
Fall State Machine
      |
      v
Fall Alert
      |
      v
Event Publisher
```

The AI module should publish structured event information rather than exposing the full video stream to the backend.

### Layer 3 — API Layer

Technology:

- Python.
- FastAPI.
- Pydantic.
- Uvicorn.

Responsibilities:

- Validate incoming requests.
- Apply authentication checks.
- Expose event endpoints.
- Return standardized responses.
- Forward requests to application services.

### Layer 4 — Application Layer

Core services:

| Service              | Responsibility                 |
| -------------------- | ------------------------------ |
| Event Service        | Create and retrieve events     |
| Event Engine         | Process lifecycle transitions  |
| Contact Service      | Manage emergency contacts      |
| Escalation Service   | Determine next response action |
| Notification Service | Deliver notifications          |
| Audit Service        | Record important actions       |
| Device Service       | Manage device metadata         |
| Care Service         | Manage care profiles and plans |

These services describe the target modular architecture. They do not imply that every service currently exists as a separate implementation.

### Layer 5 — Data Layer

Logical data domains:

- Users.
- Households.
- Care Profiles.
- Emergency Contacts.
- Devices.
- Events.
- Event History.
- Audit Logs.
- Consent Records.
- Care Plans.
- Care Tasks.

Current prototype:

- SQLite persistence for events and audit logs.

Future consideration:

- PostgreSQL for multi-household and multi-user deployment.

### Layer 6 — Presentation Layer

Current:

- Lightweight browser-based Caregiver Dashboard.

Planned:

- Family App.
- Coordinator Console.
- Care Network Interface.

Dashboard responsibilities:

- Display events.
- Display priority and status.
- Allow authorized acknowledgement.
- Allow resolution.
- Allow false-alarm classification.
- Display event history.

---

## 4. Deployment Architecture

### 4.1. Development Deployment

```text
WINDOWS DEVELOPMENT MACHINE
          |
          +----------------------+
          |                      |
          v                      v
    FALL DETECTION          FASTAPI SERVER
    DESKTOP APP             127.0.0.1:8000
          |                      |
          v                      v
    EVENT PUBLISHER ------> EVENT API
                                 |
                                 v
                              SQLITE
                                 |
                                 v
                         CAREGIVER DASHBOARD
```

The current local setup is suitable for development and demonstration, not production emergency operations.

### 4.2. Future Pilot Deployment

```text
HOUSEHOLD
   |
   +-- SOS Device
   +-- Optional Sensors
   +-- Home Hub
           |
           v
      Secure Connection
           |
           v
      CARE LOOP API
           |
           v
      Event Processing
           |
      +----+-----+
      |          |
      v          v
   Database  Notification
                 |
          +------+------+
          |             |
          v             v
       Family       Caregiver
       Interface    Interface
```

A pilot deployment requires appropriate monitoring, backup connectivity, security controls, and a tested manual fallback.

---

## 5. Communication Patterns

| Communication                    | Method                             |
| -------------------------------- | ---------------------------------- |
| AI to Backend                    | HTTP POST                          |
| Dashboard to Backend             | HTTP GET / POST                    |
| Backend to Database              | SQL                                |
| Backend to Notification Provider | Provider API                       |
| Device to Home Hub               | Device-specific protocol           |
| Home Hub to Cloud                | Secure HTTP / MQTT where supported |

The existing AI Event Publisher uses HTTP-based delivery to the local API.

WebSocket or MQTT support is a future option, not a current requirement.

---

## 6. Failure Handling

| Failure                           | Expected Behavior                                     |
| --------------------------------- | ----------------------------------------------------- |
| Camera disconnected               | Report sensor unavailable                             |
| AI inference fails                | Record processing error                               |
| Backend unavailable               | Log delivery failure; future queue/retry mechanism    |
| Database unavailable              | Reject or safely fail persistence                     |
| Notification provider unavailable | Record failed notification attempt                    |
| Contact does not respond          | Trigger configured escalation                         |
| Device offline                    | Mark connection status unknown/offline when supported |

The system must never silently interpret missing sensor data as proof that the household is safe.

---

## 7. Current Implementation vs Target Architecture

| Component                     | Current Status        |
| ----------------------------- | --------------------- |
| YOLO Pose pipeline            | Implemented prototype |
| Person tracking               | Implemented prototype |
| Fall State Machine            | Implemented prototype |
| Desktop GUI                   | Implemented           |
| FastAPI backend               | Implemented           |
| SQLite event persistence      | Implemented           |
| Event Publisher               | Implemented           |
| Basic Caregiver Dashboard     | Implemented           |
| Event acknowledgement         | Implemented           |
| Event resolution              | Implemented           |
| Audit history                 | Implemented           |
| Care Profile management       | Not implemented       |
| Emergency Contact Tree        | Not implemented       |
| Real SMS / voice notification | Not implemented       |
| Automated escalation provider | Not implemented       |
| User authentication and RBAC  | Not implemented       |
| Device provisioning           | Not implemented       |
| Production consent management | Not implemented       |
| Family Mobile App             | Not implemented       |

Implementation status must be rechecked against the current Git commit before each release.

---

## 8. Architecture Evolution

**MVP:**

- Single backend.
- Local database.
- Event-driven application logic.
- Simulated input.
- Browser dashboard.

**Pilot:**

- Physical SOS device.
- Device adapters.
- Basic notification provider.
- Household management.
- Improved authentication.
- Optional Edge AI.

**Expansion:**

- Multi-household deployment.
- PostgreSQL.
- External integrations.
- Mobile applications.
- Scalable notification infrastructure.
- Operational monitoring.

---

## 9. Architecture Acceptance Criteria

The architecture is considered documented when:

1. All logical layers are defined.
2. Each layer has clear responsibilities.
3. Data flow between components is described.
4. Existing and planned components are distinguished.
5. Failure scenarios are documented.
6. AI and human response responsibilities are separated.
7. Privacy and security requirements are included.

**Architecture principle: Sensors generate signals, the platform coordinates events, and humans remain responsible for real-world response.**
