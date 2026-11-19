# CARE LOOP — MVP FEATURE SPECIFICATION

**Project:** CARE LOOP  
**Document:** MVP Features & Acceptance Criteria  
**Version:** 1.0  
**Date:** 19 November 2026

---

## 1. MVP Objective

The objective of the CARE LOOP MVP is to demonstrate a complete home safety event coordination workflow.

The MVP must demonstrate that the platform can:

1. Receive an SOS or simulated incident signal.
2. Create and classify an event.
3. Notify designated contacts.
4. Record acknowledgement.
5. Support human verification and response coordination.
6. Record the final event outcome.
7. Maintain event history and audit records.

The MVP prioritizes the reliability of the response workflow rather than advanced sensor technology.

---

## 2. Feature Prioritization

Features are categorized into three levels.

| Priority         | Meaning                        |
| ---------------- | ------------------------------ |
| P0 — Must Have   | Required for MVP demonstration |
| P1 — Should Have | Important for a complete pilot |
| P2 — Future      | Planned for later development  |

---

## 3. P0 — Core MVP Features

### 3.1. Care Profile Management

**Description:** Store essential information about the elderly person and their care arrangements.

Functional requirements:

- Create a Care Profile.
- Store basic user information.
- Store emergency contact information.
- Record relevant assistance requirements.
- Configure information-sharing permissions.

Acceptance criteria:

- A profile can be created and retrieved.
- Emergency contact information can be updated.
- Only authorized users can access the profile.

### 3.2. Emergency Contact Tree

**Description:** Maintain a list of designated people who should receive notifications when an event occurs.

Functional requirements:

- Add and remove emergency contacts.
- Store contact information.
- Define contact priority.
- Configure backup contacts.
- Associate contacts with an elderly user's profile.

Acceptance criteria:

- A profile can have multiple contacts.
- Contact priority is stored.
- The system can identify the next designated contact in the configured escalation sequence.

### 3.3. SOS Event Generation

**Description:** Allow an elderly user or a test operator to generate an SOS event.

Input methods:

- Simulated SOS event through the application.
- API-based event generation.
- Physical SOS device integration when available.

Event information:

- Event ID.
- User ID.
- Event type.
- Event timestamp.
- Event source.
- Priority.
- Initial event status.

Acceptance criteria:

- An SOS signal creates a unique event.
- The backend receives and stores the event.
- Duplicate submissions can be identified and handled safely.

### 3.4. Event Management Engine

**Description:** Process events and manage their lifecycle.

Core responsibilities:

- Receive event information.
- Assign an event status.
- Determine the response workflow.
- Track acknowledgement.
- Handle escalation.
- Record resolution.

Proposed event lifecycle:

```text
NEW
 |
 v
NOTIFIED
 |
 +------> ACKNOWLEDGED
 |               |
 |               v
 |           VERIFYING
 |               |
 |               v
 |          IN_PROGRESS
 |               |
 |               v
 |            RESOLVED
 |
 +------> ESCALATED
                 |
                 v
            ACKNOWLEDGED
```

Additional outcome:

```text
NEW / NOTIFIED / ACKNOWLEDGED
                 |
                 v
            FALSE_ALARM
```

The event lifecycle must distinguish notification, acknowledgement, human verification, and actual resolution.

### 3.5. Caregiver Dashboard

**Description:** Provide a central interface for family members or authorized caregivers to review and manage events.

Required information:

- Event ID.
- Elderly person's display name.
- Event type.
- Priority.
- Event creation time.
- Event status.
- Event source.
- Assigned or acknowledging contact.

Required actions:

- View event details.
- Acknowledge an event.
- Mark an event as in progress.
- Resolve an event.
- Mark a false alarm.
- Review event history.

Acceptance criteria:

- New events appear on the dashboard.
- Event status updates after an authorized action.
- The event history displays previous records.
- Important actions are recorded in the audit log.

### 3.6. Notification Workflow

**Description:** Notify designated contacts when an event is created or escalated.

MVP implementation options:

- In-application notification.
- Dashboard notification.
- Simulated SMS/voice notification.
- Actual SMS/voice integration when an appropriate provider is configured.

Acceptance criteria:

- A new event triggers the configured notification workflow.
- Notification attempts are recorded.
- Delivery status and acknowledgement status are not treated as the same thing.

### 3.7. Event History and Audit Log

**Description:** Preserve a traceable history of events and important actions.

Event History records:

- Event creation.
- Event type.
- Event status changes.
- Event timestamps.
- Resolution information.

Audit Log records:

- Actor.
- Action.
- Target event.
- Timestamp.
- Relevant action metadata.

Acceptance criteria:

