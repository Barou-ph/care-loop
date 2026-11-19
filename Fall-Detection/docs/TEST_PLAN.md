# CARE LOOP — TEST PLAN & QUALITY ASSURANCE

**Version:** 1.0  
**Date:** 19 November 2026  
**Testing Scope:** Backend, Event Engine, AI Integration, Database and Dashboard

---

## 1. Testing Objectives

The objective of this test plan is to evaluate whether CARE LOOP components work correctly individually and as an integrated system.

Testing must verify:

- Correct event generation.
- Correct event processing.
- Correct database persistence.
- Correct event lifecycle transitions.
- Correct notification workflow.
- Correct human response recording.
- Correct dashboard behavior.
- Reliable integration between AI and backend.
- Appropriate handling of failures.

A successful code compilation is not sufficient evidence that a feature works.

---

## 2. Testing Status Definitions

| Status     | Meaning                            |
| ---------- | ---------------------------------- |
| PASS       | Executed and verified successfully |
| PARTIAL    | Implemented but not fully verified |
| FAIL       | Executed and failed                |
| NOT TESTED | No execution evidence available    |

Every test report should include:

- Test ID.
- Test objective.
- Test environment.
- Input.
- Expected result.
- Actual result.
- Status.
- Evidence.
- Notes or limitations.

---

## 3. Testing Levels

### 3.1. Unit Testing

Tests individual functions and modules.

Examples:

- Event validation.
- Priority classification.
- Event state transitions.
- Duplicate event detection.
- Contact ordering.
- Audit record creation.

### 3.2. Integration Testing

Tests communication between modules.

Examples:

- AI Event Publisher to FastAPI.
- FastAPI to SQLite.
- Dashboard to API.
- Event Engine to Notification Service.

### 3.3. System Testing

Tests the complete workflow.

Example:

SOS → API → Database → Dashboard → Acknowledgement → Resolution.

### 3.4. Failure Testing

Tests behavior when components fail.

Examples:

- API unavailable.
- Database unavailable.
- Device offline.
- Notification provider failure.
- Invalid payload.
- Duplicate event.

### 3.5. User Acceptance Testing

Evaluates whether the system supports the expected user workflow.

Participants may include:

- Team members.
- Family representatives.
- Potential caregivers.
- Elderly user representatives, with appropriate safeguards.

---

## 4. Test Environment

### Development Environment

| Component            | Technology              |
| -------------------- | ----------------------- |
| Operating System     | Windows                 |
| Programming Language | Python                  |
| AI Framework         | Ultralytics YOLO        |
| Computer Vision      | OpenCV                  |
| Backend              | FastAPI                 |
| Server               | Uvicorn                 |
| Database             | SQLite                  |
| Frontend             | HTML / CSS / JavaScript |
| Testing              | Pytest                  |

Actual dependency versions should be recorded from the repository's requirements and environment.

---

## 5. Backend Tests

| Test ID | Test Case                | Expected Result                                 |
| ------- | ------------------------ | ----------------------------------------------- |
| BE-01   | Start FastAPI server     | Server starts                                   |
| BE-02   | GET /health              | Returns successful health response              |
| BE-03   | POST valid event         | Event accepted                                  |
| BE-04   | POST invalid event       | Validation error                                |
| BE-05   | GET event list           | Returns stored events                           |
| BE-06   | GET event details        | Correct event returned                          |
| BE-07   | Acknowledge event        | Status updated                                  |
| BE-08   | Resolve event            | Resolution stored                               |
| BE-09   | Mark false alarm         | Classification stored                           |
| BE-10   | Get audit history        | Relevant actions returned                       |
| BE-11   | Access nonexistent event | 404 response                                    |
| BE-12   | Unauthorized request     | Access rejected where authentication is enabled |

---

## 6. Database Tests

| Test ID | Test Case           | Expected Result                                             |
| ------- | ------------------- | ----------------------------------------------------------- |
| DB-01   | Create event        | Record persisted                                            |
| DB-02   | Retrieve event      | Correct data returned                                       |
| DB-03   | Update event        | Updated state persisted                                     |
| DB-04   | Create audit record | Audit entry persisted                                       |
| DB-05   | Restart backend     | Existing records remain                                     |
| DB-06   | Query event history | Correct history returned                                    |
| DB-07   | Invalid foreign key | Invalid reference rejected where constraints are configured |
| DB-08   | Concurrent update   | No inconsistent state                                       |

---

