# PromptShield — System Architecture and Design

## 1. Introduction

PromptShield is a cloud-native application security gateway prototype designed using a modular monolithic architecture.

The application follows a three-tier structure consisting of:

1. Presentation Layer
2. Application Layer
3. Data Layer

These layers are logically separated and communicate through defined interfaces and REST APIs.

The system is designed to inspect submitted request content, identify suspicious patterns, calculate security risk scores, make Allow or Block decisions, and store inspection results.

## 2. Architectural Style

PromptShield follows a modular monolithic architecture.

The backend is developed as a single FastAPI application, with separate modules responsible for authentication, authorization, request inspection, detection, risk evaluation, analytics, and database operations.

This approach provides modularity and easier maintenance without introducing the operational complexity of microservices.

## 3. High-Level System Architecture

The architecture consists of three main layers.

### 3.1 Presentation Layer

**Technology:** React and TypeScript  
**Hosting:** Vercel

Responsibilities:

- Display the login interface.
- Provide authenticated dashboard access.
- Allow authorized users to inspect request content.
- Display inspection decisions and risk scores.
- Display security events and analytics.
- Provide user-specific interface permissions.

### 3.2 Application Layer

**Technology:** Python and FastAPI  
**Hosting:** Render

Responsibilities:

- Handle HTTP requests through REST APIs.
- Authenticate users and validate JWT tokens.
- Enforce role-based access control.
- Validate inspection requests.
- Apply rule-based threat detection.
- Calculate risk scores.
- Determine Allow or Block decisions.
- Store inspection events and findings.
- Provide analytics and security-event APIs.
- Apply login-attempt rate limiting.

### 3.3 Data Layer

**Technology:** Microsoft Azure SQL Database

Responsibilities:

- Store user account information.
- Store registered application and endpoint information.
- Store detection rules and security policies.
- Store security events and threat findings.
- Maintain audit-related records.
- Provide persistent storage for application operations.

## 4. Main System Components

### 4.1 Authentication Module

The authentication module verifies user credentials and issues signed JWT access tokens after successful login.

Passwords are stored as password hashes rather than plaintext.

The access token has a configured expiration time. Protected API endpoints require valid authentication.

### 4.2 Authorization Module

PromptShield implements role-based access control using three roles:

| Role | Access |
|---|---|
| Admin | Administrative access and authorized application operations |
| Analyst | Request inspection, analytics and security events |
| Viewer | Read-only analytics and security-event access |

The backend validates permissions, so access is not dependent only on frontend interface restrictions.

### 4.3 Request Inspection Module

The inspection module receives a request containing the application ID, endpoint ID and text to analyze.

It verifies that the registered application and endpoint are valid and active before processing the submitted content.

### 4.4 Detection Engine

The detection engine applies predefined rule-based checks for selected security threats:

- SQL Injection
- Cross-Site Scripting (XSS)
- Path Traversal
- Command Injection
- Prompt Injection
- Sensitive Data Exposure

The engine identifies matching patterns and produces security findings with associated severity and risk weights.

### 4.5 Risk Evaluation and Decision Logic

Each detection rule has an associated risk weight.

The overall risk score is calculated from applicable findings and capped at 100.

The decision logic follows these conditions:

- If a critical finding exists, the request is blocked.
- If the risk score reaches or exceeds the configured policy threshold, the request is blocked.
- Otherwise, the request is allowed.

The default policy threshold is 50.

### 4.6 Security Event Management

Inspection results and associated findings are stored in Azure SQL Database.

Authorized users can retrieve recent security events through the dashboard.

### 4.7 Analytics Module

The analytics module retrieves stored security information and provides summary information for the dashboard.

## 5. Request Processing Flow

The request-inspection process follows these steps:

1. An authorized user submits request content through the React dashboard.
2. The frontend sends an authenticated API request to the FastAPI backend.
3. The backend validates the user's JWT token and role.
4. The inspection service validates the application and endpoint.
5. The detection engine evaluates the submitted text against enabled detection rules.
6. Matching security findings are generated.
7. The risk evaluation logic calculates the overall risk score.
8. The decision logic determines whether the request should be allowed or blocked.
9. The inspection result and related findings are stored in Azure SQL Database.
10. The backend returns the inspection result to the frontend.
11. The dashboard displays the decision, risk score and detected findings.

**Note:** The current MVP evaluates submitted request content and records inspection decisions. It does not automatically intercept all application traffic or forward requests to arbitrary external destinations.

## 6. Database Design Integration

Azure SQL Database provides persistent storage for the application.

The database contains eight main entities:

1. Users
2. Applications
3. Endpoints
4. DetectionRules
5. SecurityPolicies
6. SecurityEvents
7. ThreatFindings
8. AuditLogs

Primary keys uniquely identify records, while foreign keys maintain relationships between related entities.

The detailed entity relationships are documented in `er-diagram.md`.

## 7. API Design

The backend exposes REST API endpoints.

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Check backend health |
| `/health/ready` | GET | Check database readiness |
| `/api/v1/auth/login` | POST | Authenticate a user |
| `/api/v1/auth/me` | GET | Retrieve current user profile |
| `/api/v1/inspect` | POST | Inspect submitted request content |
| `/api/v1/analytics/summary` | GET | Retrieve dashboard analytics |
| `/api/v1/events` | GET | Retrieve recent security events |

Protected endpoints use JWT authentication and role-based authorization.

## 8. Cloud Deployment Architecture

PromptShield is deployed using three cloud services.

| Layer | Platform | Responsibility |
|---|---|---|
| Frontend | Vercel | Hosts React application |
| Backend | Render | Hosts FastAPI application |
| Database | Microsoft Azure SQL Database | Persistent relational storage |

Communication between the browser and backend uses HTTPS.

The backend connects to Azure SQL Database using environment-based database configuration. Database firewall rules restrict access to permitted network addresses.

## 9. Security Design Considerations

The system incorporates the following security measures:

- Password hashing.
- JWT-based authentication.
- Role-based authorization.
- Login-attempt rate limiting.
- CORS origin restrictions.
- Environment-based secret configuration.
- Azure SQL firewall restrictions.
- Validation of inspection requests.
- Security-event recording.

These controls improve the security of the prototype but do not guarantee protection against every attack.

## 10. Architecture Limitations and Future Improvements

The current implementation is an academic MVP.

Possible future improvements include:

- Reverse-proxy-based automatic traffic interception.
- Integration with real application traffic.
- More advanced threat-detection techniques.
- Distributed rate limiting.
- Stable outbound networking for cloud database access.
- Centralized monitoring and alerting.
- Improved policy-management capabilities.
- Additional security testing and performance optimization.

## 11. Conclusion

PromptShield demonstrates a modular, three-tier cloud application architecture integrating frontend development, REST API design, application security, authentication, database persistence and cloud deployment.

The architecture provides a foundation for extending the prototype into a more comprehensive application security gateway in future development.