- Event records remain available after the dashboard is refreshed.
- Important state transitions are recorded.
- Unauthorized actions are rejected and logged where appropriate.

---

## 4. P1 — Important Pilot Features

### 4.1. Basic Device Management

- Register a device.
- Associate a device with a household.
- Store device type and identifier.
- Record connection status.
- Record battery status where supported.
- Display basic device health information.

Acceptance criteria:

- Registered devices can be associated with a user or household.
- Device status can be retrieved.
- Offline devices can be identified when connectivity information is available.

### 4.2. Escalation Management

**Description:** Escalate events when no designated contact acknowledges them within the configured response window.

Functional requirements:

- Configure contact priority.
- Configure acknowledgement timeout.
- Notify the next contact when the timeout is reached.
- Record each escalation attempt.
- Stop escalation when an authorized recipient acknowledges the event, according to the configured policy.

Acceptance criteria:

- Escalation follows the configured contact order.
- Each escalation is recorded.
- The system does not claim that a person has responded merely because a notification was sent.

Actual response deadlines and service commitments must be established through operational testing and available staffing.

### 4.3. Basic Care Plan Management

- Store agreed care tasks.
- Associate tasks with designated caregivers.
- Record task frequency.
- Record task completion.
- Review previous support activities.

Acceptance criteria:

- A task can be created and assigned.
- Task status can be updated.
- Completed tasks remain available in history.

### 4.4. Basic Offline Simulation

- Simulate a device losing connectivity.
- Simulate delayed event delivery.
- Simulate a contact failing to acknowledge an event.
- Record the failure scenario.
- Verify the fallback workflow.

Acceptance criteria:

- The dashboard can distinguish device connectivity problems from normal operation.
- The system records simulated failure conditions.
- Recovery behavior is documented.

---

## 5. P2 — Future Development Features

The following features are outside the initial MVP.

### 5.1. Advanced IoT Integration

- PIR sensor integration.
- mmWave radar integration.
- Wearable IMU integration.
- Multi-sensor fusion.
- Home Hub device management.
- Firmware lifecycle management.

### 5.2. Camera-Based Fall Detection

- YOLO Pose inference.
- Multi-person tracking.
- Kinematic analysis.
- Occlusion handling.
- Fall classification.
- Edge AI integration.

The current Fall Detection V3 repository is a technical prototype for this capability. It must be evaluated independently before being treated as a validated household safety feature.

### 5.3. Family Mobile Application

- Mobile push notifications.
- Family care overview.
- Event acknowledgement.
- Care Plan management.
- Household-level configuration.

### 5.4. Partner Integration

- External caregiver services.
- Non-emergency transportation providers.
- Healthcare facility information.
- Partner APIs.
- Service referral and coordination.

### 5.5. Advanced Analytics

- Event trend analysis.
- Household-level activity summaries.
- Device reliability metrics.
- Care service performance.
- Operational reporting.

---

## 6. Event Priority Classification

The following is a proposed internal operational classification. It is not a medical diagnosis or a validated clinical triage system.

| Priority | Description                                                    | Example                                                 |
| -------- | -------------------------------------------------------------- | ------------------------------------------------------- |
| P0       | Potentially critical event requiring immediate human attention | SOS indicating a potentially life-threatening situation |
| P1       | High-priority safety event                                     | Suspected fall or prolonged immobility                  |
| P2       | Important event requiring follow-up                            | Missed check-in or repeated abnormal activity           |
| P3       | Device or connectivity issue                                   | Sensor offline or low battery                           |
| P4       | Informational event                                            | Routine status update                                   |

The priority assigned by the platform must not replace professional medical assessment.

For suspected life-threatening incidents, the responsible person should contact the appropriate official emergency medical channel rather than waiting for the platform's normal escalation process.

---

## 7. MVP User Scenarios

### Scenario 1 — SOS Request

**Given:** An elderly user has an active Care Profile and configured emergency contacts.

**When:** The user presses SOS or an operator simulates an SOS event.

**Then:**

1. The platform receives the signal.
2. A new event is created.
3. The event is stored in the database.
4. The configured contacts are notified.
5. The event appears on the caregiver dashboard.
6. A designated recipient can acknowledge the event.

### Scenario 2 — Contact Acknowledgement

**Given:** A new event has been created and notified.

**When:** A designated contact acknowledges the event.

**Then:**

1. The event status changes to ACKNOWLEDGED.
2. The actor and timestamp are recorded.
3. The dashboard displays the updated status.
4. The acknowledgement is added to the audit history.

Acknowledgement only confirms that the recipient received the alert. It does not confirm that the elderly person is safe.