## 7. Event Engine Tests

| Test ID | Test Case                  | Expected Result                                |
| ------- | -------------------------- | ---------------------------------------------- |
| EV-01   | Receive SOS event          | New event created                              |
| EV-02   | Receive suspected fall     | Correct event type assigned                    |
| EV-03   | Assign priority            | Valid P0–P4 value                              |
| EV-04   | Acknowledge event          | ACKNOWLEDGED                                   |
| EV-05   | Begin verification         | VERIFYING                                      |
| EV-06   | Start assistance           | IN_PROGRESS                                    |
| EV-07   | Resolve event              | RESOLVED                                       |
| EV-08   | Mark false alarm           | FALSE_ALARM                                    |
| EV-09   | Invalid transition         | Rejected                                       |
| EV-10   | Duplicate event submission | Duplicate handled safely                       |
| EV-11   | Missing acknowledgement    | Escalation workflow triggered when implemented |
| EV-12   | Backup contact responds    | Acknowledgement recorded                       |

---

## 8. AI Fall Detection Tests

These tests evaluate the technical fall-detection prototype, not clinical safety.

### 8.1. Detection Scenarios

| Test ID | Scenario                       | Expected Behavior                     |
| ------- | ------------------------------ | ------------------------------------- |
| AI-01   | Person standing                | No fall alert                         |
| AI-02   | Person walking                 | No fall alert                         |
| AI-03   | Person sitting                 | No fall alert                         |
| AI-04   | Person bending                 | No fall alert under normal conditions |
| AI-05   | Person lying down slowly       | Avoid unnecessary alert               |
| AI-06   | Person falling forward         | Detect according to model capability  |
| AI-07   | Person falling sideways        | Detect according to model capability  |
| AI-08   | Person falling backward        | Detect according to model capability  |
| AI-09   | Person obscured during descent | Evaluate occlusion handling           |
| AI-10   | Person stands up after falling | Recovery state handled                |
| AI-11   | Multiple people fall           | Evaluate each track independently     |
| AI-12   | Different video files          | Tracking context reset appropriately  |

### 8.2. Multi-Person Tracking

Important evaluation metrics:

- Number of actual people in video.
- Number of detected people.
- Number of correctly tracked people.
- Missed detections.
- ID switches.
- Track fragmentation.
- False person tracks.
- Fall events assigned to the wrong track.

A track ID must be scoped to a detection session.

The same track number appearing in two separate video files does not indicate the same person.

### 8.3. Fall Detection Metrics

| Metric              | Description                                         |
| ------------------- | --------------------------------------------------- |
| Precision           | Proportion of predicted falls that are actual falls |
| Recall              | Proportion of actual falls detected                 |
| F1-score            | Harmonic mean of precision and recall               |
| False Positive Rate | Proportion of non-fall cases incorrectly flagged    |
| Detection Latency   | Time from fall onset to alert                       |
| ID Switches         | Number of identity changes during tracking          |

Use labeled test videos and a consistent evaluation protocol.

Do not report performance claims without recorded test evidence.

---

## 9. Integration Tests

| Test ID | Integration                       | Expected Result          |
| ------- | --------------------------------- | ------------------------ |
| IT-01   | AI → Publisher                    | Event generated          |
| IT-02   | Publisher → API                   | Event submitted          |
| IT-03   | API → Database                    | Event persisted          |
| IT-04   | Database → API                    | Event retrieved          |
| IT-05   | API → Dashboard                   | Event displayed          |
| IT-06   | Dashboard → API                   | Acknowledgement recorded |
| IT-07   | Dashboard → API                   | Resolution recorded      |
| IT-08   | API → Audit                       | Action recorded          |
| IT-09   | Publisher → API unavailable       | Failure recorded         |
| IT-10   | Publisher → API duplicate request | Duplicate handled safely |

---

## 10. Dashboard Tests

| Test ID | Test Case           | Expected Result           |
| ------- | ------------------- | ------------------------- |
| UI-01   | Open dashboard      | Interface loads           |
| UI-02   | Display event list  | Correct events displayed  |
| UI-03   | Open event details  | Correct details displayed |
| UI-04   | Acknowledge event   | Updated status displayed  |
| UI-05   | Resolve event       | Event marked resolved     |
| UI-06   | False alarm action  | Classification updated    |
| UI-07   | Refresh page        | Persisted data remains    |
| UI-08   | Backend unavailable | Error state shown         |
| UI-09   | Empty event list    | Empty state shown         |
| UI-10   | Multiple events     | Correct records displayed |

