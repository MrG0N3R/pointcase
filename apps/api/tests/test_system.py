import json
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from point.main import create_app
from point.core.config import Settings


def test_liveness_metadata_and_request_id(unit_settings):
    app = create_app(unit_settings)
    with TestClient(app) as client:
        identifier = str(uuid4())
        response = client.get("/health/live", headers={"X-Request-ID": identifier})
        assert response.json() == {"status": "ok"}
        assert response.headers["x-request-id"] == identifier
        assert response.headers["x-content-type-options"] == "nosniff"
        meta = client.get("/api/v1/meta", headers={"X-Request-ID": "untrusted-value"})
        assert meta.json()["defaults"]["currency"] == "MXN"
        assert meta.json()["phase"] == 2
        UUID(meta.headers["x-request-id"])
        assert unit_settings.database_url.get_secret_value() not in meta.text


def test_installation_defaults_are_configurable(unit_settings):
    config = Settings(_env_file=None, database_url=unit_settings.database_url, app_name="POINT Test", default_locale="en-US", default_currency="USD", default_timezone="UTC")
    with TestClient(create_app(config)) as client:
        body = client.get("/api/v1/meta").json()
        assert body["name"] == "POINT Test"
        assert body["defaults"] == {"locale": "en-US", "currency": "USD", "timezone": "UTC"}


def test_readiness_unavailable_never_leaks_connection(unit_settings):
    class Unavailable:
        def connect(self):
            raise OperationalError("private-db-address", {}, RuntimeError("credential-marker"))
    with TestClient(create_app(unit_settings, engine=Unavailable())) as client:
        response = client.get("/health/ready")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable", "checks": {"database": False, "migrations": False}}
        assert "credential-marker" not in response.text
        assert "private-db-address" not in response.text
        assert client.get("/health/live").status_code == 200


def test_errors_and_logs_exclude_sensitive_input(unit_settings, capsys):
    app = create_app(unit_settings)
    @app.get("/_test/error")
    def failure():
        raise RuntimeError("private-error-marker")
    @app.get("/_test/query")
    def query(amount: int):
        return {"amount": amount}
    with TestClient(app) as client:
        missing = client.get("/unmatched-private-id?secret=query-marker")
        assert missing.status_code == 404
        assert missing.json()["error"]["code"] == "NOT_FOUND"
        failure_response = client.get("/_test/error")
        assert failure_response.status_code == 500
        assert failure_response.json()["error"]["request_id"] == failure_response.headers["x-request-id"]
        validation = client.get("/_test/query?amount=private-input-marker")
        assert validation.status_code == 422
        assert "private-input-marker" not in validation.text
    logs = capsys.readouterr().err
    for marker in ("query-marker", "private-input-marker", "private-error-marker", "unmatched-private-id"):
        assert marker not in logs
        assert marker not in failure_response.text
    events = [json.loads(line) for line in logs.splitlines() if line.strip()]
    assert any(event["event"] == "request_failed" for event in events)


def test_cors_allows_only_configured_origin(unit_settings):
    with TestClient(create_app(unit_settings)) as client:
        allowed = client.get("/api/v1/meta", headers={"Origin": "http://127.0.0.1:5173"})
        denied = client.get("/api/v1/meta", headers={"Origin": "https://untrusted.example"})
        assert allowed.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
        assert "access-control-allow-origin" not in denied.headers


def test_production_does_not_publish_developer_docs(unit_settings):
    production = Settings(_env_file=None, environment="production", database_url=unit_settings.database_url, cors_origins=["https://point.example"])
    with TestClient(create_app(production)) as client:
        assert client.get("/api/docs").status_code == 404
        assert client.get("/api/v1/openapi.json").status_code == 404


def test_packaged_layout_loads_without_repository_ancestors(tmp_path, unit_settings):
    import os
    import shutil
    import subprocess
    import sys
    from pathlib import Path
    package = tmp_path / "service"
    package.mkdir()
    shutil.copytree(Path(__file__).resolve().parents[1] / "point", package / "point", ignore=shutil.ignore_patterns("__pycache__"))
    environment = {**os.environ, "POINT_ENVIRONMENT": "test", "POINT_DATABASE_URL": unit_settings.database_url.get_secret_value()}
    result = subprocess.run([sys.executable, "-c", "from pathlib import Path; from point.core.config import PROJECT_ROOT; from point.main import create_app; assert PROJECT_ROOT == Path.cwd(); app = create_app(); assert app.version == '0.2.0'; app.state.engine.dispose()"], cwd=package, env=environment, capture_output=True, text=True)
    assert result.returncode == 0, "La API debe poder cargarse fuera del árbol del repositorio."


@pytest.mark.parametrize("changes", [{"cors_origins": ["*"]}, {"default_timezone": "Invalid/NoSuchZone"}, {"database_url": "sqlite:///test.db"}, {"environment": "production", "cors_origins": ["http://point.example"]}])
def test_invalid_configuration_is_rejected(unit_settings, changes):
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        Settings(_env_file=None, database_url=changes.pop("database_url", unit_settings.database_url), **changes)
