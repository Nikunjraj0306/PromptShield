# PromptShield — Security Threat Model

## 1. Introduction

Threat modelling is the process of identifying potential security threats, evaluating risks and determining suitable security controls.

PromptShield uses threat modelling to identify risks affecting its users, application interfaces, backend services and database.

The project focuses on selected application-layer threats and the security of its cloud-hosted architecture.

## 2. Assets to Protect

The main assets in PromptShield are:

| Asset | Description |
|---|---|
| User credentials | Email addresses and password hashes |
| JWT signing secret | Used to sign authentication tokens |
| Authentication tokens | Used to access protected API endpoints |
| Application configuration | Registered applications and endpoints |
| Detection rules | Security detection configurations |
| Security policies | Risk thresholds and decision settings |
| Security events | Stored request-inspection results |
| Threat findings | Records of detected suspicious patterns |
| Database credentials | Used by the backend to access Azure SQL |
| Audit records | Records of application-related activity |

## 3. Potential Threat Actors

Potential threat actors include:

1. Unauthenticated attackers attempting to access protected APIs.
2. Malicious users submitting suspicious request content.
3. Authenticated users attempting to access unauthorized functionality.
4. Attackers attempting to exploit exposed credentials or insecure configuration.
5. Attackers attempting to access the cloud-hosted database without authorization.

## 4. Threat Identification and Mitigation

### 4.1 SQL Injection

**Threat:** Malicious input may contain SQL injection patterns intended to manipulate database queries.

**Potential impact:** Unauthorized data access or database manipulation in a vulnerable application.

**Implemented control:** PromptShield includes rule-based SQL injection pattern detection and risk evaluation.

**Limitation:** Pattern-based detection cannot identify every SQL injection technique. The application does not claim to provide comprehensive SQL injection prevention for arbitrary external applications.

### 4.2 Cross-Site Scripting (XSS)

**Threat:** Malicious scripts may be submitted through application input.

**Potential impact:** Script execution in a vulnerable web application.

**Implemented control:** The detection engine checks submitted content for selected XSS patterns and generates security findings.

**Limitation:** Detection is based on predefined patterns and does not guarantee identification of all XSS variants.

### 4.3 Path Traversal

**Threat:** An attacker may submit directory traversal patterns to attempt access to restricted files.

**Potential impact:** Unauthorized file access in a vulnerable target application.

**Implemented control:** PromptShield detects selected path traversal patterns and evaluates their associated risk.

**Limitation:** The current inspection prototype does not automatically intercept file-access operations in external applications.

### 4.4 Command Injection

**Threat:** Malicious input may contain operating-system command patterns.

**Potential impact:** Execution of unauthorized commands by a vulnerable application.

**Implemented control:** The detection engine identifies selected command-injection patterns and can generate critical findings that cause requests to be blocked.

**Limitation:** The rule-based mechanism is not a complete command-injection prevention system.

### 4.5 Prompt Injection

**Threat:** Malicious instructions may be included in submitted text to manipulate an AI-based system.

**Potential impact:** Unauthorized or unintended behavior in an AI application.

**Implemented control:** PromptShield includes rule-based prompt-injection pattern detection.

**Limitation:** The current implementation does not understand all contextual or semantic forms of prompt injection.

### 4.6 Sensitive Data Exposure

**Threat:** Submitted content may contain sensitive information.

**Potential impact:** Exposure of personal or confidential information.

**Implemented control:** The detection engine checks for selected sensitive-data patterns and records relevant findings.

**Limitation:** Pattern-based checks cannot guarantee identification of every sensitive-data format.

### 4.7 Unauthorized API Access

**Threat:** An attacker may attempt to access protected API endpoints without valid authentication.

**Potential impact:** Unauthorized access to application functionality or stored information.

**Implemented controls:**

- Password hashing.
- JWT-based authentication.
- Token expiration.
- Backend authorization checks.
- Role-based access control.

**Limitation:** Security still depends on correct secret management, token handling and implementation of access checks across protected endpoints.

### 4.8 Brute-Force Login Attempts

**Threat:** An attacker may repeatedly attempt to guess user credentials.

**Potential impact:** Unauthorized account access.

**Implemented control:** Login-attempt rate limiting restricts repeated attempts based on client IP address and normalized email address.

