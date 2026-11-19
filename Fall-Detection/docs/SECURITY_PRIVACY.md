# CARE LOOP — SECURITY & PRIVACY DESIGN

**Version:** 1.0  
**Date:** 19 November 2026  
**Scope:** Platform, Household Devices, Personal Data and Event Processing

---

## 1. Security Objectives

CARE LOOP processes information related to elderly people, household environments, emergency contacts, and safety events.

The security design aims to protect:

1. Confidentiality of personal information.
2. Integrity of event records.
3. Availability of essential platform functions.
4. Accountability of users and system operations.
5. Privacy and autonomy of elderly users.

Security must be considered across the complete ecosystem, not only the backend API.

---

## 2. Data Classification

| Classification   | Examples                                          | Protection                                             |
| ---------------- | ------------------------------------------------- | ------------------------------------------------------ |
| Public           | General product documentation                     | Public access                                          |
| Internal         | System architecture and operational configuration | Authorized team access                                 |
| Personal         | Name, phone, address                              | Access control and encryption                          |
| Sensitive        | Care notes, household monitoring metadata         | Strict access control                                  |
| Highly sensitive | Video footage and detailed household activity     | Separate consent, restricted access, minimal retention |
| Security secrets | API keys, tokens, credentials                     | Secret storage, rotation, never commit                 |

---

## 3. Privacy by Design

### 3.1. Data Minimization

Collect only information required to provide the requested service.

Examples:

- Store event metadata rather than continuous video.
- Store a room-zone label rather than precise coordinates when sufficient.
- Do not collect health information unless there is a defined purpose.
- Avoid storing unnecessary personal details in event descriptions.

### 3.2. Purpose Limitation

Every data category must have a defined purpose.

Examples:

| Data                | Purpose                  |
| ------------------- | ------------------------ |
| Phone number        | Emergency contact        |
| Device ID           | Device identification    |
| Event timestamp     | Incident tracking        |
| Fall alert metadata | Human verification       |
| Video clip          | Optional incident review |
| Audit log           | Accountability           |

Data collected for one purpose must not automatically be reused for another purpose.

### 3.3. Camera Privacy

Camera deployment requires particular care.

Recommended policy:

- Camera is optional.
- Obtain appropriate consent before activation.
- Define the monitored area.
- Avoid private spaces such as bathrooms and bedrooms.
- Prefer edge inference.
- Do not transmit continuous video by default.
- Do not enable face recognition.
- Apply explicit retention and deletion policies to recorded clips.
- Provide a clear process to disable or remove the device.

### 3.4. Elderly User Autonomy

The elderly person must remain central to decisions about household monitoring.

Payment by a family member does not automatically grant access to every category of personal information.

Consent should be meaningful, understandable, and revocable where applicable.

Where a representative is involved, the basis and scope of their authority must be appropriately established.

---

## 4. Consent Management

Consent should be separated by purpose.

Proposed consent categories:

| Consent ID | Purpose                                              |
| ---------- | ---------------------------------------------------- |
| C-01       | Create and maintain Care Profile                     |
| C-02       | Share emergency contact information                  |
| C-03       | Receive safety notifications                         |
| C-04       | Use household sensor metadata                        |
| C-05       | Activate camera-based monitoring                     |
| C-06       | Store incident-related video                         |
| C-07       | Share information with designated external providers |

Each consent record should contain:

- User identifier.
- Related profile.
- Purpose.
- Consent state.
- Policy version.
- Timestamp.
- Withdrawal timestamp when applicable.

A withdrawal of consent should trigger the corresponding operational process, including disabling the relevant data collection where required.

---

## 5. Authentication

### 5.1. Account Authentication

Future production deployment should use an established authentication mechanism.

Requirements:

- Secure password handling if passwords are supported.
- Session expiration.
- Secure token storage.
- Account recovery.
- Multi-factor authentication for privileged roles where appropriate.

### 5.2. Device Authentication

Each registered device should have a unique identity.

Requirements:

- No default shared device passwords.
- Secure provisioning.
- Device credential rotation.
- Revocation of compromised devices.
- Verification of device identity.

### 5.3. Service Authentication

AI Event Publisher and backend communication should use dedicated service credentials.

Development API keys must not be exposed in frontend source code or committed to Git.

---

## 6. Authorization and RBAC

Proposed role model:

| Role        | Access                                     |
| ----------- | ------------------------------------------ |
| ELDERLY     | Own permitted profile and consent settings |
| FAMILY      | Authorized household and event information |
| CAREGIVER   | Assigned care tasks and permitted events   |
| COORDINATOR | Assigned event coordination                |
| ADMIN       | Technical administration                   |

Authorization must be enforced on the server.

The dashboard must not be trusted to hide information as the only access-control mechanism.

### 6.1. Permission Examples

| Action            | Elderly                         | Family                 | Caregiver   | Coordinator | Admin                  |
| ----------------- | ------------------------------- | ---------------------- | ----------- | ----------- | ---------------------- |
| View own profile  | Yes                             | If authorized          | If assigned | If assigned | Technical scope        |
| View event        | If permitted                    | If authorized          | If assigned | If assigned | Technical scope        |
| Acknowledge event | Configurable                    | Yes                    | Yes         | Yes         | Not automatic          |
| Resolve event     | Configurable                    | Yes                    | Yes         | Yes         | Not automatic          |
| Change consent    | Yes / authorized representative | No automatic authority | No          | No          | No automatic authority |
| Manage system     | No                              | No                     | No          | Limited     | Yes                    |

The final permission matrix requires legal and operational review.

---

## 7. API Security

Required controls:

- Input validation.
- Authentication.
- Server-side authorization.
- Rate limiting.
- Secure error handling.
- Request size limits.
- TLS for external communication.
- Secret management.
- Security logging.
- Protection against replay and duplicate submissions.

The current shared API key is suitable only
