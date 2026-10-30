import os
import secrets
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from point.core.config import Settings

API = Path(__file__).resolve().parents[1]
ROOT = API.parents[1]


@pytest.fixture
def unit_settings():
    return Settings(_env_file=None, environment="test", app_name="POINT TODO EN UNO",
                    default_locale="es-MX", default_currency="MXN", default_timezone="America/Mexico_City",
                    cors_origins=["http://127.0.0.1:5173"],
                    database_url=f"postgresql+psycopg://test:{secrets.token_hex(12)}@127.0.0.1:1/point_test")


@pytest.fixture(scope="session")
def db_engine():
    raw = os.getenv("POINT_TEST_DATABASE_URL") or dotenv_values(ROOT / ".env").get("POINT_TEST_DATABASE_URL")
    if not raw:
        pytest.skip("POINT_TEST_DATABASE_URL no configurada; integración PostgreSQL pendiente.")
    url = make_url(raw)
    if url.database != "point_test":
        pytest.fail("Integración solo permite la base aislada point_test; se rechazó otra base.")
    engine = create_engine(url, hide_parameters=True, pool_pre_ping=True)
    config = Config(str(API / "alembic.ini"))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "head")
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    with db_engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection) as session:
            yield session
        if transaction.is_active:
            transaction.rollback()
