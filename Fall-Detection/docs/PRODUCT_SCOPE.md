# CARE LOOP — PRODUCT SCOPE

**Project:** CARE LOOP  
**Document:** Product Scope & Product Requirements  
**Version:** 1.0  
**Date:** 19 November 2026  
**Target Market:** Vietnam — Initial focus on Ho Chi Minh City  
**Product Category:** Home Safety & Care Coordination Platform

---

## 1. Product Overview

### 1.1. Product Definition

CARE LOOP is a home safety and care coordination platform designed to connect elderly people living at home with their families, designated caregivers, community support networks, and appropriate external services.

The platform aims to transform an emergency signal or abnormal event into a coordinated response involving responsible people.

Rather than functioning as a standalone monitoring device, CARE LOOP provides a continuous coordination process:

**Signal Detection → Event Creation → Notification → Acknowledgement → Human Verification → Response Coordination → Resolution → Care Plan Update.**

CARE LOOP combines software infrastructure, optional IoT devices, event management, and human response coordination to improve the safety and continuity of elderly care at home.

### 1.2. Problem Statement

Elderly people living independently may experience unexpected incidents such as falls, prolonged immobility, or situations where they need assistance but cannot contact family members.

Meanwhile, family members may live far away, have limited availability, or lack a reliable way to coordinate assistance.

Existing devices can generate alerts, but an alert alone does not guarantee that someone will verify the incident or provide assistance.

The main problem CARE LOOP addresses is therefore not simply the lack of monitoring technology, but the lack of a coordinated process connecting an incident to a responsible human response.

### 1.3. Product Vision

To become a trusted home safety and care coordination infrastructure connecting elderly people, families, community support networks, and appropriate healthcare and transportation services.

CARE LOOP aims to help elderly people maintain independence while giving families better visibility into care activities and incident response.

### 1.4. Product Mission

- Provide accessible ways for elderly people to request assistance.
- Help families receive and manage safety-related events.
- Coordinate designated caregivers and community support networks.
- Maintain structured records of incidents and care activities.
- Connect users with appropriate external services when necessary.
- Protect the privacy, consent, and autonomy of elderly users.

---

## 2. Target Users and Stakeholders

### 2.1. Primary Users

**Elderly People**

- Live independently or with limited daily assistance.
- Need an accessible way to request help.
- Want to maintain independence and personal privacy.
- Should be able to decide what information is shared and with whom.

**Family Members / Caregivers**

- Monitor relevant safety events.
- Receive notifications and acknowledge alerts.
- Coordinate assistance with other designated contacts.
- Review incident history and response outcomes.

### 2.2. Secondary Stakeholders

**Community Support Network**

- Designated neighbors.
- Verified volunteers.
- Local caregivers.
- Community organizations.

**External Service Providers**

- Healthcare facilities.
- Qualified emergency medical services.
- Non-emergency transportation providers.
- Home-care service providers.

These stakeholders may participate through defined workflows or future integrations. Their involvement is subject to consent, operational capability, and appropriate agreements.

---

## 3. Product Scope

### 3.1. Core Product Components

| Component                     | Description                                        |
| ----------------------------- | -------------------------------------------------- |
| CARE LOOP Home Safety         | SOS devices and optional household sensors         |
| CARE LOOP Platform            | Central event and care coordination infrastructure |
| CARE LOOP Family Interface    | Family-facing notifications and event monitoring   |
| CARE LOOP Coordinator Console | Event management and response coordination         |
| CARE LOOP Care Network        | Designated caregivers and community support        |
| CARE LOOP Partner Connect     | Future connection to external service providers    |

### 3.2. Product Architecture — Ecosystem Perspective

CARE LOOP is organized into six functional loops and one cross-cutting governance layer.

**Core — Human Layer**

- Elderly people.
- Family members.
- Authorized representatives where applicable.
- Care Profile and Care Plan.

**Loop 1 — Sensor Layer**

- Physical SOS buttons.
- Wearable devices.
- PIR and door sensors.
- Pressure sensors.
- Optional RGB/depth cameras.
- Optional mmWave radar.
- Home Hub.

