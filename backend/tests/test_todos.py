import os
from uuid import uuid4

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-chars")

from fastapi.testclient import TestClient

from app.main import app


ORIGIN = "http://localhost:8000"


def authenticated_client(client: TestClient, email: str) -> str:
    signup = client.post(
        "/api/auth/signup",
        headers={"Origin": ORIGIN},
        json={"name": "Todo User", "email": email, "password": "secure-password"},
    )
    assert signup.status_code == 201
    signin = client.post(
        "/api/auth/signin",
        headers={"Origin": ORIGIN},
        json={"email": email, "password": "secure-password"},
    )
    assert signin.status_code == 200
    return client.cookies.get("taskflow_csrf")


def state_headers(csrf: str) -> dict[str, str]:
    return {"Origin": ORIGIN, "X-CSRF-Token": csrf}


def test_todo_crud_and_status_operations() -> None:
    with TestClient(app) as client:
        csrf = authenticated_client(client, f"todo-{uuid4().hex}@example.com")
        headers = state_headers(csrf)

        created = client.post(
            "/api/todos",
            headers=headers,
            json={"title": " Plan release ", "description": " Ship MVP "},
        )
        assert created.status_code == 201
        todo = created.json()
        assert todo["title"] == "Plan release"
        assert todo["description"] == "Ship MVP"
        assert todo["completed"] is False
        todo_id = todo["id"]

        listed = client.get("/api/todos")
        assert listed.status_code == 200
        assert [item["id"] for item in listed.json()] == [todo_id]

        fetched = client.get(f"/api/todos/{todo_id}")
        assert fetched.status_code == 200

        updated = client.put(
            f"/api/todos/{todo_id}",
            headers=headers,
            json={"title": "Release MVP", "description": "Ship the MVP"},
        )
        assert updated.status_code == 200
        assert updated.json()["title"] == "Release MVP"

        completed = client.patch(f"/api/todos/{todo_id}/complete", headers=headers)
        assert completed.status_code == 200
        assert completed.json()["completed"] is True

        pending = client.patch(f"/api/todos/{todo_id}/pending", headers=headers)
        assert pending.status_code == 200
        assert pending.json()["completed"] is False

        deleted = client.delete(f"/api/todos/{todo_id}", headers=headers)
        assert deleted.status_code == 204
        assert client.get(f"/api/todos/{todo_id}").status_code == 404


def test_todo_ownership_isolation() -> None:
    with TestClient(app) as owner, TestClient(app) as other:
        owner_csrf = authenticated_client(owner, f"owner-{uuid4().hex}@example.com")
        other_csrf = authenticated_client(other, f"other-{uuid4().hex}@example.com")
        created = owner.post(
            "/api/todos",
            headers=state_headers(owner_csrf),
            json={"title": "Private task", "description": ""},
        )
        todo_id = created.json()["id"]

        assert other.get(f"/api/todos/{todo_id}").status_code == 404
        assert other.put(
            f"/api/todos/{todo_id}",
            headers=state_headers(other_csrf),
            json={"title": "Tampered", "description": ""},
        ).status_code == 404
        assert other.patch(
            f"/api/todos/{todo_id}/complete",
            headers=state_headers(other_csrf),
        ).status_code == 404
        assert other.delete(
            f"/api/todos/{todo_id}", headers=state_headers(other_csrf)
        ).status_code == 404
        assert owner.get(f"/api/todos/{todo_id}").status_code == 200


def test_todo_validation_and_authentication() -> None:
    with TestClient(app) as client:
        assert client.get("/api/todos").status_code == 401
        assert client.post(
            "/api/todos",
            headers={"Origin": ORIGIN},
            json={"title": "Unauthenticated", "description": ""},
        ).status_code == 403
        csrf = authenticated_client(client, f"validation-{uuid4().hex}@example.com")
        response = client.post(
            "/api/todos",
            headers=state_headers(csrf),
            json={"title": ""},
        )
        assert response.status_code == 400


def test_missing_todo_returns_not_found() -> None:
    with TestClient(app) as client:
        csrf = authenticated_client(client, f"missing-{uuid4().hex}@example.com")
        missing_id = str(uuid4())
        assert client.get(f"/api/todos/{missing_id}").status_code == 404
        assert client.put(
            f"/api/todos/{missing_id}",
            headers=state_headers(csrf),
            json={"title": "Missing", "description": ""},
        ).status_code == 404
        assert client.delete(
            f"/api/todos/{missing_id}",
            headers=state_headers(csrf),
        ).status_code == 404
