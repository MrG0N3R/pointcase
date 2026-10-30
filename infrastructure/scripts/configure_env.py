"""Generate only project-local development credentials; preserve existing values."""
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def ensure_env():
    path = ROOT / ".env"
    if not path.exists():
        content = (ROOT / ".env.example").read_text(encoding="utf-8")
        content = content.replace("REPLACE_WITH_GENERATED_PASSWORD", secrets.token_hex(24))
        content = content.replace("REPLACE_WITH_GENERATED_ADMIN_PASSWORD", secrets.token_hex(32))
    else:
        content = path.read_text(encoding="utf-8")
    keys = {line.split("=", 1)[0] for line in content.splitlines() if "=" in line and not line.startswith("#")}
    if "POSTGRES_ADMIN_PASSWORD" not in keys:
        content += f"\nPOSTGRES_ADMIN_PASSWORD={secrets.token_hex(32)}\n"
    if "POINT_TEST_DATABASE_URL" not in keys:
        url = next((line.split("=", 1)[1] for line in content.splitlines() if line.startswith("POINT_DATABASE_URL=")), "")
        if url:
            content += f"\nPOINT_TEST_DATABASE_URL={url.rsplit('/', 1)[0]}/point_test\n"
    path.write_text(content, encoding="utf-8")
    return path


if __name__ == "__main__":
    ensure_env()
    print("Configuración local preparada; valores existentes conservados y secretos sin mostrar.")
