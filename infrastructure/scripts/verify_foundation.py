"""Check local deliverable integrity; never render credentials or resolved Compose env."""
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote
from zoneinfo import ZoneInfo

import yaml
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
ignored = [".env", ".local/postgres/data/PG_VERSION", ".venv/pyvenv.cfg", "node_modules/.package-lock.json"]
for filename in ignored:
    result = subprocess.run(["git", "check-ignore", "--quiet", filename], cwd=ROOT)
    if result.returncode:
        raise SystemExit(f"Falta ignorar estado privado o generado: {filename}")

names = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).decode("utf-8").split("\0")
files = [ROOT / name for name in names if name and (ROOT / name).is_file()]
env = dotenv_values(ROOT / ".env")
secrets = [env[key] for key in ("POSTGRES_PASSWORD", "POSTGRES_ADMIN_PASSWORD") if env.get(key)]
admin_file = ROOT / ".local/postgres/admin.secret"
if admin_file.exists():
    secrets.append(admin_file.read_text().strip())
frontend = list((ROOT / "apps/web/dist").rglob("*")) if (ROOT / "apps/web/dist").exists() else []
for filename in [*files, *[file for file in frontend if file.is_file()]]:
    body = filename.read_bytes()
    if any(secret.encode() in body for secret in secrets if len(secret) > 16):
        raise SystemExit(f"Se encontró un valor privado en {filename.relative_to(ROOT)}; no se muestra su contenido.")

links = 0
for filename in files:
    if filename.suffix != ".md" or filename.name.startswith("POINT_Todo_"):
        continue
    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", filename.read_text(encoding="utf-8")):
        value = match.group(1).split("#", 1)[0]
        if not value or re.match(r"[a-z]+:", value, re.I):
            continue
        links += 1
        if not (filename.parent / unquote(value)).resolve().exists():
            raise SystemExit(f"Enlace local inválido en {filename.relative_to(ROOT)}: {value}")

master = ROOT / "POINT_Todo_en_Uno_Prompt_Maestro_PyMEs_Mexico.md"
assert hashlib.sha256(master.read_bytes()).hexdigest() == "39939b592e4e1de51f9ba3be314918feb9c8a72e7a7bcc738ae373085a5a1f71"
assert (ROOT / "prototypes/phase-01/POINT-Prototipo.html").read_bytes() == (ROOT / "apps/web/public/diseno/index.html").read_bytes()
compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
for service in compose["services"].values():
    if "build" in service:
        assert (ROOT / service["build"]["dockerfile"]).is_file()
assert yaml.safe_load((ROOT / ".github/workflows/ci.yml").read_text())["jobs"]["verify"]["steps"]
report = {"date": datetime.now(ZoneInfo("America/Mexico_City")).date().isoformat(), "local_links_checked": links, "master_unchanged": True, "approved_prototype_preserved": True,
          "private_state_ignored": True, "local_secrets_absent_from_source_and_web_build": True,
          "compose_yaml_and_paths_checked": True, "docker_runtime_executed": False, "remote_ci_executed": False}
destination = ROOT / "docs/phases/02-base-tecnica/evidence/project-checks.json"
destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
