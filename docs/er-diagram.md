# PromptShield — Entity Relationship Diagram

## 1. Introduction

The PromptShield database uses a relational data model implemented in Microsoft Azure SQL Database.

The Entity Relationship Diagram (ERD) represents the eight main database tables, their primary keys, foreign keys and relationships.

## 2. Main Entities

The database consists of:

1. Users
2. Applications
3. Endpoints
4. DetectionRules
5. SecurityPolicies
6. SecurityEvents
7. ThreatFindings
8. AuditLogs

## 3. Relationship Explanation

| Relationship | Cardinality |
|---|---|
| Users to Applications | One-to-many, optional creator |
| Users to SecurityPolicies | One-to-many, optional creator |
| Users to AuditLogs | One-to-many, optional user |
| Applications to Endpoints | One-to-many |
| Applications to SecurityEvents | One-to-many |
| Endpoints to SecurityEvents | One-to-many, optional endpoint |
| SecurityPolicies to SecurityEvents | One-to-many |
| SecurityEvents to ThreatFindings | One-to-many |
| DetectionRules to ThreatFindings | One-to-many, optional rule reference |

## 4. Important Database Relationships

### Application and Endpoint Relationship

Each endpoint belongs to one registered application. The database uses a composite unique key on `(application_id, endpoint_id)` to support validation of endpoint ownership by security events.

### Security Event and Threat Finding Relationship

A security event may contain multiple threat findings. Each finding references its parent security event through `event_id`.

The database uses `ON DELETE CASCADE` for this relationship.

### Detection Rule and Threat Finding Relationship

A threat finding may reference the detection rule that identified it. Snapshot columns preserve the rule's name, category, severity and weight at the time of inspection.

### User and Audit Log Relationship

Audit records can reference the user responsible for an action. The user reference is optional to support records without an associated authenticated user.

## 5. Database Integrity

The database uses:

- Primary keys for unique record identification.
- Foreign keys for referential integrity.
- Unique constraints to prevent duplicate records.
- Check constraints to restrict invalid values.
- Indexes to improve data retrieval.

## 6. Diagram Source

The complete Mermaid ER diagram is maintained in:

`docs/er-diagram.mmd`

It represents the database structure defined in:

`database/001_initial_schema.sql`

## 7. Conclusion

The ER diagram illustrates how PromptShield organizes its relational data and maintains relationships between users, applications, endpoints, security policies, detection rules, security events and threat findings.