"""Project-owned PostgreSQL only. Never uses or changes an installed DB service."""
import argparse
import os
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import psycopg
from configure_env import ensure_env
from psycopg import sql
from dotenv import dotenv_values
from sqlalchemy.engine import make_url

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / ".local"
DATA = LOCAL / "postgres/data"
ADMIN_FILE = LOCAL / "postgres/admin.secret"
FLAGS = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def config():
    if not (ROOT / ".env").is_file():
        raise RuntimeError("Falta .env. Primero ejecuta local.py setup.")
    return {**dotenv_values(ROOT / ".env"), **{key: value for key, value in os.environ.items() if key.startswith(("POINT_", "POSTGRES_"))}}


def pg_bin():
    configured = os.environ.get("POINT_PG_BIN")
    installed = shutil.which("pg_ctl")
    candidates = [Path(configured)] if configured else []
    if installed:
        candidates.append(Path(installed).parent)
    candidates.append(Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "PostgreSQL/18/bin")
    for candidate in candidates:
        if (candidate / ("pg_ctl.exe" if os.name == "nt" else "pg_ctl")).exists():
            return candidate
    raise RuntimeError("No se encontró PostgreSQL. Configura POINT_PG_BIN o usa Docker Compose.")


def run_pg(name, args, *, password=None, check=True):
    executable = pg_bin() / (name + (".exe" if os.name == "nt" else ""))
    env = os.environ.copy()
    if password:
        env["PGPASSWORD"] = password
    # A detached Windows postgres can inherit pipes from pg_ctl and hold communicate()
    # open after startup. Send startup output to the null device; postgres has its log.
    startup = name == "pg_ctl" and "start" in args
    result = subprocess.run([str(executable), *map(str, args)], cwd=ROOT, env=env,
                            stdout=subprocess.DEVNULL if startup else subprocess.PIPE,
                            stderr=subprocess.DEVNULL if startup else subprocess.PIPE,
                            text=True, encoding="utf-8", errors="replace", creationflags=FLAGS, timeout=120)
    if check and result.returncode:
        # Commands and stderr can include connection data; never print them automatically.
        raise RuntimeError(f"{name} no pudo completar la operación (código {result.returncode}). Revisa .local/postgres/server.log si corresponde.")
    return result


def verify_data_path():
    if DATA.resolve() != (ROOT.resolve() / ".local/postgres/data").resolve():
        raise RuntimeError("La ruta de PostgreSQL debe permanecer dentro del proyecto.")


def owned_admin():
    """Only return an admin connection after verifying the exact project data directory."""
    verify_data_path()
    cfg = config()
    if not ADMIN_FILE.is_file() or not (DATA / "PG_VERSION").is_file():
        raise RuntimeError("No existe un clúster local administrado por este proyecto.")
    connection = psycopg.connect(host="127.0.0.1", port=int(cfg["POSTGRES_PORT"]), user="point_local_admin",
                                  password=ADMIN_FILE.read_text().strip(), dbname="postgres", autocommit=True, connect_timeout=3)
    actual = Path(connection.execute("SHOW data_directory").fetchone()[0]).resolve()
    if os.path.normcase(str(actual)) != os.path.normcase(str(DATA.resolve())):
        connection.close()
        raise RuntimeError("Se rechazó una conexión que no pertenece al proyecto.")
    return connection


def create_database(connection, name, owner):
    if not name.startswith("point_") or not all(char.islower() or char.isdigit() or char == "_" for char in name):
        raise RuntimeError("La base local debe tener un nombre propio point_*.")
    if connection.execute("SELECT 1 FROM pg_database WHERE datname = %s", (name,)).fetchone():
        return False
    connection.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(sql.Identifier(name), sql.Identifier(owner)))
    return True


