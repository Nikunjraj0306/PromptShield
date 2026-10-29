-- PromptShield: Initial Azure SQL Database schema
-- Migration: 001_initial_schema.sql
-- Status: Initial development migration

SET XACT_ABORT ON;
BEGIN TRANSACTION;

CREATE TABLE dbo.Users (
    user_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_Users PRIMARY KEY,
    email NVARCHAR(254) NOT NULL,
    password_hash NVARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BIT NOT NULL
        CONSTRAINT DF_Users_is_active DEFAULT (1),
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_Users_created_at DEFAULT (SYSUTCDATETIME()),
    updated_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_Users_updated_at DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT CK_Users_role
        CHECK (role IN ('Admin', 'Analyst', 'Viewer'))
);

CREATE UNIQUE INDEX UX_Users_email ON dbo.Users(email);

CREATE TABLE dbo.Applications (
    application_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_Applications PRIMARY KEY,
    name NVARCHAR(150) NOT NULL,
    description NVARCHAR(500) NULL,
    is_active BIT NOT NULL
        CONSTRAINT DF_Applications_is_active DEFAULT (1),
    created_by BIGINT NULL,
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_Applications_created_at DEFAULT (SYSUTCDATETIME()),
    updated_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_Applications_updated_at DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT FK_Applications_Users
        FOREIGN KEY (created_by) REFERENCES dbo.Users(user_id)
);

CREATE TABLE dbo.Endpoints (
    endpoint_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_Endpoints PRIMARY KEY,
    application_id BIGINT NOT NULL,
    path_pattern NVARCHAR(500) NOT NULL,
    http_method VARCHAR(10) NOT NULL,
    description NVARCHAR(500) NULL,
    is_active BIT NOT NULL
        CONSTRAINT DF_Endpoints_is_active DEFAULT (1),
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_Endpoints_created_at DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT FK_Endpoints_Applications
        FOREIGN KEY (application_id)
        REFERENCES dbo.Applications(application_id),
    CONSTRAINT UQ_Endpoints_Application_Endpoint
        UNIQUE (application_id, endpoint_id),
    CONSTRAINT UQ_Endpoints_Application_Path_Method
        UNIQUE (application_id, path_pattern, http_method)
);

CREATE TABLE dbo.DetectionRules (
    rule_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_DetectionRules PRIMARY KEY,
    name NVARCHAR(120) NOT NULL,
    category VARCHAR(40) NOT NULL,
    description NVARCHAR(500) NULL,
    severity VARCHAR(20) NOT NULL,
    weight INT NOT NULL,
    is_critical BIT NOT NULL
        CONSTRAINT DF_DetectionRules_is_critical DEFAULT (0),
    is_enabled BIT NOT NULL
        CONSTRAINT DF_DetectionRules_is_enabled DEFAULT (1),
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_DetectionRules_created_at DEFAULT (SYSUTCDATETIME()),
    updated_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_DetectionRules_updated_at DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT UQ_DetectionRules_name UNIQUE (name),
    CONSTRAINT CK_DetectionRules_weight CHECK (weight >= 0),
    CONSTRAINT CK_DetectionRules_severity
        CHECK (severity IN ('Low', 'Medium', 'High', 'Critical'))
);

CREATE TABLE dbo.SecurityPolicies (
    policy_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_SecurityPolicies PRIMARY KEY,
    name NVARCHAR(120) NOT NULL,
    description NVARCHAR(500) NULL,
    risk_threshold INT NOT NULL
        CONSTRAINT DF_SecurityPolicies_risk_threshold DEFAULT (50),
    is_enabled BIT NOT NULL
        CONSTRAINT DF_SecurityPolicies_is_enabled DEFAULT (1),
    created_by BIGINT NULL,
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_SecurityPolicies_created_at DEFAULT (SYSUTCDATETIME()),
    updated_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_SecurityPolicies_updated_at DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT UQ_SecurityPolicies_name UNIQUE (name),
    CONSTRAINT CK_SecurityPolicies_threshold
        CHECK (risk_threshold BETWEEN 0 AND 100),
    CONSTRAINT FK_SecurityPolicies_Users
        FOREIGN KEY (created_by) REFERENCES dbo.Users(user_id)
);

