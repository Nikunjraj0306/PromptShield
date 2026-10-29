## System Architecture and Request Flow

PromptShield is designed as a modular monolithic application. The frontend, backend API, detection engine, risk engine, policy engine, and persistence layer are logically separated modules deployed as a small number of application services. Microservices are outside the initial MVP scope.

### Components

1. **Frontend:** React with TypeScript. Provides login, application configuration, security-event views, policy management, and analytics dashboards.
2. **Backend API:** Python with FastAPI. Handles authentication, authorization, input validation, request inspection, event retrieval, policy management, and analytics APIs.
3. **Detection engine:** Applies configurable rule-based checks for SQL injection patterns, cross-site scripting (XSS), path traversal, command-injection patterns, prompt-injection patterns, sensitive-data patterns, and rate-limit violations.
4. **Risk engine:** Calculates a bounded risk score from applicable findings and identifies whether any finding is critical.
5. **Policy engine:** Applies the configured decision rules and returns an Allow or Block decision.
6. **Persistence layer:** Azure SQL Database stores users, registered applications, endpoints, detection rules, security policies, security events, threat findings, and audit logs.
7. **Controlled demo target:** A deliberately limited test application used to demonstrate allowed and blocked requests. The MVP does not forward requests to arbitrary user-supplied URLs.
8. **Cloud security and monitoring:** HTTPS, managed secret storage, access controls, application logging, and Azure monitoring services protect and observe the deployment.

### Request-Processing Flow

1. The client submits a request to the PromptShield inspection API.
2. The backend validates the request structure, size, and permitted target.
3. The detection engine evaluates the request against enabled rules and rate limits.
4. The risk engine calculates the score and determines whether a critical finding exists.
5. The policy engine selects Allow or Block using the documented decision rules.
6. The event and associated findings are persisted as a consistent database transaction.
7. Only an allowed request for the registered controlled demo target may be forwarded.
8. The API returns a decision and correlation ID without exposing secrets or unnecessary sensitive evidence.
9. Authorized users retrieve events and aggregated analytics through the dashboard APIs.

### Failure Handling

PromptShield fails closed: if a required validation, detection, risk evaluation, policy evaluation, or event-persistence step fails, the request must not be forwarded. A suitable error response and correlation ID should be returned where possible. The system must not report an event as successfully stored if persistence failed.

### Deployment Boundaries

The browser communicates with the backend over HTTPS. The backend accesses Azure SQL through a restricted connection and uses securely managed credentials or managed identity where supported. Secrets must not be committed to source control. Production deployment must use restricted database networking, least-privilege permissions, and appropriate monitoring.

### Authentication and Authorization

Passwords are stored using a suitable salted password-hashing algorithm, never as plaintext. Successful login issues a signed, expiring access token. The backend validates tokens and enforces role permissions on every protected operation. Frontend-only role checks are not sufficient.