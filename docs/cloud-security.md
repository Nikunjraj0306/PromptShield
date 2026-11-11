# PromptShield — Cloud Security Documentation

## 1. Introduction

Cloud Security refers to the technologies, policies and practices used to protect cloud-hosted applications, infrastructure, networks and data.

PromptShield demonstrates cloud security concepts through a distributed deployment architecture consisting of a React frontend, FastAPI backend and Microsoft Azure SQL Database.

The application incorporates authentication, authorization, request inspection, security-event monitoring, environment-based configuration and database firewall restrictions.

## 2. Cloud Deployment Architecture

PromptShield uses three cloud services:

| Component | Cloud platform | Purpose |
|---|---|---|
| Frontend | Vercel | Hosts the React and TypeScript dashboard |
| Backend | Render | Hosts the Python FastAPI application |
| Database | Microsoft Azure SQL Database | Stores application and security information |

### Communication Flow

1. The user accesses the frontend through a web browser.
2. The frontend communicates with the backend using HTTPS API requests.
3. The backend authenticates and authorizes the user.
4. The backend processes inspection requests using the detection engine.
5. The backend communicates with Azure SQL Database.
6. The inspection results and security events are returned to the frontend.

## 3. Authentication and Identity Security

PromptShield uses application-managed authentication.

The authentication mechanism includes:

- Email and password-based login.
- Password hashing instead of plaintext password storage.
- JWT-based access tokens.
- Token expiration.
- Authentication checks for protected API endpoints.

JWT tokens allow the backend to verify the identity and authentication status of users when they access protected resources.

## 4. Role-Based Access Control

Role-Based Access Control (RBAC) restricts application functionality according to assigned user roles.

PromptShield implements three roles:

| Role | Permissions |
|---|---|
| Admin | Administrative access |
| Analyst | Request inspection, analytics and security events |
| Viewer | Read-only dashboard and security-event access |

Authorization is enforced by the backend rather than relying exclusively on frontend navigation restrictions.

This helps prevent unauthorized access to protected application operations.

## 5. Application-Layer Threat Detection

PromptShield uses rule-based detection to identify selected suspicious request patterns.

The implemented detection categories include:

1. SQL Injection
2. Cross-Site Scripting (XSS)
3. Path Traversal
4. Command Injection
5. Prompt Injection
6. Sensitive Data Exposure

The detection engine produces findings with associated severity levels and risk weights.

The risk evaluation mechanism calculates a score capped at 100.

A request is blocked if a critical finding is identified or the configured risk threshold is reached. Otherwise, it is allowed.

This provides a practical demonstration of application-layer security monitoring and risk-based decision-making.

## 6. Network Security and CORS

Cross-Origin Resource Sharing (CORS) is configured in the backend to permit communication from approved frontend origins.

Only the configured frontend domains should be allowed to make browser-based cross-origin requests to the API.

The application uses HTTPS for communication between the browser and deployed application services.

CORS is a browser access-control mechanism and should not be considered a replacement for API authentication or authorization.

## 7. Database Security

PromptShield uses Microsoft Azure SQL Database for persistent storage.

Database security measures include:

- Database credentials stored as backend environment variables.
- Database access through the backend rather than direct frontend connections.
- Azure SQL firewall restrictions.
- Database authentication.
- Encrypted connection configuration using Microsoft ODBC Driver 18.
- Separation of application configuration and source code.

The database firewall permits connections from configured network addresses.

The current Render Free deployment uses an observed outbound IP address added to the Azure SQL firewall. Render Free does not guarantee a permanent outbound IP address, so firewall configuration may need to be updated if that address changes.

## 8. Secret and Configuration Management

Sensitive configuration values are maintained through environment variables rather than being hardcoded into application source files.

Examples include:

- Azure SQL server name.
- Azure SQL database name.
- Azure SQL username.
- Azure SQL password.
- JWT signing secret.
- Application environment configuration.
- CORS allowed origins.

Example configuration files may contain placeholder values, but actual credentials must never be committed to a public GitHub repository or included in the final submission archive.

## 9. Login Rate Limiting

PromptShield implements login-attempt rate limiting to reduce repeated authentication attempts.

The current mechanism limits repeated login attempts based on client IP address and normalized email address.

The implementation uses in-memory storage. Therefore, the rate-limit state is not shared across multiple backend instances and may reset when the application restarts.

This is an application-level protective measure rather than a distributed rate-limiting solution.

## 10. Security Event Monitoring

PromptShield records inspection results and associated security findings.

Authorized users can access the Security Events interface to review recorded activity.

This provides visibility into detected threats, risk scores and Allow or Block decisions.

The current MVP does not include a dedicated centralized cloud monitoring or SIEM integration.

## 11. Security Testing

The application was tested using representative security-related inputs.

| Security test | Expected behavior |
|---|---|
| Normal input | ALLOW |
| SQL injection pattern | Detect suspicious input |
| XSS pattern | Detect suspicious input |
| Path traversal pattern | Detect suspicious input |
| Prompt injection pattern | Detect suspicious input |
| Command injection pattern | BLOCK when critical finding is generated |
| Combined attack patterns | High risk score and BLOCK |

The automated backend test suite also includes regression testing for command-injection detection.

## 12. Security Limitations

PromptShield is an academic security prototype and has the following limitations:

- Rule-based detection may produce false positives and false negatives.
- The application does not automatically intercept all traffic to external web applications.
- It is not a complete reverse-proxy-based Web Application Firewall.
- Login rate limiting is in-memory and not distributed.
- Render Free does not provide a guaranteed permanent outbound IP address.
- The system does not provide comprehensive protection against every application-layer attack.
- Dedicated centralized cloud monitoring and alerting are not implemented.

## 13. Future Security Enhancements

Possible future improvements include:

1. Stable outbound networking for the backend.
2. Distributed rate limiting.
3. Advanced threat-detection techniques.
4. Automatic traffic interception through a reverse proxy.
5. Centralized security monitoring and alerting.
6. Additional authentication protections.
7. More extensive penetration testing and security validation.
8. Improved security policies and administrative controls.

## 14. Conclusion

PromptShield demonstrates several important Cloud Security concepts, including cloud deployment, authentication, authorization, CORS, database firewall restrictions, environment-based secret management and application-layer threat detection.

The project provides practical experience in securing communication between cloud-hosted application components and protecting application data through controlled database access.

It serves as an academic prototype for understanding cloud application security and its practical implementation.