CREATE TABLE dbo.SecurityEvents (
    event_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_SecurityEvents PRIMARY KEY,
    application_id BIGINT NOT NULL,
    endpoint_id BIGINT NULL,
    policy_id BIGINT NOT NULL,
    request_time DATETIME2(3) NOT NULL,
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_SecurityEvents_created_at DEFAULT (SYSUTCDATETIME()),
    risk_score INT NOT NULL,
    decision VARCHAR(10) NOT NULL,
    reason_code VARCHAR(50) NOT NULL,
    correlation_id UNIQUEIDENTIFIER NOT NULL
        CONSTRAINT DF_SecurityEvents_correlation_id DEFAULT (NEWID()),
    http_method VARCHAR(10) NULL,
    request_path NVARCHAR(500) NULL,
    processing_status VARCHAR(20) NOT NULL,
    CONSTRAINT FK_SecurityEvents_Applications
        FOREIGN KEY (application_id)
        REFERENCES dbo.Applications(application_id),
    CONSTRAINT FK_SecurityEvents_Endpoints
        FOREIGN KEY (application_id, endpoint_id)
        REFERENCES dbo.Endpoints(application_id, endpoint_id),
    CONSTRAINT FK_SecurityEvents_Policies
        FOREIGN KEY (policy_id) REFERENCES dbo.SecurityPolicies(policy_id),
    CONSTRAINT CK_SecurityEvents_risk_score
        CHECK (risk_score BETWEEN 0 AND 100),
    CONSTRAINT CK_SecurityEvents_decision
        CHECK (decision IN ('Allow', 'Block')),
    CONSTRAINT CK_SecurityEvents_processing_status
        CHECK (processing_status IN ('Completed', 'Failed'))
);

CREATE TABLE dbo.ThreatFindings (
    finding_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_ThreatFindings PRIMARY KEY,
    event_id BIGINT NOT NULL,
    rule_id BIGINT NULL,
    rule_name_snapshot NVARCHAR(120) NOT NULL,
    category_snapshot VARCHAR(40) NOT NULL,
    severity_snapshot VARCHAR(20) NOT NULL,
    weight_snapshot INT NOT NULL,
    is_critical_snapshot BIT NOT NULL,
    confidence DECIMAL(4,3) NULL,
    evidence_summary NVARCHAR(1000) NULL,
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_ThreatFindings_created_at DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT FK_ThreatFindings_Events
        FOREIGN KEY (event_id) REFERENCES dbo.SecurityEvents(event_id)
        ON DELETE CASCADE,
    CONSTRAINT FK_ThreatFindings_Rules
        FOREIGN KEY (rule_id) REFERENCES dbo.DetectionRules(rule_id),
    CONSTRAINT CK_ThreatFindings_weight
        CHECK (weight_snapshot >= 0),
    CONSTRAINT CK_ThreatFindings_confidence
        CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
    CONSTRAINT CK_ThreatFindings_severity
        CHECK (severity_snapshot IN ('Low', 'Medium', 'High', 'Critical'))
);

CREATE TABLE dbo.AuditLogs (
    audit_id BIGINT IDENTITY(1,1) NOT NULL
        CONSTRAINT PK_AuditLogs PRIMARY KEY,
    user_id BIGINT NULL,
    action VARCHAR(80) NOT NULL,
    entity_type VARCHAR(50) NULL,
    entity_id NVARCHAR(100) NULL,
    outcome VARCHAR(20) NOT NULL,
    correlation_id UNIQUEIDENTIFIER NULL,
    created_at DATETIME2(3) NOT NULL
        CONSTRAINT DF_AuditLogs_created_at DEFAULT (SYSUTCDATETIME()),
    details_summary NVARCHAR(1000) NULL,
    CONSTRAINT FK_AuditLogs_Users
        FOREIGN KEY (user_id) REFERENCES dbo.Users(user_id),
    CONSTRAINT CK_AuditLogs_outcome
        CHECK (outcome IN ('Success', 'Failure'))
);

CREATE INDEX IX_Endpoints_Application_Active
    ON dbo.Endpoints(application_id, is_active);

CREATE INDEX IX_SecurityEvents_CreatedAt
    ON dbo.SecurityEvents(created_at);

CREATE INDEX IX_SecurityEvents_Application_CreatedAt
    ON dbo.SecurityEvents(application_id, created_at);

CREATE INDEX IX_SecurityEvents_Decision_CreatedAt
    ON dbo.SecurityEvents(decision, created_at);

CREATE INDEX IX_SecurityEvents_CorrelationId
    ON dbo.SecurityEvents(correlation_id);

CREATE INDEX IX_ThreatFindings_Event
    ON dbo.ThreatFindings(event_id);

CREATE INDEX IX_ThreatFindings_Category_Severity
    ON dbo.ThreatFindings(category_snapshot, severity_snapshot);

CREATE INDEX IX_AuditLogs_CreatedAt
    ON dbo.AuditLogs(created_at);

CREATE INDEX IX_AuditLogs_User_CreatedAt
    ON dbo.AuditLogs(user_id, created_at);

COMMIT TRANSACTION;
