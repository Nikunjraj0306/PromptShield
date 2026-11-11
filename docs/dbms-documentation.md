# PromptShield — Database Management System (DBMS) Documentation

## 1. Introduction

Database Management Systems provide a structured way to store, organize, retrieve and manage application data.

PromptShield uses Microsoft Azure SQL Database, a relational database management system, to store user information, application configurations, detection rules, security policies, security events, threat findings and audit records.

The database is designed using relational database concepts, including primary keys, foreign keys, constraints, relationships and indexes.

## 2. Database Technology

| Property | Implementation |
|---|---|
| Database system | Microsoft Azure SQL Database |
| Database model | Relational |
| Query language | SQL |
| Backend connectivity | Python pyodbc |
| Database driver | Microsoft ODBC Driver 18 |
| Schema | dbo |
| Database name | PromptshieldDB |

## 3. Database Design

The PromptShield database contains eight main tables:

1. Users
2. Applications
3. Endpoints
4. DetectionRules
5. SecurityPolicies
6. SecurityEvents
7. ThreatFindings
8. AuditLogs

The database supports the application's authentication, request-inspection, threat-detection and monitoring functionality.

## 4. Table Descriptions

### 4.1 Users

**Purpose:** Stores user account information for authentication and authorization.

Important columns:

- `user_id` — Primary key.
- `email` — User email address.
- `password_hash` — Hashed password.
- `role` — User role: Admin, Analyst or Viewer.
- `is_active` — Account activation status.
- `created_at` — Account creation timestamp.
- `updated_at` — Last update timestamp.

The email column has a unique index to prevent duplicate email addresses.

### 4.2 Applications

**Purpose:** Stores registered applications that can be associated with inspection requests.

Important columns:

- `application_id` — Primary key.
- `name` — Application name.
- `description` — Application description.
- `is_active` — Application activation status.
- `created_by` — Foreign key referencing Users.
- `created_at` — Creation timestamp.
- `updated_at` — Update timestamp.

### 4.3 Endpoints

**Purpose:** Stores endpoint definitions associated with registered applications.

Important columns:

- `endpoint_id` — Primary key.
- `application_id` — Foreign key referencing Applications.
- `path_pattern` — Endpoint path.
- `http_method` — HTTP method.
- `description` — Endpoint description.
- `is_active` — Endpoint activation status.
- `created_at` — Creation timestamp.

A unique constraint is applied to the combination of application ID, path pattern and HTTP method.

### 4.4 DetectionRules

**Purpose:** Stores detection-rule configuration used by the inspection engine.

Important columns:

- `rule_id` — Primary key.
- `name` — Detection-rule name.
- `category` — Threat category.
- `description` — Rule description.
- `severity` — Severity level.
- `weight` — Risk weight.
- `is_critical` — Critical-rule indicator.
- `is_enabled` — Rule activation status.
- `created_at` — Creation timestamp.
- `updated_at` — Update timestamp.

The database applies constraints to rule weights and severity values.

### 4.5 SecurityPolicies

**Purpose:** Stores security policy configuration.

Important columns:

- `policy_id` — Primary key.
- `name` — Policy name.
- `description` — Policy description.
- `risk_threshold` — Risk threshold used for decisions.
- `is_enabled` — Policy activation status.
- `created_by` — Foreign key referencing Users.
- `created_at` — Creation timestamp.
- `updated_at` — Update timestamp.

The risk threshold is restricted to values between 0 and 100. The default value is 50.

### 4.6 SecurityEvents

**Purpose:** Stores request-inspection results and security decisions.

Important columns:

- `event_id` — Primary key.
- `application_id` — Foreign key referencing Applications.
- `endpoint_id` — Optional endpoint reference.
- `policy_id` — Foreign key referencing SecurityPolicies.
- `request_time` — Request timestamp.
- `created_at` — Event creation timestamp.
- `risk_score` — Calculated risk score.
- `decision` — Allow or Block.
- `reason_code` — Decision reason.
- `correlation_id` — Request tracking identifier.
- `http_method` — HTTP method.
- `request_path` — Request path.
- `processing_status` — Processing status.

Constraints restrict risk scores to 0–100 and decisions to Allow or Block.

### 4.7 ThreatFindings

**Purpose:** Stores individual threat findings associated with security events.

Important columns:

- `finding_id` — Primary key.
- `event_id` — Foreign key referencing SecurityEvents.
- `rule_id` — Optional foreign key referencing DetectionRules.
- `rule_name_snapshot` — Rule name at inspection time.
- `category_snapshot` — Threat category.
- `severity_snapshot` — Severity level.
- `weight_snapshot` — Rule weight at inspection time.
- `is_critical_snapshot` — Critical status at inspection time.
- `confidence` — Optional confidence value.
- `evidence_summary` — Summary of detected evidence.
- `created_at` — Finding creation timestamp.

