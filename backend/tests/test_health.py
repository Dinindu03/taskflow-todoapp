import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-chars")

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "taskflow-api"}
