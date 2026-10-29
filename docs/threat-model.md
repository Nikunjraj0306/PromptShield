## Assets and Security Objectives

The main assets are user credentials, access tokens and signing secrets, registered application configuration, security policies, inspected request data, security events, threat findings, audit logs, and database credentials.

Security objectives are confidentiality, integrity, availability, authenticated access, correct enforcement of policy decisions, and trustworthy audit records.

## Trust Boundaries

- The user's browser is untrusted.
- The public API boundary receives untrusted request data.
- Backend modules process and evaluate requests.
- Azure SQL stores persistent application and security data.
- Cloud configuration and secret storage form a privileged administrative boundary.
- The controlled demo target is a separate request destination with a restricted interface.

Data crossing a trust boundary must be validated and protected. The backend, not the frontend, is authoritative for access and policy decisions.

## Threat Scenarios and Mitigations

| Threat | Mitigation | Verification |
|---|---|---|
| Unauthorized access or privilege escalation | Validate access tokens and enforce roles on every protected endpoint | Attempt restricted actions using each role |
| Brute-force login | Apply login rate limits and safe authentication errors | Repeatedly submit invalid credentials |
| SQL injection | Use parameterized database queries and validate input | Test representative injection payloads |
| Cross-site scripting | Encode output in the frontend and avoid unsafe HTML rendering | Verify that test payloads render as text |
| Path traversal or command injection | Do not execute user-supplied commands or use unvalidated paths; use safe APIs | Submit representative malicious patterns |
| Prompt injection | Detect suspicious patterns and apply documented policies; treat detection as heuristic | Test representative benign and malicious prompts |
| Sensitive-data exposure | Minimize stored evidence, redact sensitive values, restrict access, and avoid secrets in logs | Inspect event records and API responses |
| Server-side request forgery (SSRF) | Do not accept arbitrary forwarding URLs; allow only the registered controlled demo target | Attempt loopback, private-network, and external destinations |
| Denial of service | Enforce request-size limits, timeouts, and rate limits | Submit oversized and repeated requests |
| Log injection or audit tampering | Sanitize log fields, restrict write access, and use structured logging | Submit newline/control-character payloads and test permissions |
| Secret exposure | Use secure configuration and secret storage; exclude secrets from Git | Inspect repository and deployment configuration |
| Database failure during inspection | Fail closed and avoid forwarding when required persistence fails | Simulate database unavailability |

## Risk and Residual Risk

Each threat should be assessed for likelihood and impact, with a documented severity and mitigation owner where appropriate. Detection rules are heuristic and may produce false positives and false negatives. PromptShield must not be described as a replacement for parameterized queries, output encoding, secure application design, or other underlying security controls.

## Verification Evidence

For each mitigation, record the test performed, expected result, actual result, and pass/fail status. Deployment security claims remain unverified until the relevant cloud settings and live behavior have been checked.