### Scenario 3 — No Contact Response

**Given:** An event has been notified but no contact has acknowledged it.

**When:** The configured acknowledgement timeout expires.

**Then:**

1. The Event Engine evaluates the escalation rule.
2. The next designated contact is notified.
3. The escalation attempt is recorded.
4. The event remains active until an appropriate response is recorded.

### Scenario 4 — Event Resolution

**Given:** A recipient has verified the situation and coordinated assistance.

**When:** The authorized recipient resolves the event.

**Then:**

1. The event status changes to RESOLVED.
2. Resolution information is stored.
3. The actor and timestamp are recorded.
4. The event remains accessible in Event History.

### Scenario 5 — False Alarm

**Given:** A generated alert has been reviewed and determined not to represent the corresponding incident.

**When:** An authorized recipient marks it as FALSE_ALARM.

**Then:**

1. The event is classified as FALSE_ALARM.
2. The action is recorded in the audit log.
3. The event remains available for later analysis.

### Scenario 6 — Device Offline

**Given:** A registered device stops reporting its connection status.

**When:** The platform detects a missing heartbeat or receives an offline signal.

**Then:**

1. The device status is updated when the information is available.
2. The platform records the connectivity issue.
3. The relevant operator can review the device condition.
4. The system does not silently treat an offline device as functioning normally.

---

## 8. MVP Acceptance Test Matrix

| Test ID | Test Case                 | Expected Result                   |
| ------- | ------------------------- | --------------------------------- |
| TC-01   | Create Care Profile       | Profile stored successfully       |
| TC-02   | Add emergency contacts    | Contacts associated with profile  |
| TC-03   | Generate SOS event        | Unique event created              |
| TC-04   | Submit event to API       | API accepts valid event           |
| TC-05   | Store event               | Event persists in database        |
| TC-06   | Display event             | Dashboard shows new event         |
| TC-07   | Acknowledge event         | Status and actor updated          |
| TC-08   | Escalate event            | Next contact workflow triggered   |
| TC-09   | Resolve event             | Resolution stored                 |
| TC-10   | Mark false alarm          | False alarm classification stored |
| TC-11   | Review event history      | Previous events retrievable       |
| TC-12   | Review audit log          | Important actions retrievable     |
| TC-13   | Simulate device offline   | Device issue recorded             |
| TC-14   | Simulate delayed response | Escalation behavior verified      |

Test results must be reported as:

- **PASS:** Executed and verified successfully.
- **PARTIAL:** Implemented but not fully verified.
- **FAIL:** Executed and failed.
- **NOT TESTED:** No execution evidence available.

---

## 9. MVP Demonstration Flow

The recommended MVP demonstration should follow this sequence:

```text
START
  |
  v
Create Elderly User Profile
  |
  v
Configure Emergency Contacts
  |
  v
Generate SOS Event
  |
  v
Backend Receives Event
  |
  v
Database Stores Event
  |
  v
Dashboard Displays Alert
  |
  v
Notify Designated Contact
  |
  v
Contact Acknowledges
  |
  v
Human Verification
  |
  v
Coordinate Assistance
  |
  v
Resolve Event
  |
  v
Update Event History
  |
  v
END
```

A second demonstration should show the no-acknowledgement scenario and escalation to a backup contact.

The demo may use simulated SOS events and simulated notifications. These must be clearly labelled as simulations.

---

## 10. Feature Delivery Roadmap

| Phase     | Timeline     | Main Deliverables                                                               |
| --------- | ------------ | ------------------------------------------------------------------------------- |
| MVP       | 0–3 months   | Care Profile, Contact Tree, Event API, Dashboard, SOS simulation, Event History |
| Pilot     | 3–12 months  | Physical SOS devices, basic IoT, optional sensors, Edge AI, household testing   |
| Expansion | 12–36 months | Multi-sensor integration, Partner Connect, advanced care coordination           |

The timeline represents the proposed product roadmap, not a statement that every feature has already been implemented.

---

## 11. MVP Completion Definition

The CARE LOOP MVP is considered ready for functional demonstration when the team can show a complete event coordination cycle from signal generation to recorded resolution.

The minimum proof must include:

- A working event creation workflow.
- A functioning backend API.
- Persistent event records.
- A caregiver dashboard.
- Acknowledgement and resolution actions.
- Event history and audit records.
- A tested escalation scenario.
- Documented limitations and failure scenarios.

The completion of this MVP does not imply production readiness, clinical validation, guaranteed fall detection, or 24/7 emergency response.

**Core principle: CARE LOOP must demonstrate not only that an event can be detected, but also that the event can reach a responsible person and have its outcome recorded.**
