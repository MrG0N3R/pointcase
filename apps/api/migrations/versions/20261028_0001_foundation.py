"""Durable internal outbox; tenant records and access are added in phase 03."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20261028_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("outbox_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("operation_key", sa.String(128), nullable=False),
        sa.Column("event_type", sa.String(80), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("status", sa.String(16), server_default="pending", nullable=False),
        sa.Column("attempts", sa.Integer(), server_default="0", nullable=False),
        sa.Column("available_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_outbox_events"),
        sa.UniqueConstraint("tenant_id", "operation_key", name="uq_outbox_tenant_operation"),
        sa.CheckConstraint("attempts >= 0", name=op.f("ck_outbox_events_nonnegative_attempts")),
        sa.CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed')", name=op.f("ck_outbox_events_valid_status")),
    )
    op.create_index("ix_outbox_pending", "outbox_events", ["available_at"], postgresql_where=sa.text("status = 'pending'"))


def downgrade():
    op.drop_index("ix_outbox_pending", table_name="outbox_events")
    op.drop_table("outbox_events")
