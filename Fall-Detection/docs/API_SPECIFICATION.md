# CARE LOOP — API SPECIFICATION

**Version:** 1.0  
**Date:** 19 November 2026  
**Backend:** FastAPI  
**Base URL (Development):** `http://127.0.0.1:8000`  
**API Prefix:** `/api/v1`

---

## 1. API Overview

The CARE LOOP API provides a standardized interface for event intake, event management, and caregiver interaction.

The API separates:

- Event ingestion.
- Event retrieval.
- Event lifecycle operations.
- Audit history.
- Health monitoring.
- Future care and device management.

### 1.1. Current API Endpoints

The repository implementation status documents these endpoints:

| Method | Endpoint                                | Purpose                |
| ------ | --------------------------------------- | ---------------------- |
| GET    | `/`                                     | Caregiver Dashboard    |
| GET    | `/health`                               | Health check           |
| POST   | `/api/v1/events`                        | Create event           |
| GET    | `/api/v1/events`                        | List events            |
| GET    | `/api/v1/events/{event_id}`             | Get event details      |
| POST   | `/api/v1/events/{event_id}/acknowledge` | Acknowledge event      |
| POST   | `/api/v1/events/{event_id}/resolve`     | Resolve event          |
| POST   | `/api/v1/events/{event_id}/false-alarm` | Mark false alarm       |
| GET    | `/api/v1/events/{event_id}/audit`       | Retrieve audit history |

The exact request and response fields must be confirmed against the current Pydantic models and route handlers before client implementation.

---

## 2. General API Conventions

### 2.1. Content Type

Requests containing JSON should use:

```http
Content-Type: application/json
```

### 2.2. Timestamp Format

Use ISO 8601 timestamps in UTC.

Example:

```text
2026-11-19T07:30:00Z
```

### 2.3. Identifier Format

Use unique string identifiers for:

- Event IDs.
- User IDs.
- Device IDs.
- Household IDs.

UUID is recommended for newly introduced entities.

### 2.4. Standard Error Format

Proposed response:

```json
{
  "error": {
    "code": "INVALID_EVENT",
    "message": "The event payload is invalid.",
    "details": {}
  }
}
```

---

## 3. Health API

### GET /health

Purpose:

Verify that the backend service is running.

Example response:

```json
{
  "status": "ok"
}
```

A successful health response does not necessarily mean the database, notification provider, or all integrations are healthy.

A future readiness endpoint should check dependencies separately.

---

## 4. Event API

### 4.1. Create Event

**POST `/api/v1/events`**

Purpose:

Receive an event from the SOS interface, simulator, or an integrated device/AI component.

Proposed request:

```json
{
  "profile_id": "profile_001",
  "device_id": "device_001",
  "event_type": "SOS",
  "priority": "P0",
  "source": "APP",
  "description": "User requested emergency assistance",
  "metadata": {
    "location_zone": "living_room"
  }
}
```

Expected behavior:

1. Validate the payload.
2. Verify the source and authorization.
3. Validate the related profile and device when supplied.
4. Generate a unique event ID.
5. Store the event.
6. Record event creation in the audit history.
7. Trigger the configured notification workflow.
8. Return the created event.

Proposed response:

```json
{
  "event_id": "evt_001",
  "event_type": "SOS",
  "priority": "P0",
  "status": "NEW",
  "source": "APP",
  "created_at": "2026-11-19T07:30:00Z"
}
```

The example is a proposed contract, not a guarantee of the current implementation's exact response shape.

### 4.2. List Events

**GET `/api/v1/events`**

Supported query parameters:

| Parameter  | Type    | Description              |
| ---------- | ------- | ------------------------ |
| status     | string  | Filter by event status   |
| priority   | string  | Filter by priority       |
| limit      | integer | Maximum returned records |
| offset     | integer | Pagination offset        |
| profile_id | string  | Filter by profile        |
| event_type | string  | Filter by event type     |

Example:

```http
GET /api/v1/events?status=NEW&limit=50&offset=0
```

Expected behavior:

- Return matching events.
- Apply pagination.
- Sort newest events first by default.
- Restrict data according to authorization.

### 4.3. Get Event Details

**GET `/api/v1/events/{event_id}`**

Purpose:

Retrieve an individual event.

Example:

```http
GET /api/v1/events/evt_001
```

Proposed response:

```json
{
  "event_id": "evt_001",
  "profile_id": "profile_001",
  "event_type": "SOS",
  "priority": "P0",
  "status": "ACKNOWLEDGED",
  "source": "APP",
  "created_at": "2026-11-19T07:30:00Z",
  "acknowledged_at": "2026-11-19T07:31:00Z"
}
```

---

## 5. Event Lifecycle APIs

### 5.1. Acknowledge Event

**POST `/api/v1/events/{event_id}/acknowledge`**

Purpose:

Record that an authorized recipient has accepted responsibility for following up on an alert.

Proposed request:

```json
{
  "actor_id": "user_002",
  "note": "I have received the alert and will contact the elderly person."
}
```

Expected behavior:

- Verify the event exists.
- Verify the actor is authorized.
- Validate the current event state.
- Update acknowledgement information.
- Record the action in audit history.

