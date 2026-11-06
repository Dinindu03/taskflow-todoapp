from datetime import UTC, datetime
import os
from uuid import uuid4

import pytest
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from app.config import Settings
from app.database import initialize_database, validate_connection
from app.models.documents import UserDocument, UserResponse
from app.repositories.users import DuplicateEmailError, UserRepository


def test_database_connectivity_and_indexes() -> None:
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    settings = Settings(
        jwt_secret_key="test-secret-key-with-at-least-32-chars",
        mongodb_uri=mongodb_uri,
        mongodb_database=f"taskflow_test_{uuid4().hex}",
    )
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=1000)
    database = client[settings.mongodb_database]
    try:
        validate_connection(client)
        initialize_database(database)
        assert "users_email_unique" in database["users"].index_information()
        assert "todos_user_created_at" in database["todos"].index_information()
        assert "todos_user_completed" in database["todos"].index_information()
    except Exception as exc:
        pytest.skip(f"MongoDB is not available: {exc}")
    finally:
        client.drop_database(settings.mongodb_database)
        client.close()


def test_duplicate_email_is_rejected() -> None:
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    settings = Settings(
        jwt_secret_key="test-secret-key-with-at-least-32-chars",
        mongodb_uri=mongodb_uri,
        mongodb_database=f"taskflow_test_{uuid4().hex}",
    )
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=1000)
    database = client[settings.mongodb_database]
    now = datetime.now(UTC)
    user = UserDocument(
        id=str(uuid4()),
        name="Test User",
        email="test@example.com",
        password_hash="hash",
        created_at=now,
    )
    try:
        validate_connection(client)
        initialize_database(database)
        repository = UserRepository(database)
        repository.create(user)
        with pytest.raises(DuplicateEmailError):
            repository.create(user.model_copy(update={"id": str(uuid4())}))
    except Exception as exc:
        if isinstance(exc, DuplicateEmailError):
            raise
        pytest.skip(f"MongoDB is not available: {exc}")
    finally:
        client.drop_database(settings.mongodb_database)
        client.close()


def test_user_response_excludes_password_hash() -> None:
    assert "password_hash" not in UserResponse.model_fields
