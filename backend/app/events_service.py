
from app.database import get_connection


def get_recent_events(limit: int = 50) -> list[dict]:
    """Return recent persisted inspection events and their findings."""
    if not 1 <= limit <= 100:
        raise ValueError("LIMIT_OUT_OF_RANGE")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT TOP (?)
                e.event_id,
                e.application_id,
                a.name AS application_name,
                e.endpoint_id,
                ep.path_pattern AS endpoint_path,
                ep.http_method AS endpoint_method,
                e.request_time,
                e.risk_score,
                e.decision,
                e.reason_code,
                e.correlation_id,
                e.request_path,
                e.processing_status
            FROM dbo.SecurityEvents AS e
            LEFT JOIN dbo.Applications AS a
                ON a.application_id = e.application_id
            LEFT JOIN dbo.Endpoints AS ep
                ON ep.endpoint_id = e.endpoint_id
            ORDER BY e.request_time DESC, e.event_id DESC
            """,
            limit,
        )

        rows = cursor.fetchall()
        events = []

        for row in rows:
            events.append(
                {
                    "event_id": int(row.event_id),
                    "application_id": int(row.application_id),
                    "application_name": row.application_name,
                    "endpoint_id": (
                        int(row.endpoint_id)
                        if row.endpoint_id is not None
                        else None
                    ),
                    "endpoint_path": row.endpoint_path,
                    "endpoint_method": row.endpoint_method,
                    "request_time": (
                        row.request_time.isoformat()
                        if row.request_time is not None
                        else None
                    ),
                    "risk_score": int(row.risk_score),
                    "decision": row.decision,
                    "reason_code": row.reason_code,
                    "correlation_id": str(row.correlation_id),
                    "request_path": row.request_path,
                    "processing_status": row.processing_status,
                    "findings": [],
                }
            )

        if not events:
            return events

        event_ids = [event["event_id"] for event in events]
        placeholders = ",".join("?" for _ in event_ids)

        cursor.execute(
            f"""
            SELECT
                event_id,
                rule_name_snapshot,
                category_snapshot,
                severity_snapshot,
                weight_snapshot,
                is_critical_snapshot,
                confidence,
                evidence_summary
            FROM dbo.ThreatFindings
            WHERE event_id IN ({placeholders})
            ORDER BY event_id DESC, finding_id ASC
            """,
            *event_ids,
        )

        findings_by_event = {event_id: [] for event_id in event_ids}

        for row in cursor.fetchall():
            findings_by_event[int(row.event_id)].append(
                {
                    "rule_name": row.rule_name_snapshot,
                    "category": row.category_snapshot,
                    "severity": row.severity_snapshot,
                    "weight": int(row.weight_snapshot),
                    "is_critical": bool(row.is_critical_snapshot),
                    "confidence": (
                        float(row.confidence)
                        if row.confidence is not None
                        else None
                    ),
                    "evidence_summary": row.evidence_summary,
                }
            )

        for event in events:
            event["findings"] = findings_by_event[event["event_id"]]

        return events

    finally:
        connection.close()
