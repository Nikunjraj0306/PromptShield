import pyodbc

from app.config import settings


def get_connection():
    required = {
        "AZURE_SQL_SERVER": settings.azure_sql_server,
        "AZURE_SQL_DATABASE": settings.azure_sql_database,
        "AZURE_SQL_USERNAME": settings.azure_sql_username,
        "AZURE_SQL_PASSWORD": settings.azure_sql_password,
    }

    missing = [key for key, value in required.items() if not value.strip()]
    if missing:
        raise RuntimeError(
            "Missing required database configuration: " + ", ".join(missing)
        )

    connection_string = (
        f"DRIVER={{{settings.azure_sql_driver}}};"
        f"SERVER=tcp:{settings.azure_sql_server},1433;"
        f"DATABASE={settings.azure_sql_database};"
        f"UID={settings.azure_sql_username};"
        f"PWD={settings.azure_sql_password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=10;"
    )

    return pyodbc.connect(connection_string)


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
