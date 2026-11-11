# PromptShield — Implemented Database Schema

## 1. Purpose

This document describes the relational database schema implemented for PromptShield using Microsoft Azure SQL Database.

The database supports user authentication, application registration, endpoint configuration, detection rules, security policies, request-inspection events, threat findings and audit records.

**Implementation status:** Implemented and deployed in Azure SQL Database.

**Database name:** PromptshieldDB

**Schema:** dbo

## 2. Database Conventions

| Property | Implementation |
|---|---|
| Database system | Microsoft Azure SQL Database |
| Database model | Relational |
| Primary key type | BIGINT IDENTITY(1,1) |
| Timestamp type | DATETIME2(3) |
| Boolean type | BIT |
| Risk score type | INT |
| Unicode text | NVARCHAR |
| SQL schema | dbo |

Timestamps use UTC defaults through `SYSUTCDATETIME()` where defined.

The database uses primary keys, foreign keys, unique constraints, check constraints and indexes to maintain data integrity.

## 3. Entity Overview

The implemented database contains eight tables:

1. Users
2. Applications
3. Endpoints
4. DetectionRules
5. SecurityPolicies
6. SecurityEvents
7. ThreatFindings
8. AuditLogs

The MVP supports a single organization. A separate Organizations table is not implemented.

## 4. Table Definitions

### 4.1 Users

**Purpose:** Stores user accounts and authentication information.

| Column | SQL type | Constraints |
|---|---|---|
| user_id | BIGINT IDENTITY | Primary key |
| email | NVARCHAR(254) | NOT NULL |
| password_hash | NVARCHAR(255) | NOT NULL |
| role | VARCHAR(20) | NOT NULL |
| is_active | BIT | NOT NULL, DEFAULT 1 |
| created_at | DATETIME2(3) | NOT NULL, UTC default |
| updated_at | DATETIME2(3) | NOT NULL, UTC default |

Additional constraints:
- Unique index on email.
- Role must be Admin, Analyst or Viewer.

### 4.2 Applications

**Purpose:** Stores registered applications.

| Column | SQL type | Constraints |
|---|---|---|
| application_id | BIGINT IDENTITY | Primary key |
| name | NVARCHAR(150) | NOT NULL |
| description | NVARCHAR(500) | NULL |
| is_active | BIT | NOT NULL, DEFAULT 1 |
| created_by | BIGINT | Optional foreign key to Users |
| created_at | DATETIME2(3) | NOT NULL, UTC default |
| updated_at | DATETIME2(3) | NOT NULL, UTC default |

### 4.3 Endpoints

**Purpose:** Stores endpoint definitions associated with registered applications.

| Column | SQL type | Constraints |
|---|---|---|
| endpoint_id | BIGINT IDENTITY | Primary key |
| application_id | BIGINT | NOT NULL, foreign key |
| path_pattern | NVARCHAR(500) | NOT NULL |
| http_method | VARCHAR(10) | NOT NULL |
| description | NVARCHAR(500) | NULL |
| is_active | BIT | NOT NULL, DEFAULT 1 |
| created_at | DATETIME2(3) | NOT NULL, UTC default |

Additional constraints:
- Unique combination of application_id and endpoint_id.
- Unique combination of application_id, path_pattern and http_method.

### 4.4 DetectionRules

**Purpose:** Stores security detection-rule configurations.

| Column | SQL type | Constraints |
|---|---|---|
| rule_id | BIGINT IDENTITY | Primary key |
| name | NVARCHAR(120) | NOT NULL, UNIQUE |
| category | VARCHAR(40) | NOT NULL |
| description | NVARCHAR(500) | NULL |
| severity | VARCHAR(20) | NOT NULL |
| weight | INT | NOT NULL |
| is_critical | BIT | NOT NULL, DEFAULT 0 |
| is_enabled | BIT | NOT NULL, DEFAULT 1 |
| created_at | DATETIME2(3) | NOT NULL, UTC default |
| updated_at | DATETIME2(3) | NOT NULL, UTC default |

Additional constraints:
- Weight must be non-negative.
- Severity must be Low, Medium, High or Critical.

### 4.5 SecurityPolicies

**Purpose:** Stores risk-based security policy configuration.

| Column | SQL type | Constraints |
|---|---|---|
| policy_id | BIGINT IDENTITY | Primary key |
| name | NVARCHAR(120) | NOT NULL, UNIQUE |
| description | NVARCHAR(500) | NULL |
| risk_threshold | INT | NOT NULL, DEFAULT 50 |
| is_enabled | BIT | NOT NULL, DEFAULT 1 |
| created_by | BIGINT | Optional foreign key to Users |
| created_at | DATETIME2(3) | NOT NULL, UTC default |
| updated_at | DATETIME2(3) | NOT NULL, UTC default |

The risk threshold must be between 0 and 100.

### 4.6 SecurityEvents

**Purpose:** Stores request-inspection results and security decisions.

| Column | SQL type | Constraints |
|---|---|---|
| event_id | BIGINT IDENTITY | Primary key |
| application_id | BIGINT | NOT NULL, foreign key |
| endpoint_id | BIGINT | NULL, composite foreign key |
| policy_id | BIGINT | NOT NULL, foreign key |
| request_time | DATETIME2(3) | NOT NULL |
| created_at | DATETIME2(3) | NOT NULL, UTC default |
| risk_score | INT | NOT NULL |
| decision | VARCHAR(10) | NOT NULL |
| reason_code | VARCHAR(50) | NOT NULL |
| correlation_id | UNIQUEIDENTIFIER | NOT NULL, default NEWID() |
| http_method | VARCHAR(10) | NULL |
| request_path | NVARCHAR(500) | NULL |
| processing_status | VARCHAR(20) | NOT NULL |