**Limitation:** The current implementation uses in-memory storage and is not shared across multiple backend instances.

### 4.9 Database Unauthorized Access

**Threat:** An attacker may attempt to access the Azure SQL Database directly or through exposed credentials.

**Potential impact:** Unauthorized access, modification or deletion of stored information.

**Implemented controls:**

- Database credentials stored in backend environment variables.
- Azure SQL firewall restrictions.
- Backend-mediated database access.
- Encrypted database connection configuration.

**Limitation:** The current Render Free deployment uses an observed outbound IP address rather than a guaranteed permanent outbound IP. Firewall configuration may need updating if that address changes.

### 4.10 Cross-Origin Resource Sharing Misconfiguration

**Threat:** Incorrect CORS configuration may permit unintended browser-based cross-origin requests.

**Potential impact:** Unintended access from unauthorized browser origins.

**Implemented control:** The backend configures allowed frontend origins through its CORS settings.

**Limitation:** CORS is not a replacement for authentication, authorization or API-level access control.

### 4.11 Secret Exposure

**Threat:** Database credentials or JWT signing secrets may be exposed through source code, logs or public repositories.

**Potential impact:** Unauthorized database access or token forgery.

**Implemented controls:**

- Environment-based configuration.
- Exclusion of local environment files from version control.
- Separation of example configuration from actual credentials.

**Limitation:** Deployment secrets must continue to be protected and rotated when exposure is suspected.

## 5. Risk Assessment

The following table summarizes the major threats.

| Threat | Potential impact | Implemented mitigation |
|---|---|---|
| SQL Injection | High | Pattern-based detection |
| XSS | High | Pattern-based detection |
| Path Traversal | High | Pattern-based detection |
| Command Injection | Critical | Detection and critical-finding block |
| Prompt Injection | Medium to High | Pattern-based detection |
| Sensitive Data Exposure | High | Pattern-based detection |
| Unauthorized API access | High | JWT and RBAC |
| Brute-force login | High | Login-attempt rate limiting |
| Database unauthorized access | Critical | Credentials and firewall restrictions |
| CORS misconfiguration | Medium | Allowed-origin configuration |
| Secret exposure | Critical | Environment-based secret management |

These ratings are qualitative project assessments, not results from a formal quantitative risk assessment.

## 6. Security Decision Mechanism

PromptShield uses a risk-based inspection mechanism.

Each detection rule has an associated weight and severity.

The system calculates an overall risk score capped at 100.

The decision logic is:

1. Identify matching detection rules.
2. Generate security findings.
3. Calculate the combined risk score.
4. Check whether a critical finding exists.
5. Compare the risk score with the configured policy threshold.
6. Block the request if a critical finding exists or the threshold is reached.
7. Otherwise, allow the request.

The default risk threshold is 50.

## 7. Security Controls Summary

The following security controls are implemented in the current MVP:

- Password hashing.
- JWT-based authentication.
- Role-based authorization.
- Login-attempt rate limiting.
- CORS allowed-origin restrictions.
- Environment-based secret configuration.
- Azure SQL firewall restrictions.
- Encrypted database connectivity.
- Rule-based threat detection.
- Risk-based Allow/Block decisions.
- Security-event and finding storage.

## 8. Residual Risks and Limitations

Despite the implemented controls, some risks remain:

1. Rule-based detection can produce false positives and false negatives.
2. The system does not automatically intercept all external application traffic.
3. The application is not a complete reverse-proxy-based Web Application Firewall.
4. Login rate limiting is not distributed.
5. Render Free does not guarantee a fixed outbound IP.
6. Dedicated centralized security monitoring is not implemented.
7. The application has not been demonstrated to protect against every possible attack technique.

## 9. Future Security Improvements

Potential future improvements include:

- More advanced detection techniques.
- Distributed rate limiting.
- Stable cloud networking.
- Automated reverse-proxy traffic interception.
- Centralized security monitoring.
- Additional penetration testing.
- Enhanced authentication protections.
- Improved security policy management.

## 10. Conclusion

The PromptShield threat model identifies important security risks affecting the application, its users, API endpoints and database.

It documents the security controls implemented in the current MVP and identifies limitations that require further development.

This threat model demonstrates the practical application of threat identification, risk assessment and security-control selection in a cloud-hosted application.