**Loop 2 — AI / Edge Layer**

- Sensor data processing.
- Pose and movement analysis.
- Event filtering.
- Multi-sensor signal interpretation.
- Suspicious event generation.

**Loop 3 — Platform Layer**

- CARE LOOP API.
- Event Engine.
- Database.
- Notification services.
- Family Dashboard.
- Event History.
- Audit Log.
- Escalation Management.

**Loop 4 — Human Response Layer**

- Family members.
- Designated neighbors.
- Caregivers.
- Community support personnel.
- Coordinators when an operational team is available.

**Loop 5 — External Partner Layer**

- Healthcare facilities.
- Official emergency medical channels.
- Qualified transportation providers.
- Home-care service providers.

**Cross-Cutting Governance Layer**

- Consent Management.
- Privacy.
- Authentication and Authorization.
- Device Security.
- Audit Logging.
- Incident Management.
- Service-Level Management.

### 3.3. MVP Scope

The initial MVP focuses on proving that CARE LOOP can receive an SOS signal, create an event, notify the appropriate contacts, record acknowledgement, coordinate a human response, and maintain an event history.

**MVP — 0 to 3 Months**

Included:

1. SOS event simulation and/or compatible SOS input.
2. Basic Care Profile.
3. Emergency Contact Tree.
4. Event API.
5. Event Management Engine.
6. Family-facing notification flow.
7. Caregiver Dashboard.
8. Event Acknowledgement and Resolution.
9. Event History and Audit Log.
10. Basic device and connection status.
11. Simulated offline and non-response scenarios.

The MVP may use simulated events before physical device integration is available.

Camera-based fall detection is not mandatory for the MVP.

### 3.4. Pilot Scope — 3 to 12 Months

After the core event coordination workflow is validated, CARE LOOP may introduce:

- PIR or mmWave sensors.
- Optional camera-based fall detection.
- Edge AI processing.
- Device fleet management.
- Multi-sensor event interpretation.
- Field testing with consented households.
- Partnerships with home-care and transportation providers.

The proposed device pilot is separate from the core service pilot and must be evaluated independently.

### 3.5. Expansion Scope — 12 to 36 Months

Potential future capabilities:

- Multi-sensor integration.
- Wearable device integration.
- Partner APIs.
- Advanced caregiver coordination.
- Household-level configuration.
- Operational coordinator services, subject to staffing and service-level commitments.

These capabilities are strategic directions, not current MVP commitments.

---

## 4. Functional Requirements

| ID    | Requirement                                        | Priority |
| ----- | -------------------------------------------------- | -------- |
| FR-01 | Create and manage an elderly user's Care Profile   | Must     |
| FR-02 | Configure emergency contacts                       | Must     |
| FR-03 | Receive SOS events                                 | Must     |
| FR-04 | Create and store event records                     | Must     |
| FR-05 | Notify designated contacts                         | Must     |
| FR-06 | Allow recipients to acknowledge events             | Must     |
| FR-07 | Record event resolution                            | Must     |
| FR-08 | Maintain event history                             | Must     |
| FR-09 | Maintain audit records                             | Must     |
| FR-10 | Track basic device status                          | Should   |
| FR-11 | Simulate sensor-generated events                   | Must     |
| FR-12 | Support escalation when acknowledgement is missing | Must     |
| FR-13 | Manage Care Plans and support tasks                | Should   |
| FR-14 | Integrate physical SOS devices                     | Should   |
| FR-15 | Integrate optional camera-based fall detection     | Future   |
| FR-16 | Integrate external service providers               | Future   |

Priority definitions:

- **Must:** Essential to demonstrate the MVP.
- **Should:** Important but can be delivered incrementally.
- **Future:** Outside the initial MVP implementation scope.

---

## 5. Non-Functional Requirements

### 5.1. Reliability

- Event creation and status transitions must be recorded.
- The system should prevent duplicate event creation during retries.
- Device connectivity failures should be identifiable.
- Notification delivery and acknowledgement should be distinguishable.

### 5.2. Security and Privacy

