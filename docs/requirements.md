## MVP Detection Requirements

The MVP shall implement rule-based detection for:

- SQL injection patterns
- Cross-site scripting (XSS) patterns
- Path traversal patterns
- Command-injection patterns
- Prompt-injection patterns
- Selected sensitive-data patterns
- Rate-limit violations

These detectors provide indicators and policy inputs; they do not guarantee detection of every attack. Detection results shall include a rule reference, severity, and a concise evidence summary that avoids unnecessary sensitive-data retention.

## Risk Scoring and Policy Requirements

Each applicable finding contributes a non-negative integer rule weight. The risk score is the sum of applicable weights capped at 100. If no findings apply, the score is 0.

A request shall be blocked if any applicable finding is marked critical or if its score is at least 50. Otherwise, it shall be allowed unless another explicitly configured policy requires blocking. Critical findings always take precedence over any Allow rule.

Policy precedence and tie-breaking shall be deterministic, documented, and covered by tests. The effective decision and reason code shall be recorded.

## Authentication Requirements

The MVP shall use application-managed authentication with salted password hashing, signed short-lived access tokens, and server-side role enforcement.

For the initial MVP, refresh tokens are not supported; users must authenticate again when their access token expires. Logout removes the token from the client but does not independently revoke an already issued stateless token. Protected operations must validate token expiry, signature, and account status.

Login attempts shall be rate-limited. Passwords, signing keys, tokens, and database credentials must never be written to application logs.

## Request Forwarding and Failure Requirements

The MVP shall forward only approved requests to a registered controlled demo target. Arbitrary user-provided forwarding URLs are out of scope.

If a required inspection, policy, or persistence step fails, the request shall not be forwarded. Error responses shall not expose stack traces, credentials, or internal secrets.

## Retention and Analytics Requirements

Security events and their associated findings shall have a proposed retention period of 30 days. Cleanup must preserve referential integrity. Audit-log retention shall be defined separately before deployment.

The dashboard shall report event counts over time, findings by category and severity, Allow-versus-Block counts, score distribution, and the most-targeted registered endpoints. Timestamps shall be stored and aggregated consistently in UTC.

## Acceptance Criteria

- Role checks are enforced by the backend.
- Risk scoring follows the documented formula and boundaries.
- Critical findings always produce a Block decision.
- Requests are not forwarded after a required processing or persistence failure.
- Arbitrary forwarding destinations are rejected.
- Event and finding records remain consistent when a database transaction fails.
- Analytics results agree with the underlying stored events.
- Security tests and their outcomes are recorded before deployment claims are made.