---

## 11. Security Tests

| Test ID | Test Case                                     | Expected Result                          |
| ------- | --------------------------------------------- | ---------------------------------------- |
| SEC-01  | Access protected endpoint without credentials | Rejected where required                  |
| SEC-02  | Submit invalid payload                        | Rejected                                 |
| SEC-03  | Access unauthorized profile                   | Rejected                                 |
| SEC-04  | Attempt unauthorized state change             | Rejected                                 |
| SEC-05  | Check Git repository for secrets              | No active secrets committed              |
| SEC-06  | Check sensitive logs                          | No unnecessary personal data             |
| SEC-07  | Check video storage behavior                  | Matches configured consent and retention |
| SEC-08  | Review audit integrity                        | Actions traceable                        |

---

## 12. Performance Tests

Measure:

- API response latency.
- Event ingestion latency.
- Database query latency.
- Dashboard refresh time.
- AI inference FPS.
- CPU and memory usage.
- Publisher delivery latency.

Recommended measurements:

| Metric                  | Measurement Method                |
| ----------------------- | --------------------------------- |
| API latency             | Request timing                    |
| Event ingestion         | Source timestamp to persistence   |
| Acknowledgement latency | Event creation to acknowledgement |
| Inference speed         | Frames per second                 |
| CPU usage               | Process monitoring                |
| Memory usage            | Process monitoring                |

Performance targets must be established after measuring the actual development environment.

---

## 13. End-to-End Acceptance Scenario

### Test Case: SOS to Resolution

**Preconditions:**

- Backend is running.
- Database is available.
- A test profile exists.
- A designated contact exists.
- Dashboard is accessible.

**Execution:**

1. Generate an SOS event.
2. Verify API response.
3. Check database persistence.
4. Open caregiver dashboard.
5. Verify event visibility.
6. Acknowledge event.
7. Verify status update.
8. Record human verification.
9. Resolve event.
10. Retrieve audit history.

**Expected outcome:**

The complete event lifecycle is recorded and can be retrieved after refreshing the dashboard and restarting the backend.

### Test Case: Missing Acknowledgement

1. Generate an SOS event.
2. Do not acknowledge it.
3. Simulate the configured timeout.
4. Verify escalation to the next contact.
5. Record escalation history.
6. Verify final event state.

The test may use simulated contacts and notifications.

---

## 14. Test Report Template

| Field           | Value                              |
| --------------- | ---------------------------------- |
| Test ID         |                                    |
| Test Name       |                                    |
| Date            |                                    |
| Environment     |                                    |
| Preconditions   |                                    |
| Test Input      |                                    |
| Expected Result |                                    |
| Actual Result   |                                    |
| Status          | PASS / PARTIAL / FAIL / NOT TESTED |
| Evidence        |                                    |
| Tester          |                                    |
| Notes           |                                    |

---

## 15. Release Readiness Checklist

### Core Backend

- [ ] API starts successfully.
- [ ] Health endpoint works.
- [ ] Event creation works.
- [ ] Event persistence works.
- [ ] Event retrieval works.
- [ ] Acknowledgement works.
- [ ] Resolution works.
- [ ] Audit history works.

### AI Integration

- [ ] Model loads successfully.
- [ ] Video inference works.
- [ ] Fall alert can be generated.
- [ ] Event Publisher submits a valid event.
- [ ] Backend receives AI event.
- [ ] Duplicate event behavior is verified.
- [ ] Multiple video session behavior is verified.

### Dashboard

- [ ] Dashboard loads.
- [ ] Events appear.
- [ ] Status updates work.
- [ ] Resolution works.
- [ ] History is available.

### Security and Reliability

- [ ] Secrets are not committed.
- [ ] Access restrictions are reviewed.
- [ ] Failure scenarios are tested.
- [ ] Backup and recovery are documented.
- [ ] Limitations are disclosed.

---

## 16. Final Acceptance

A successful demonstration must prove the complete event coordination workflow.

The project should not be marked production-ready solely because all local prototype tests pass.

Production readiness additionally requires:

- Real household pilot testing.
- Security assessment.
- Privacy assessment.
- Device reliability testing.
- Notification provider integration.
- Defined human response operations.
- Appropriate legal and operational review.

\*\*Quality principle: Every PASS must have evidence. Every limitation must be disclosed. Every untested capability must remain NOT
