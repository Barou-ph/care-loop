# CARE LOOP — Product Scope & MVP Definition

Version: 1.0
Status: MVP Proposal
Project: CARE LOOP

## 1. Product Overview

CARE LOOP is an AI-powered elderly care and home safety
monitoring platform designed to help families monitor
elderly individuals, receive alerts about potential
safety incidents, and coordinate appropriate responses.

The platform connects monitoring devices, event detection
modules, caregivers, and family members through a unified
event management workflow.

Its primary value is not simply detecting incidents,
but ensuring that important alerts are received,
acknowledged, and followed up by responsible people.

## 2. Problem Statement

Elderly individuals living independently may face
unexpected incidents such as falls or emergencies
when family members and caregivers are unavailable.

Existing standalone monitoring devices may detect
or report an event but often lack an integrated
response workflow.

This creates several problems:

- Family members may not receive alerts promptly.
- Caregivers may not know whether another person
  has already responded.
- Incident history may be fragmented.
- Device connectivity failures may go unnoticed.
- Families may lack visibility into the response process.

CARE LOOP addresses these gaps through a centralized
monitoring and care coordination platform.

## 3. Target Users

### 3.1 Elderly Individuals

People who live independently or require occasional
monitoring and assistance.

Needs:

- Simple access to emergency assistance.
- Respect for privacy and personal autonomy.
- Reliable communication with designated contacts.

### 3.2 Family Members

Relatives responsible for monitoring and supporting
elderly individuals.

Needs:

- Receive incident notifications.
- Know whether an alert has been acknowledged.
- Track incident history and response status.

### 3.3 Caregivers

People assigned to provide assistance or verify incidents.

Needs:

- View assigned alerts.
- Acknowledge incidents.
- Record verification and resolution outcomes.

### 3.4 Administrators

Users responsible for configuring households,
devices, and access permissions.

## 4. Product Value Proposition

For elderly individuals:

- Accessible assistance and safety monitoring.

For family members:

- Greater visibility into safety incidents and
  response progress.

For caregivers:

- A structured workflow for handling alerts.

For care organizations:

- Centralized event history and operational visibility.

## 5. MVP Objectives

The MVP aims to demonstrate an end-to-end workflow:

1. Receive a safety-related signal.
2. Generate a structured event.
3. Display the event on a dashboard.
4. Notify or identify the responsible contact.
5. Allow the contact to acknowledge the event.
6. Record verification and resolution.
7. Maintain an event history.

The MVP focuses on demonstrating the platform workflow,
not proving medical-grade AI detection performance.

## 6. MVP Functional Requirements

| ID  | Feature                       | Description                                | Priority |
| --- | ----------------------------- | ------------------------------------------ | -------- |
| F01 | Household Management          | Manage household profiles                  | Must     |
| F02 | Device Management             | Register devices and monitor status        | Must     |
| F03 | Event Ingestion               | Receive SOS and detection events           | Must     |
| F04 | Event Dashboard               | Display active and historical events       | Must     |
| F05 | Alert Acknowledgement         | Allow contacts to acknowledge alerts       | Must     |
| F06 | Event Resolution              | Record outcomes and close events           | Must     |
| F07 | Event History                 | Maintain event and action history          | Must     |
| F08 | Role Management               | Separate admin, family and caregiver roles | Should   |
| F09 | Device Health Monitoring      | Track connectivity and battery status      | Should   |
| F10 | Escalation                    | Simulate notification to backup contacts   | Should   |
| F11 | AI Fall Detection Integration | Receive detection metadata from AI module  | Could    |
| F12 | Notification Integration      | Support notification provider integration  | Could    |

## 7. Core User Journey

### Emergency SOS Workflow

1. An elderly individual activates an SOS button.
2. CARE LOOP receives the signal.
3. The Event Engine creates a HIGH severity event.
4. The dashboard displays the incident.
5. A designated family member acknowledges the alert.
6. A caregiver verifies the situation.
7. The caregiver records the outcome.
8. The event is marked as RESOLVED.

## 8. Out of Scope

The following capabilities are excluded from the initial MVP:

- Medical diagnosis or treatment recommendations.
- Guaranteed detection of all falls.
- Autonomous emergency dispatch.
- Guaranteed 24/7 human monitoring.
- Continuous cloud video recording.
- Production-scale cloud infrastructure.
- Medical record management.
- Payment and insurance integrations.

## 9. Success Criteria

The MVP is considered functionally successful when:

- A simulated SOS event can be created.
- The event appears on the dashboard.
- A user can acknowledge the event.
- A caregiver can resolve it with a note.
- Event history records the workflow.
- Device disconnection can be represented.
- The system clearly distinguishes suspected incidents
  from verified incidents.

## 10. Product Limitations

AI-generated fall detection events are potential
incident signals, not medical diagnoses.

A successful demonstration using sample videos
does not establish real-world detection accuracy.

CARE LOOP is intended to support human care coordination,
not replace human supervision or emergency services.