Acknowledgement must not automatically mark the event as resolved.

### 5.2. Resolve Event

**POST `/api/v1/events/{event_id}/resolve`**

Purpose:

Record the completion of the response workflow.

Proposed request:

```json
{
  "actor_id": "user_002",
  "resolution_note": "Contacted the elderly person and verified the situation."
}
```

Expected behavior:

- Verify the event is in a resolvable state.
- Record the responsible actor.
- Store the resolution time.
- Update the event status.
- Create an audit record.

### 5.3. Mark False Alarm

**POST `/api/v1/events/{event_id}/false-alarm`**

Purpose:

Record that a reviewed alert was not a corresponding incident.

Proposed request:

```json
{
  "actor_id": "user_002",
  "reason": "Verified as a non-fall activity."
}
```

False alarm classification should not delete the original event.

---

## 6. Audit API

### GET /api/v1/events/{event_id}/audit

Purpose:

Retrieve the history of actions related to an event.

Proposed response:

```json
{
  "event_id": "evt_001",
  "audit": [
    {
      "action": "EVENT_CREATED",
      "actor_id": "SYSTEM",
      "timestamp": "2026-11-19T07:30:00Z"
    },
    {
      "action": "EVENT_ACKNOWLEDGED",
      "actor_id": "user_002",
      "timestamp": "2026-11-19T07:31:00Z"
    }
  ]
}
```

Audit records must not be editable through ordinary user-facing endpoints.

---

## 7. Proposed Future APIs

These endpoints are design proposals and are not confirmed as implemented.

### 7.1. Care Profile

| Method | Endpoint                | Purpose                  |
| ------ | ----------------------- | ------------------------ |
| POST   | `/api/v1/profiles`      | Create profile           |
| GET    | `/api/v1/profiles`      | List authorized profiles |
| GET    | `/api/v1/profiles/{id}` | Get profile              |
| PATCH  | `/api/v1/profiles/{id}` | Update profile           |

### 7.2. Emergency Contacts

| Method | Endpoint                         | Purpose            |
| ------ | -------------------------------- | ------------------ |
| POST   | `/api/v1/profiles/{id}/contacts` | Add contact        |
| GET    | `/api/v1/profiles/{id}/contacts` | List contacts      |
| PATCH  | `/api/v1/contacts/{id}`          | Update contact     |
| DELETE | `/api/v1/contacts/{id}`          | Deactivate contact |

### 7.3. Devices

| Method | Endpoint                         | Purpose              |
| ------ | -------------------------------- | -------------------- |
| POST   | `/api/v1/devices`                | Register device      |
| GET    | `/api/v1/devices`                | List devices         |
| GET    | `/api/v1/devices/{id}`           | Device details       |
| POST   | `/api/v1/devices/{id}/heartbeat` | Submit heartbeat     |
| PATCH  | `/api/v1/devices/{id}/status`    | Update device status |

### 7.4. Care Plans

| Method | Endpoint                        | Purpose       |
| ------ | ------------------------------- | ------------- |
| POST   | `/api/v1/care-plans`            | Create plan   |
| GET    | `/api/v1/care-plans/{id}`       | Retrieve plan |
| POST   | `/api/v1/care-plans/{id}/tasks` | Create task   |
| PATCH  | `/api/v1/care-tasks/{id}`       | Update task   |

### 7.5. Consent

| Method | Endpoint                | Purpose                             |
| ------ | ----------------------- | ----------------------------------- |
| POST   | `/api/v1/consents`      | Record consent                      |
| GET    | `/api/v1/consents`      | Retrieve authorized consent records |
| PATCH  | `/api/v1/consents/{id}` | Update or withdraw consent          |

---

## 8. HTTP Status Codes

| Code | Meaning                              |
| ---- | ------------------------------------ |
| 200  | Request successful                   |
| 201  | Resource created                     |
| 400  | Invalid request                      |
| 401  | Authentication required              |
| 403  | Permission denied                    |
| 404  | Resource not found                   |
| 409  | Invalid state transition or conflict |
| 422  | Validation error                     |
| 429  | Rate limit exceeded                  |
| 500  | Internal server error                |
| 503  | Service unavailable                  |

---

## 9. API Security

Future production API requirements:

- Authentication for user-facing endpoints.
- Authorization for every sensitive operation.
- Secure service-to-service credentials.
- Request validation.
- Rate limiting.
- Audit logging.
- TLS for external communication.
- Secret rotation.
- No sensitive information in error messages.

The current shared API key is a development safeguard, not a substitute for account authentication and role-based authorization.

---

## 10. API Versioning

All application endpoints should remain under `/api/v1`.

Breaking changes should be introduced through a controlled versioning and migration process.

Backward compatibility should be maintained for existing event publishers whenever practical.

---

## 11. API Acceptance Criteria

- Existing endpoints are documented.
- Proposed future endpoints are distinguished.
- Request and response examples are provided.
- Lifecycle operations are defined.
- Error responses are standardized.
- Authentication and authorization requirements are documented.
- API behavior can be verified through automated tests.

**API principle: Every event operation must have a defined request, authorization rule, state transition, and auditable outcome.**
