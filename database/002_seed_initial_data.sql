-- PromptShield: Initial seed data
-- Run only after 001_initial_schema.sql succeeds.
-- Safe to rerun for these stable seed names.

SET XACT_ABORT ON;
BEGIN TRANSACTION;

-- Default policy: critical findings always block;
-- otherwise block when the score reaches the threshold.
IF NOT EXISTS (
    SELECT 1
    FROM dbo.SecurityPolicies
    WHERE name = N'Default Policy'
)
BEGIN
    INSERT INTO dbo.SecurityPolicies
        (name, description, risk_threshold, is_enabled)
    VALUES
        (
            N'Default Policy',
            N'Blocks critical findings or requests meeting the configured risk threshold.',
            50,
            1
        );
END;

-- Starter rule weights are proposed heuristic values.
-- They must be validated and tuned with tests before deployment.
INSERT INTO dbo.DetectionRules
    (name, category, description, severity, weight, is_critical, is_enabled)
SELECT
    seed.name,
    seed.category,
    seed.description,
    seed.severity,
    seed.weight,
    seed.is_critical,
    1
FROM (
    VALUES
    (
        N'SQL Injection Pattern',
        'SQL_INJECTION',
        N'Detects selected SQL injection-like input patterns.',
        'High',
        35,
        0
    ),
    (
        N'Cross-Site Scripting Pattern',
        'XSS',
        N'Detects selected cross-site scripting-like input patterns.',
        'High',
        35,
        0
    ),
    (
        N'Path Traversal Pattern',
        'PATH_TRAVERSAL',
        N'Detects selected path traversal-like input patterns.',
        'High',
        35,
        0
    ),
    (
        N'Command Injection Pattern',
        'COMMAND_INJECTION',
        N'Detects selected command injection-like input patterns.',
        'Critical',
        60,
        1
    ),
    (
        N'Prompt Injection Pattern',
        'PROMPT_INJECTION',
        N'Detects selected prompt injection-like input patterns.',
        'Medium',
        25,
        0
    ),
    (
        N'Sensitive Data Pattern',
        'SENSITIVE_DATA',
        N'Detects selected patterns that may contain sensitive data.',
        'High',
        35,
        0
    ),
    (
        N'Request Rate Limit',
        'RATE_LIMIT',
        N'Flags requests that exceed the configured rate limit.',
        'High',
        50,
        0
    )
) AS seed(name, category, description, severity, weight, is_critical)
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.DetectionRules existing
    WHERE existing.name = seed.name
);

COMMIT TRANSACTION;

-- Verify seeded records.
SELECT policy_id, name, risk_threshold, is_enabled
FROM dbo.SecurityPolicies
WHERE name = N'Default Policy';

SELECT rule_id, name, category, severity, weight, is_critical, is_enabled
FROM dbo.DetectionRules
ORDER BY rule_id;