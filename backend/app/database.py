
import time
import logging

import pyodbc

from app.config import settings

logger = logging.getLogger(__name__)

# Maximum connection attempts when Azure SQL is temporarily unavailable.
MAX_CONNECTION_ATTEMPTS = 5

# Delay between attempts, in seconds.
RETRY_DELAYS = [2, 4, 8, 12]


def get_connection():
    required = {
        "AZURE_SQL_SERVER": settings.azure_sql_server,
        "AZURE_SQL_DATABASE": settings.azure_sql_database,
        "AZURE_SQL_USERNAME": settings.azure_sql_username,
        "AZURE_SQL_PASSWORD": settings.azure_sql_password,
    }

    missing = [
        key for key, value in required.items()
        if not value.strip()
    ]

    if missing:
        raise RuntimeError(
            "Missing required database configuration: "
            + ", ".join(missing)
        )

    connection_string = (
        f"DRIVER={{{settings.azure_sql_driver}}};"
        f"SERVER=tcp:{settings.azure_sql_server},1433;"
        f"DATABASE={settings.azure_sql_database};"
        f"UID={settings.azure_sql_username};"
        f"PWD={settings.azure_sql_password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=15;"
    )

    for attempt in range(MAX_CONNECTION_ATTEMPTS):
        try:
            return pyodbc.connect(connection_string)

        except pyodbc.Error as exc:
            error_message = str(exc)

            # Retry only errors commonly associated with
            # temporary Azure SQL availability or connectivity.
            retryable_codes = (
                "40613",
                "40197",
                "40501",
                "10928",
                "10929",
                "08S01",
                "08001",
                "HYT00",
                "HYT01",
            )

            is_retryable = any(
                code in error_message
                for code in retryable_codes
            )

            if not is_retryable:
                raise

            if attempt == MAX_CONNECTION_ATTEMPTS - 1:
                logger.exception(
                    "Azure SQL connection failed after all retry attempts"
                )
                raise

            delay = RETRY_DELAYS[attempt]

            logger.warning(
                "Temporary Azure SQL connection failure. "
                "Retrying attempt %s/%s in %s seconds.",
                attempt + 1,
                MAX_CONNECTION_ATTEMPTS,
                delay,
            )

            time.sleep(delay)

    raise RuntimeError("Unable to establish database connection")


def check_database_connection() -> bool:
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")

        result = cursor.fetchone()

        return result is not None and result[0] == 1

    finally:
        if connection is not None:
            connection.close()