- Apply authentication and authorization.
- Restrict access according to user roles and permissions.
- Collect only information necessary for the care workflow.
- Record important user and system actions.
- Obtain appropriate consent before collecting or sharing sensor and personal data.
- Provide a process for consent withdrawal.

### 5.3. Usability

- Provide an understandable interface for family members and caregivers.
- Keep SOS workflows simple.
- Clearly distinguish new, acknowledged, and resolved events.
- Avoid technical terminology in elderly-facing interfaces.

### 5.4. Maintainability

- Separate sensor adapters from event management logic.
- Keep API, database, and notification components modular.
- Support future device integration without redesigning the entire platform.

---

## 6. Out of Scope

The following capabilities are explicitly excluded from the initial MVP:

- Automatic emergency vehicle dispatch.
- Automatic diagnosis or treatment recommendations.
- Guaranteed detection of every fall.
- Guaranteed 24/7 human monitoring.
- Face recognition and biometric identity tracking.
- Continuous recording of private household spaces.
- Full-scale ambulance fleet operation.
- Large-scale cloud video analytics.
- Medical monitoring claims without appropriate assessment and validation.

CARE LOOP does not replace emergency services, hospitals, doctors, or qualified medical transportation providers.

For potentially life-threatening incidents, the responsible person must contact the appropriate official emergency medical channel.

---

## 7. Key User Journey

### Scenario: Elderly Person Requests Assistance

1. An elderly user presses the SOS button.
2. The device or application sends an SOS signal to CARE LOOP.
3. The platform creates an event with a unique event ID.
4. The Event Engine assigns the appropriate priority and response workflow.
5. Designated family members receive notifications.
6. One recipient acknowledges the event.
7. The recipient contacts or visits the elderly user to verify the situation.
8. If additional assistance is required, the recipient coordinates with the appropriate support network or external service.
9. The event is marked as resolved after the response is completed.
10. The platform stores the event and response history.

If no recipient acknowledges the event, the platform follows the configured escalation procedure.

Acknowledgement does not mean that the elderly person has already received assistance.

---

## 8. Success Metrics

CARE LOOP should evaluate success across three dimensions.

### 8.1. Operational Safety

- SOS event delivery rate.
- Notification delivery rate.
- Event acknowledgement rate.
- Time to acknowledgement.
- Percentage of events with recorded outcomes.
- Number of missed simulated events.

### 8.2. Care Quality

- Percentage of support tasks completed.
- Time required to coordinate assistance.
- Family satisfaction.
- Elderly user acceptance.
- Number of unresolved events.

### 8.3. Business Sustainability

- Cost per household.
- Cost per handled event.
- Device and connectivity costs.
- Willingness to pay.
- User retention.
- Cost of human response operations.

No performance target should be presented as achieved until supported by actual test or pilot evidence.

---

## 9. Product Constraints and Assumptions

- The initial team consists of two IT members and two social-science members.
- The team focuses on building the platform and response workflow while sourcing appropriate hardware from existing providers.
- The initial MVP prioritizes software and simulated event workflows.
- Physical hardware integration is incremental.
- Medical, emergency, legal, and device-safety expertise must be obtained from appropriate external advisors.
- Camera-based monitoring requires separate consent and privacy assessment.
- Operational commitments must reflect actual staffing and available resources.

---

## 10. MVP Acceptance Criteria

The MVP can be considered functionally demonstrated when:

1. A user profile can be created.
2. Emergency contacts can be configured.
3. An SOS event can be generated.
4. The backend receives and stores the event.
5. The event appears on the caregiver dashboard.
6. A designated recipient can acknowledge the event.
7. The event can be resolved.
8. Event history and audit records are available.
9. A missing acknowledgement triggers the configured escalation workflow.
10. Basic failure scenarios can be simulated and documented.

These criteria demonstrate a functional prototype. They do not establish clinical safety, production readiness, or guaranteed emergency response.

---

## 11. Product Development Principle

CARE LOOP must be designed around a human-centered response loop.

Technology identifies and communicates signals. The platform coordinates information and responsibilities. Human responders verify and act. Appropriate external providers deliver services within their authorized scope.

**The product is not simply a system that detects incidents. It is a system that helps ensure an incident reaches someone responsible for responding.**
