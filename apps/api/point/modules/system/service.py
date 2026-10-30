from pathlib import Path
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from point.modules.system.schemas import HealthChecks, Readiness

API_ROOT = Path(__file__).resolve().parents[3]


def expected_heads() -> set[str]:
    config = Config(str(API_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(API_ROOT / "migrations"))
    return set(ScriptDirectory.from_config(config).get_heads())


def check_readiness(engine) -> Readiness:
    checks = HealthChecks(database=False, migrations=False)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            checks.database = True
            checks.migrations = set(MigrationContext.configure(connection).get_current_heads()) == expected_heads()
    except SQLAlchemyError:
        # No database addresses, credentials or SQL error text go to the public response.
        pass
    return Readiness(status="ok" if checks.database and checks.migrations else "unavailable", checks=checks)
