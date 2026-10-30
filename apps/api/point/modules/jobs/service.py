from uuid import UUID
from sqlalchemy.orm import Session
from point.modules.jobs.models import OutboxEvent


def enqueue(session: Session, *, tenant_id: UUID, operation_key: str, event_type: str, payload: dict) -> OutboxEvent:
    """Join the caller's transaction; never commit independently or send externally.

    The unique tenant/operation key rejects duplicate insertions. This is an internal
    durable outbox foundation, not a public enqueue API or a running job worker.
    """
    if not operation_key or len(operation_key) > 128 or not event_type or len(event_type) > 80:
        raise ValueError("Invalid event identity.")
    event = OutboxEvent(tenant_id=tenant_id, operation_key=operation_key, event_type=event_type, payload=payload)
    session.add(event)
    session.flush()
    return event
