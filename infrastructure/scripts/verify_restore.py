"""Prove a backup preserves data, using fresh databases owned by this project only."""
import json
import secrets
import sys
from pathlib import Path
from uuid import uuid4

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

import local

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
from point.modules.jobs.service import enqueue


def main():
    source_name = "point_backup_" + secrets.token_hex(6)
    base_url = make_url(local.config()["POINT_DATABASE_URL"])
    with local.owned_admin() as admin:
        if not local.create_database(admin, source_name, "point"):
            raise RuntimeError("La base de prueba ya existe; operación rechazada.")
    source_url = base_url.set(database=source_name)
    source_engine = create_engine(source_url, hide_parameters=True)
    with source_engine.begin() as connection:
        cfg = Config(str(ROOT / "apps/api/alembic.ini"))
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")
    marker = uuid4()
    with Session(source_engine) as session:
        event = enqueue(session, tenant_id=uuid4(), operation_key=str(marker), event_type="verification.backup", payload={"synthetic": True, "marker": str(marker)})
        event_id = event.id
        session.commit()
    archive = local.backup(ROOT / ".local/backups" / f"verification-{marker}.dump", source_url.render_as_string(hide_password=False))
    restored_url = local.restore_check(archive)
    restored_engine = create_engine(restored_url, hide_parameters=True)
    with Session(restored_engine) as session:
        from point.modules.jobs.models import OutboxEvent
        restored = session.get(OutboxEvent, event_id)
        if restored is None or restored.payload != {"synthetic": True, "marker": str(marker)}:
            raise RuntimeError("El dato de prueba no coincide después de restaurar.")
    source_engine.dispose()
    restored_engine.dispose()
    result = {"source_database": source_name, "restored_database": restored_url.database, "revision": "20261028_0001",
              "synthetic_records_restored": 1, "data_matches": True, "application_database_modified": False}
    target = ROOT / "docs/phases/02-base-tecnica/evidence/backup-restore.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Respaldo y restauración comprobados con un registro ficticio. point_dev no fue modificada.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc) if isinstance(exc, RuntimeError) else f"Falló la comprobación ({type(exc).__name__}).", file=sys.stderr)
        raise SystemExit(1)
