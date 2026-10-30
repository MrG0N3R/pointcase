from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url

API_ROOT = Path(__file__).resolve().parents[2]
# Both repository layout (apps/api) and packaged/container layout (/app) work.
PROJECT_ROOT = API_ROOT.parents[1] if API_ROOT.name == "api" and API_ROOT.parent.name == "apps" else API_ROOT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="POINT_", env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8",
        extra="ignore", hide_input_in_errors=True,
    )
    environment: Literal["development", "test", "production"] = "development"
    app_name: str = Field(default="POINT TODO EN UNO", min_length=1, max_length=80)
    database_url: SecretStr
    default_locale: str = Field(default="es-MX", pattern=r"^[a-z]{2}(?:-[A-Z]{2})?$")
    default_currency: str = Field(default="MXN", pattern=r"^[A-Z]{3}$")
    default_timezone: str = Field(default="America/Mexico_City", min_length=3, max_length=64)
    cors_origins: list[str] = ["http://127.0.0.1:5173"]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    @field_validator("default_timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError:
            raise ValueError("Usa una zona horaria IANA válida.") from None
        return value

    @field_validator("database_url")
    @classmethod
    def validate_database(cls, secret: SecretStr) -> SecretStr:
        try:
            url = make_url(secret.get_secret_value())
        except Exception:
            raise ValueError("Se requiere una conexión PostgreSQL válida.") from None
        if url.drivername != "postgresql+psycopg" or not url.host or not url.database:
            raise ValueError("Usa PostgreSQL con psycopg, servidor y base explícitos.")
        if not url.password or url.password == "REPLACE_WITH_GENERATED_PASSWORD":
            raise ValueError("Genera una contraseña local antes de iniciar.")
        return secret

    @field_validator("cors_origins")
    @classmethod
    def validate_origins(cls, origins: list[str]) -> list[str]:
        from urllib.parse import urlsplit
        for origin in origins:
            parsed = urlsplit(origin)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.path or parsed.query or parsed.fragment or parsed.username:
                raise ValueError("Los orígenes deben ser URLs explícitas, sin rutas ni credenciales.")
        return origins

    @model_validator(mode="after")
    def validate_production(self):
        if self.environment == "production" and any(not origin.startswith("https://") for origin in self.cors_origins):
            raise ValueError("En producción los orígenes deben usar HTTPS.")
        return self
