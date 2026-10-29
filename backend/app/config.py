from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PromptShield"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:5173"

    azure_sql_server: str = ""
    azure_sql_database: str = "PromptShield"
    azure_sql_username: str = ""
    azure_sql_password: str = ""
    azure_sql_driver: str = "ODBC Driver 18 for SQL Server"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
