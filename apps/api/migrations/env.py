from alembic import context
from sqlalchemy import create_engine, pool
from point.core.config import Settings
from point.db.base import Base
from point.modules.jobs.models import OutboxEvent  # noqa: F401

settings = Settings()
target_metadata = Base.metadata

if context.is_offline_mode():
    context.configure(url=settings.database_url.get_secret_value(), target_metadata=target_metadata,
                      literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()
else:
    def migrate_connection(connection):
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

    supplied = context.config.attributes.get("connection")
    if supplied is not None:
        migrate_connection(supplied)
    else:
        engine = create_engine(settings.database_url.get_secret_value(), poolclass=pool.NullPool, hide_parameters=True)
        with engine.connect() as connection:
            migrate_connection(connection)
        engine.dispose()
