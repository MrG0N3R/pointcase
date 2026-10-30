"""Export deterministic public contracts without opening a database connection."""
import json
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
from point.core.config import Settings
from point.main import create_app

config = Settings(_env_file=None, environment="test", database_url=f"postgresql+psycopg://contracts:{secrets.token_hex(8)}@127.0.0.1:1/point_contracts")
application = create_app(config)
destination = ROOT / "docs/api/openapi.json"
output = json.dumps(application.openapi(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
if "--check" in sys.argv:
    if not destination.exists() or destination.read_text(encoding="utf-8") != output:
        raise SystemExit("OpenAPI desactualizado. Ejecuta export_openapi.py.")
else:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="utf-8")
application.state.engine.dispose()
print("Contrato OpenAPI verificado." if "--check" in sys.argv else "Contrato OpenAPI exportado.")
