from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from point.modules.jobs.models import OutboxEvent
from point.modules.jobs.service import enqueue
from point.modules.system.service import check_readiness

pytestmark = pytest.mark.integration
API = Path(__file__).resolve().parents[1]


def test_postgresql_migration_and_readiness(db_engine):
    result = check_readiness(db_engine)
    assert result.status == "ok"
    assert result.checks.database and result.checks.migrations
    with db_engine.connect() as connection:
        assert connection.execute(text("SHOW server_version")).scalar().startswith("18.")
        assert connection.execute(text("SELECT rolsuper FROM pg_roles WHERE rolname = current_user")).scalar() is False


def test_outbox_is_part_of_the_callers_transaction(db_engine):
    tenant = uuid4()
    with Session(db_engine) as session:
        event = enqueue(session, tenant_id=tenant, operation_key="rollback-test", event_type="test.created", payload={"example": True})
        identifier = event.id
        session.rollback()
    with Session(db_engine) as session:
        assert session.get(OutboxEvent, identifier) is None


def test_same_key_can_exist_only_once_within_each_tenant(db_session):
    tenant = uuid4()
    enqueue(db_session, tenant_id=tenant, operation_key="operation-1", event_type="test.created", payload={})
    enqueue(db_session, tenant_id=uuid4(), operation_key="operation-1", event_type="test.created", payload={})
    with pytest.raises(IntegrityError):
        with db_session.begin_nested():
            enqueue(db_session, tenant_id=tenant, operation_key="operation-1", event_type="test.created", payload={})
    assert db_session.scalar(select(func.count()).select_from(OutboxEvent).where(OutboxEvent.operation_key == "operation-1")) == 2


def test_outbox_requires_tenant_and_nonnegative_attempts(db_session):
    for values in ({"tenant_id": None, "attempts": 0}, {"tenant_id": uuid4(), "attempts": -1}):
        with pytest.raises(IntegrityError):
            with db_session.begin_nested():
                db_session.add(OutboxEvent(operation_key=str(uuid4()), event_type="test.created", payload={}, **values))
                db_session.flush()


def test_migration_upgrade_downgrade_upgrade_in_disposable_schema(db_engine):
    schema = "test_migration_" + uuid4().hex
    with db_engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            connection.execute(text(f'SET LOCAL search_path TO "{schema}"'))
            config = Config(str(API / "alembic.ini"))
            config.attributes["connection"] = connection
            command.upgrade(config, "head")
            assert connection.execute(text("SELECT version_num FROM alembic_version")).scalar() == "20261028_0001"
            command.downgrade(config, "base")
            assert connection.execute(text("SELECT count(*) FROM pg_tables WHERE schemaname = :schema AND tablename = 'outbox_events'"), {"schema": schema}).scalar() == 0
            command.upgrade(config, "head")
            assert connection.execute(text("SELECT count(*) FROM outbox_events")).scalar() == 0
        finally:
            transaction.rollback()