Additional constraints:
- Risk score must be between 0 and 100.
- Decision must be Allow or Block.
- Processing status must be Completed or Failed.
- The composite foreign key ensures that the endpoint belongs to the same application.

### 4.7 ThreatFindings

**Purpose:** Stores individual security findings associated with inspection events.

| Column | SQL type | Constraints |
|---|---|---|
| finding_id | BIGINT IDENTITY | Primary key |
| event_id | BIGINT | NOT NULL, foreign key |
| rule_id | BIGINT | NULL, foreign key |
| rule_name_snapshot | NVARCHAR(120) | NOT NULL |
| category_snapshot | VARCHAR(40) | NOT NULL |
| severity_snapshot | VARCHAR(20) | NOT NULL |
| weight_snapshot | INT | NOT NULL |
| is_critical_snapshot | BIT | NOT NULL |
| confidence | DECIMAL(4,3) | NULL |
| evidence_summary | NVARCHAR(1000) | NULL |
| created_at | DATETIME2(3) | NOT NULL, UTC default |

Additional constraints:
- Weight must be non-negative.
- Confidence, when provided, must be between 0 and 1.
- Severity must be Low, Medium, High or Critical.
- Deleting a security event cascades to its associated findings.

Snapshot columns preserve the rule information associated with a finding at inspection time.

### 4.8 AuditLogs

**Purpose:** Stores audit-related application activity.

| Column | SQL type | Constraints |
|---|---|---|
| audit_id | BIGINT IDENTITY | Primary key |
| user_id | BIGINT | NULL, foreign key |
| action | VARCHAR(80) | NOT NULL |
| entity_type | VARCHAR(50) | NULL |
| entity_id | NVARCHAR(100) | NULL |
| outcome | VARCHAR(20) | NOT NULL |
| correlation_id | UNIQUEIDENTIFIER | NULL |
| created_at | DATETIME2(3) | NOT NULL, UTC default |
| details_summary | NVARCHAR(1000) | NULL |

The outcome must be Success or Failure.

## 5. Relationships

The implemented foreign-key relationships are:

| Parent | Child | Relationship |
|---|---|---|
| Users | Applications | One-to-many |
| Users | SecurityPolicies | One-to-many |
| Users | AuditLogs | One-to-many |
| Applications | Endpoints | One-to-many |
| Applications | SecurityEvents | One-to-many |
| Endpoints | SecurityEvents | One-to-many, optional endpoint |
| SecurityPolicies | SecurityEvents | One-to-many |
| SecurityEvents | ThreatFindings | One-to-many |
| DetectionRules | ThreatFindings | One-to-many, optional rule |

## 6. Primary Keys and Foreign Keys

Each table has a primary key that uniquely identifies its records.

Foreign keys maintain relationships between related entities.

An important implementation detail is the composite foreign key in SecurityEvents:

- SecurityEvents.application_id references Endpoints.application_id.
- SecurityEvents.endpoint_id references Endpoints.endpoint_id.

Together, these columns ensure endpoint ownership consistency.

## 7. Constraints

The database implements the following constraints:

- PRIMARY KEY for record identification.
- FOREIGN KEY for referential integrity.
- UNIQUE for duplicate prevention.
- CHECK for valid roles, severity, risk scores and decisions.
- DEFAULT for initial values and timestamps.
- NOT NULL for mandatory fields.

These constraints help prevent invalid data from entering the database.

## 8. Indexes

The migration creates indexes to support application queries and dashboard retrieval.

| Index | Table | Purpose |
|---|---|---|
| UX_Users_email | Users | Unique email lookup |
| UQ_DetectionRules_name | DetectionRules | Unique rule names |
| UQ_SecurityPolicies_name | SecurityPolicies | Unique policy names |
| IX_Endpoints_Application_Active | Endpoints | Application and active endpoint lookup |
| IX_SecurityEvents_CreatedAt | SecurityEvents | Time-based event retrieval |
| IX_SecurityEvents_Application_CreatedAt | SecurityEvents | Application-specific event retrieval |
| IX_SecurityEvents_Decision_CreatedAt | SecurityEvents | Decision-based event retrieval |
| IX_SecurityEvents_CorrelationId | SecurityEvents | Correlation lookup |
| IX_ThreatFindings_Event | ThreatFindings | Event finding retrieval |
| IX_ThreatFindings_Category_Severity | ThreatFindings | Threat classification queries |
| IX_AuditLogs_CreatedAt | AuditLogs | Time-based audit retrieval |
| IX_AuditLogs_User_CreatedAt | AuditLogs | User-specific audit retrieval |

## 9. Database Migration and Seed Data

The initial schema is defined in:

`database/001_initial_schema.sql`

This migration creates the eight tables, primary keys, foreign keys, constraints and indexes.

The project also includes seed data used to initialize the application with its initial configuration.

The database was deployed to Microsoft Azure SQL Database and successfully connected to the cloud-hosted FastAPI backend.

## 10. Database Connectivity

The backend connects to Azure SQL Database using Python pyodbc and Microsoft ODBC Driver 18.

Database connection configuration is supplied through backend environment variables.

The actual database password and other sensitive connection information are not included in this document or in source-controlled configuration files.

## 11. Conclusion

The implemented PromptShield database demonstrates relational database design through eight interconnected tables.

It uses primary keys, foreign keys, composite relationships, constraints and indexes to maintain data integrity and support authentication, inspection, threat findings, analytics and audit-related storage.

The schema is implemented in Azure SQL Database and integrated with the deployed FastAPI backend.