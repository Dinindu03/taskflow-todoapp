import os
from uuid import uuid4

import pytest
from pymongo import MongoClient


TEST_DATABASE = f"taskflow_test_{uuid4().hex}"
os.environ["MONGODB_DATABASE"] = TEST_DATABASE
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-chars")


@pytest.fixture(scope="session", autouse=True)
def isolated_database() -> None:
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=1000)
    try:
        client.admin.command("ping")
    except Exception as exc:
        client.close()
        pytest.skip(f"MongoDB is not available: {exc}")

    try:
        yield
    finally:
        client.drop_database(TEST_DATABASE)
        client.close()
