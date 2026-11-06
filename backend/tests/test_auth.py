import os
from uuid import uuid4

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-chars")

from fastapi.testclient import TestClient

from app.main import app


ORIGIN = "http://localhost:8000"


def test_signup_signin_me_and_logout() -> None:
    email = f"auth-{uuid4().hex}@example.com"
    with TestClient(app) as client:
        signup = client.post(
            "/api/auth/signup",
            headers={"Origin": ORIGIN},
            json={"name": "Auth User", "email": email, "password": "secure-password"},
        )
        assert signup.status_code == 201
        assert "password_hash" not in signup.text

        duplicate = client.post(
            "/api/auth/signup",
            headers={"Origin": ORIGIN},
            json={"name": "Other User", "email": email, "password": "secure-password"},
        )
        assert duplicate.status_code == 409

        signin = client.post(
            "/api/auth/signin",
            headers={"Origin": ORIGIN},
            json={"email": email, "password": "secure-password"},
        )
        assert signin.status_code == 200
        assert "password_hash" not in signin.text
        assert "taskflow_auth" in signin.cookies
        assert "taskflow_csrf" in signin.cookies

        current = client.get("/api/auth/me")
        assert current.status_code == 200
        assert current.json()["email"] == email
        assert "password_hash" not in current.text

        csrf_token = client.cookies.get("taskflow_csrf")
        logout = client.post(
            "/api/auth/logout",
            headers={"Origin": ORIGIN, "X-CSRF-Token": csrf_token},
        )
        assert logout.status_code == 204
        assert client.get("/api/auth/me").status_code == 401


def test_auth_rejects_bad_credentials_and_missing_origin() -> None:
    with TestClient(app) as client:
        signin = client.post(
            "/api/auth/signin",
            headers={"Origin": ORIGIN},
            json={"email": "missing@example.com", "password": "bad-password"},
        )
        assert signin.status_code == 401

        signup = client.post(
            "/api/auth/signup",
            json={"name": "No Origin", "email": "no-origin@example.com", "password": "secure-password"},
        )
        assert signup.status_code == 403


def test_signin_rejects_invalid_password() -> None:
    email = f"wrong-password-{uuid4().hex}@example.com"
    with TestClient(app) as client:
        signup = client.post(
            "/api/auth/signup",
            headers={"Origin": ORIGIN},
            json={"name": "Password User", "email": email, "password": "secure-password"},
        )
        assert signup.status_code == 201

        signin = client.post(
            "/api/auth/signin",
            headers={"Origin": ORIGIN},
            json={"email": email, "password": "incorrect-password"},
        )
        assert signin.status_code == 401
        assert signin.json()["error"]["message"] == "Invalid email or password."
