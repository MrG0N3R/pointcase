"""Run project API and web without global installs. Ctrl+C stops only these children."""
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
processes = []


def stop_children(*_):
    for process in reversed(processes):
        if process.poll() is None:
            process.terminate()
    for process in processes:
        try: process.wait(timeout=8)
        except subprocess.TimeoutExpired: process.kill()


def main():
    if not (ROOT / ".env").exists():
        raise SystemExit("Primero prepara .env y PostgreSQL; consulta DEPLOYMENT.md.")
    cfg = dotenv_values(ROOT / ".env")
    api_port = int(cfg.get("POINT_API_PORT", "8000"))
    web_port = int(cfg.get("POINT_WEB_PORT", "5173"))
    node = shutil.which("node")
    if not node or not (ROOT / "node_modules/vite/bin/vite.js").is_file():
        raise SystemExit("Faltan dependencias web. Ejecuta npm ci desde la raíz.")
    result = subprocess.run([node, str(ROOT / "infrastructure/scripts/prepare-web.mjs")], cwd=ROOT)
    if result.returncode: raise SystemExit(result.returncode)
    signal.signal(signal.SIGINT, stop_children)
    signal.signal(signal.SIGTERM, stop_children)
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        processes.append(subprocess.Popen([sys.executable, "-m", "uvicorn", "point.main:create_app", "--factory", "--app-dir", "apps/api", "--host", "127.0.0.1", "--port", str(api_port), "--no-access-log"], cwd=ROOT, creationflags=flags))
        processes.append(subprocess.Popen([node, str(ROOT / "node_modules/vite/bin/vite.js"), "--host", "127.0.0.1", "--port", str(web_port), "--strictPort"], cwd=ROOT / "apps/web", creationflags=flags))
        print(f"\nPOINT local: http://127.0.0.1:{web_port}\nDocumentación API: http://127.0.0.1:{api_port}/api/docs\nCtrl+C para detener web y API. PostgreSQL se conserva; local.py stop lo detiene.\n", flush=True)
        while all(process.poll() is None for process in processes):
            time.sleep(.3)
        failed = any(process.returncode not in {None, 0} for process in processes)
        return 1 if failed else 0
    finally:
        stop_children()


if __name__ == "__main__":
    raise SystemExit(main())
