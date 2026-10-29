
from app.database import get_connection


def get_security_summary() -> dict:
    """Return aggregate security metrics from Azure SQL."""
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) AS total_events,
                SUM(CASE WHEN decision = 'Block' THEN 1 ELSE 0 END)
                    AS blocked_events,
                SUM(CASE WHEN decision = 'Allow' THEN 1 ELSE 0 END)
                    AS allowed_events,
                AVG(CAST(risk_score AS FLOAT)) AS average_risk
            FROM dbo.SecurityEvents
        """)

        row = cursor.fetchone()

        return {
            "total_events": int(row[0] or 0),
            "blocked_events": int(row[1] or 0),
            "allowed_events": int(row[2] or 0),
            "average_risk": round(float(row[3] or 0), 2),
        }
    finally:
        connection.close()
