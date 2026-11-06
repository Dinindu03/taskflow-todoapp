import os
from uuid import uuid4

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-chars")

from fastapi.testclient import TestClient

from app.main import app


ORIGIN = "http://localhost:8000"


def authenticate(client: TestClient, email: str) -> str:
    response = client.post(
        "/api/auth/signup",
        headers={"Origin": ORIGIN},
        json={"name": "Dashboard User", "email": email, "password": "secure-password"},
    )
    assert response.status_code == 201
    response = client.post(
        "/api/auth/signin",
        headers={"Origin": ORIGIN},
        json={"email": email, "password": "secure-password"},
    )
    assert response.status_code == 200
    return client.cookies.get("taskflow_csrf")


def mutation_headers(csrf: str) -> dict[str, str]:
    return {"Origin": ORIGIN, "X-CSRF-Token": csrf}


def create_todo(client: TestClient, csrf: str, title: str) -> str:
    response = client.post(
        "/api/todos",
        headers=mutation_headers(csrf),
        json={"title": title, "description": ""},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_dashboard_stats_are_user_scoped() -> None:
    with TestClient(app) as first, TestClient(app) as second:
        first_csrf = authenticate(first, f"stats-first-{uuid4().hex}@example.com")
        second_csrf = authenticate(second, f"stats-second-{uuid4().hex}@example.com")

        first_pending = create_todo(first, first_csrf, "First pending")
        first_completed = create_todo(first, first_csrf, "First completed")
        create_todo(second, second_csrf, "Second pending")
        second_completed = create_todo(second, second_csrf, "Second completed")

        complete = first.patch(
            f"/api/todos/{first_completed}/complete",
            headers=mutation_headers(first_csrf),
        )
        assert complete.status_code == 200
        complete = second.patch(
            f"/api/todos/{second_completed}/complete",
            headers=mutation_headers(second_csrf),
        )
        assert complete.status_code == 200

        assert first.get("/api/dashboard/stats").json() == {
            "total": 2,
            "completed": 1,
            "pending": 1,
        }
        assert second.get("/api/dashboard/stats").json() == {
            "total": 2,
            "completed": 1,
            "pending": 1,
        }
        assert first.get("/api/todos").json()[0]["id"] in {
            first_pending,
            first_completed,
        }


def test_dashboard_stats_require_authentication_and_support_empty_users() -> None:
    with TestClient(app) as client:
        assert client.get("/api/dashboard/stats").status_code == 401
        authenticate(client, f"empty-stats-{uuid4().hex}@example.com")
        response = client.get("/api/dashboard/stats")
        assert response.status_code == 200
        assert response.json() == {"total": 0, "completed": 0, "pending": 0}