def setup():
    verify_data_path()
    LOCAL.mkdir(exist_ok=True)
    ensure_env()
    cfg = config()
    url = make_url(cfg["POINT_DATABASE_URL"])
    if url.host != "127.0.0.1" or url.database != "point_dev" or url.username != "point" or url.port != int(cfg["POSTGRES_PORT"]) or url.password != cfg["POSTGRES_PASSWORD"]:
        raise RuntimeError("El asistente local requiere la configuración point_dev/point en 127.0.0.1. No modificará una conexión personalizada.")
    ADMIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not (DATA / "PG_VERSION").exists():
        if DATA.exists() and any(DATA.iterdir()):
            raise RuntimeError("El directorio de datos no está vacío. No se modificará automáticamente.")
        if not ADMIN_FILE.exists():
            ADMIN_FILE.write_text(secrets.token_hex(32), encoding="utf-8")
        run_pg("initdb", ["-D", DATA, "-U", "point_local_admin", f"--pwfile={ADMIN_FILE}", "--auth=scram-sha-256", "--encoding=UTF8", "--locale=C"])
    if run_pg("pg_ctl", ["-D", DATA, "status"], check=False).returncode:
        run_pg("pg_ctl", ["-D", DATA, "-l", LOCAL / "postgres/server.log", "-o", f"-h 127.0.0.1 -p {int(cfg['POSTGRES_PORT'])}", "-w", "start"])
    with owned_admin() as admin:
        if not admin.execute("SELECT 1 FROM pg_roles WHERE rolname = 'point'").fetchone():
            admin.execute(sql.SQL("CREATE ROLE point LOGIN PASSWORD {}").format(sql.Literal(url.password)))
        create_database(admin, "point_dev", "point")
        create_database(admin, "point_test", "point")
    print("PostgreSQL del proyecto listo. Bases de desarrollo y pruebas separadas; credenciales guardadas en .env sin mostrarlas.")


def migrate():
    result = subprocess.run([sys.executable, "-m", "alembic", "-c", str(ROOT / "apps/api/alembic.ini"), "upgrade", "head"], cwd=ROOT)
    if result.returncode:
        raise RuntimeError("No se pudieron aplicar las migraciones.")
    print("Migraciones aplicadas.")


def backup(destination=None, database_url=None):
    url = make_url(database_url or config()["POINT_DATABASE_URL"])
    destination = Path(destination) if destination else LOCAL / "backups" / f"point-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}.dump"
    destination = destination.resolve()
    if destination.exists():
        raise RuntimeError("El respaldo de destino ya existe; no se sobrescribirá.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    run_pg("pg_dump", ["-h", url.host, "-p", url.port or 5432, "-U", url.username, "-d", url.database,
                        "--format=custom", "--no-owner", "--no-privileges", "--file", destination], password=url.password)
    print(f"Respaldo creado: {destination}")
    return destination


def restore_check(archive):
    """Restore to a newly created, owned database, never over existing application data."""
    archive = Path(archive).resolve()
    if not archive.is_file():
        raise RuntimeError("No se encontró el respaldo.")
    cfg = config()
    source = make_url(cfg["POINT_DATABASE_URL"])
    name = f"point_restore_{datetime.now(timezone.utc):%Y%m%d_%H%M%S}_{secrets.token_hex(3)}"
    with owned_admin() as admin:
        if not create_database(admin, name, "point"):
            raise RuntimeError("La base de restauración ya existe; se rechazó la operación.")
    run_pg("pg_restore", ["-h", "127.0.0.1", "-p", source.port or 5432, "-U", "point", "-d", name,
                           "--exit-on-error", "--single-transaction", "--no-owner", "--no-privileges", archive], password=source.password)
    url = source.set(database=name)
    with psycopg.connect(url.render_as_string(hide_password=False).replace("postgresql+psycopg://", "postgresql://")) as restored:
        revision = restored.execute("SELECT version_num FROM alembic_version").fetchone()[0]
        count = restored.execute("SELECT count(*) FROM outbox_events").fetchone()[0]
    print(f"Restauración independiente comprobada: {name}. Revisión {revision}; eventos {count}.")
    return url


def stop():
    verify_data_path()
    if not (DATA / "PG_VERSION").is_file():
        print("No hay PostgreSQL propio que detener.")
        return
    if run_pg("pg_ctl", ["-D", DATA, "status"], check=False).returncode:
        print("PostgreSQL del proyecto ya está detenido.")
        return
    run_pg("pg_ctl", ["-D", DATA, "-m", "fast", "-w", "stop"])
    print("PostgreSQL del proyecto detenido. No se eliminaron datos.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entorno local aislado de POINT")
    parser.add_argument("action", choices=["setup", "migrate", "backup", "restore-check", "stop"])
    parser.add_argument("--file", help="Destino de respaldo o archivo para restaurar")
    args = parser.parse_args()
    try:
        if args.action == "setup": setup()
        elif args.action == "migrate": migrate()
        elif args.action == "backup": backup(args.file)
        elif args.action == "restore-check":
            if not args.file: raise RuntimeError("Indica el archivo de respaldo con --file.")
            restore_check(args.file)
        else: stop()
    except Exception as exc:
        print(str(exc) if isinstance(exc, RuntimeError) else f"La operación no se completó ({type(exc).__name__}). No se muestran datos de conexión.", file=sys.stderr)
        raise SystemExit(1)