The event relationship uses `ON DELETE CASCADE`, so associated findings are deleted when their parent event is deleted.

### 4.8 AuditLogs

**Purpose:** Stores audit-related activity records.

Important columns:

- `audit_id` — Primary key.
- `user_id` — Optional foreign key referencing Users.
- `action` — Recorded action.
- `entity_type` — Type of entity involved.
- `entity_id` — Related entity identifier.
- `outcome` — Success or Failure.
- `correlation_id` — Optional request tracking identifier.
- `created_at` — Record creation timestamp.
- `details_summary` — Summary of activity details.

## 5. Entity Relationships

The database uses foreign keys to maintain relationships between related entities.

The main relationships are:

| Parent table | Child table | Relationship |
|---|---|---|
| Users | Applications | One-to-many, optional creator |
| Users | SecurityPolicies | One-to-many, optional creator |
| Users | AuditLogs | One-to-many, optional user |
| Applications | Endpoints | One-to-many |
| Applications | SecurityEvents | One-to-many |
| Endpoints | SecurityEvents | One-to-many, optional endpoint |
| SecurityPolicies | SecurityEvents | One-to-many |
| SecurityEvents | ThreatFindings | One-to-many |
| DetectionRules | ThreatFindings | One-to-many, optional rule |

These relationships help maintain referential integrity and organize the data logically.

## 6. Primary Keys and Foreign Keys

### Primary Keys

Each table uses a primary key to uniquely identify its records.

Examples:

- `Users.user_id`
- `Applications.application_id`
- `Endpoints.endpoint_id`
- `DetectionRules.rule_id`
- `SecurityPolicies.policy_id`
- `SecurityEvents.event_id`
- `ThreatFindings.finding_id`
- `AuditLogs.audit_id`

### Foreign Keys

Foreign keys connect related tables.

Examples:

- `Applications.created_by` references `Users.user_id`.
- `Endpoints.application_id` references `Applications.application_id`.
- `SecurityEvents.policy_id` references `SecurityPolicies.policy_id`.
- `ThreatFindings.event_id` references `SecurityEvents.event_id`.

The SecurityEvents table also uses a composite foreign key to ensure that an associated endpoint belongs to the same application as the event.

## 7. Database Constraints

The database uses several constraints to preserve data correctness.

| Constraint | Purpose |
|---|---|
| PRIMARY KEY | Uniquely identifies records |
| FOREIGN KEY | Maintains relationships |
| UNIQUE | Prevents duplicate values |
| CHECK | Restricts invalid values |
| DEFAULT | Supplies default values |
| NOT NULL | Ensures required values are present |

Examples include:

- Unique user email.
- Valid user roles.
- Non-negative detection-rule weights.
- Valid risk-score range.
- Valid security decisions.
- Valid severity levels.
- Valid audit outcomes.

## 8. Database Indexing

Indexes are implemented to improve query performance.

Examples include:

- User email index.
- Endpoint application and activation index.
- Security-event creation timestamp index.
- Security-event application and timestamp index.
- Security-event decision and timestamp index.
- Security-event correlation ID index.
- Threat-finding event index.
- Threat-finding category and severity index.
- Audit-log timestamp and user indexes.

Indexes help improve the retrieval of dashboard data and security-event records.

## 9. Data Integrity and Security

The database implementation incorporates the following practices:

1. Primary and foreign keys maintain referential integrity.
2. CHECK constraints restrict invalid data.
3. Unique indexes prevent duplicate user email addresses.
4. Passwords are stored as hashes rather than plaintext.
5. Database credentials are configured through backend environment variables.
6. Database connections use Microsoft ODBC Driver 18.
7. Azure SQL firewall rules restrict permitted network access.

## 10. Database Implementation

The initial database schema is defined in:

`database/001_initial_schema.sql`

The database setup also includes migration scripts and seed data.

The initial schema creates the eight main tables, their relationships, constraints and indexes.

Seed data provides the initial registered application, endpoint, detection rules and security policy required by the MVP.

The database is hosted on Microsoft Azure SQL Database and accessed by the FastAPI backend.

## 11. DBMS Concepts Demonstrated

The PromptShield project demonstrates the following DBMS concepts:

- Relational database model.
- Entity Relationship modelling.
- Primary keys and foreign keys.
- One-to-many relationships.
- Composite foreign keys.
- Unique and CHECK constraints.
- Default values and NOT NULL constraints.
- Database indexing.
- SQL schema creation and migrations.
- Referential integrity.
- Persistent data storage.
- Database connectivity through a backend application.

## 12. Conclusion

PromptShield demonstrates the practical use of relational database management concepts through Microsoft Azure SQL Database.

The database organizes application information, user accounts, detection configurations, inspection events and audit records into related tables.

The implementation uses keys, constraints, indexes and relationships to maintain data integrity and support the application's core functionality.