from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from point.core.config import Settings


def build_engine(settings: Settings):
    return create_engine(
        settings.database_url.get_secret_value(), pool_pre_ping=True, pool_size=5, max_overflow=5,
        hide_parameters=True, echo=False,
        connect_args={"connect_timeout": 3, "options": "-c statement_timeout=3000"},
    )


def session_factory(engine):
    return sessionmaker(bind=engine, expire_on_commit=False)
