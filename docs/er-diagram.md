## Single-Organization MVP and Updated Constraints

PromptShield's initial deployment serves one organization. The Organizations table and organization foreign keys are therefore omitted. Multi-tenant support would require a separate reviewed schema and authorization design.

### Authentication Constraints

## Database Constraints and Integrity Rules

- `Users.email` shall be unique and normalized consistently.
- `Users.role` shall be restricted to `Admin`, `Analyst`, or `Viewer`.
- `Users.is_active` shall determine whether a user account can authenticate or perform protected operations.
- `DetectionRules.weight` shall be a non-negative integer.
- `DetectionRules.is_critical` shall indicate whether a finding triggers the critical-rule override.
- `SecurityEvents.risk_score` shall be constrained to the range 0–100.
- `SecurityEvents.decision` shall be restricted to `Allow` or `Block`.
- `SecurityEvents.request_time` records when the request was observed; `created_at` records when the event record was created. Both shall use UTC.
- `SecurityEvents.policy_id` may be nullable only if the system permits a documented default-policy path. Otherwise, a valid policy reference is required.
- If an event references an endpoint, that endpoint must belong to the same application referenced by the event. This must be enforced through an appropriate composite constraint or transactional backend validation.
- The event and its associated findings shall be persisted transactionally so that a partial write is not reported as a successful inspection record.
- Retention cleanup shall remove dependent findings safely and must not unintentionally delete audit records.
- Historical findings must remain interpretable if a detection rule is disabled or changed. Rule deletion behavior must preserve historical references or a suitable historical rule snapshot.

### Confidence Field

If `ThreatFindings.confidence` is retained, define it as a value between 0 and 1 and document how each detector derives it. If the MVP detectors cannot produce a meaningful confidence value, omit this field for the initial version rather than assigning arbitrary values.

### Policy Threshold

Define whether the threshold of 50 is the system default or a fixed rule. If policies can override the threshold, document the allowed range and precedence. The critical-finding override must always take precedence over a configured threshold or Allow action.thin this deployment. Password hashes may be stored in a dedicated password-hash column if local password authentication is implemented; plaintext passwords and signing secrets must never be stored.

JWT expiry and validation are enforced by the backend rather than by a database relationship.

### Risk and Policy Constraints

SecurityEvents.risk_score must be an integer between 0 and 100. SecurityEvents.decision is restricted to Allow or Block. DetectionRules.weight must be a non-negative integer. Critical findings override the score threshold; otherwise, a score of at least 50 causes Block.

### Event Consistency and Retention

An event and its findings should be persisted transactionally so that partial writes are not reported as successful. If the required persistence operation fails, the request must not be forwarded.

Security events and their associated findings have a proposed 30-day retention period. Deleting an expired event must also delete its dependent findings through a documented cascade or controlled deletion transaction. Audit-log retention is separate.

### Suggested Additional Fields

- Users.password_hash: nullable only if an external identity provider is later adopted; required for application-managed password authentication.
- SecurityEvents.created_at: timestamp for event creation and retention processing.
- SecurityEvents.correlation_id: identifier for safely tracing a request across processing and diagnostics.
- DetectionRules.is_critical: indicates whether a finding from the rule must cause a Block decision.

The exact SQL data types, foreign-key deletion behavior, and constraints must be confirmed in the implementation design.
