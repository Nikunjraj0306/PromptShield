from uuid import uuid4

from app.database import get_connection
from app.detector import (
    calculate_risk_score,
    inspect_text,
    make_decision,
)


def inspect_and_store(
    application_id: int,
    endpoint_id: int,
    text: str,
) -> dict:
    correlation_id = str(uuid4())
    connection = get_connection()

    try:
        connection.autocommit = False
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT application_id
            FROM dbo.Applications
            WHERE application_id = ? AND is_active = 1
            """,
            application_id,
        )
        if cursor.fetchone() is None:
            raise ValueError("APPLICATION_NOT_FOUND_OR_INACTIVE")

        cursor.execute(
            """
            SELECT endpoint_id
            FROM dbo.Endpoints
            WHERE endpoint_id = ?
              AND application_id = ?
              AND is_active = 1
            """,
            endpoint_id,
            application_id,
        )
        if cursor.fetchone() is None:
            raise ValueError("ENDPOINT_NOT_FOUND_OR_INACTIVE")

        cursor.execute(
            """
            SELECT TOP (1) policy_id, risk_threshold
            FROM dbo.SecurityPolicies
            WHERE name = N'Default Policy' AND is_enabled = 1
            ORDER BY policy_id
            """
        )
        policy = cursor.fetchone()
        if policy is None:
            raise RuntimeError("NO_ENABLED_DEFAULT_POLICY")

        policy_id, threshold = int(policy[0]), int(policy[1])

        cursor.execute(
            """
            SELECT rule_id, name, category, severity, weight, is_critical
            FROM dbo.DetectionRules
            WHERE is_enabled = 1
            """
        )

        enabled_rules = {
            row.name: {
                "rule_id": int(row.rule_id),
                "category": row.category,
                "severity": row.severity,
                "weight": int(row.weight),
                "is_critical": bool(row.is_critical),
            }
            for row in cursor.fetchall()
        }

        detected = inspect_text(text)
        findings = []

        for finding in detected:
            rule = enabled_rules.get(finding.rule_name)
            if rule is None:
                continue

            findings.append(
                type(finding)(
                    rule_name=finding.rule_name,
                    category=rule["category"],
                    severity=rule["severity"],
                    weight=rule["weight"],
                    is_critical=rule["is_critical"],
                    confidence=finding.confidence,
                    evidence_summary=finding.evidence_summary,
                )
            )

        score = calculate_risk_score(findings)
        decision, reason = make_decision(
            findings,
            score,
            threshold,
        )

        cursor.execute(
            """
            INSERT INTO dbo.SecurityEvents
                (application_id, endpoint_id, policy_id, request_time,
                 risk_score, decision, reason_code, correlation_id,
                 http_method, request_path, processing_status)
            OUTPUT INSERTED.event_id
            VALUES (?, ?, ?, SYSUTCDATETIME(), ?, ?, ?, ?,
                    'POST', N'/api/v1/inspect', 'Completed')
            """,
            application_id,
            endpoint_id,
            policy_id,
            score,
            decision,
            reason,
            correlation_id,
        )

        event_row = cursor.fetchone()
        if event_row is None:
            raise RuntimeError("EVENT_INSERT_FAILED")

        event_id = int(event_row[0])

        for finding in findings:
            rule = enabled_rules[finding.rule_name]
            cursor.execute(
                """
                INSERT INTO dbo.ThreatFindings
                    (event_id, rule_id, rule_name_snapshot,
                     category_snapshot, severity_snapshot, weight_snapshot,
                     is_critical_snapshot, confidence, evidence_summary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                event_id,
                rule["rule_id"],
                finding.rule_name,
                finding.category,
                finding.severity,
                finding.weight,
                finding.is_critical,
                finding.confidence,
                finding.evidence_summary,
            )

        connection.commit()

        return {
            "correlation_id": correlation_id,
            "risk_score": score,
            "decision": decision,
            "reason_code": reason,
            "findings": [
                {
                    "rule_name": f.rule_name,
                    "category": f.category,
                    "severity": f.severity,
                    "weight": f.weight,
                    "is_critical": f.is_critical,
                    "evidence_summary": f.evidence_summary,
                }
                for f in findings
            ],
        }

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
