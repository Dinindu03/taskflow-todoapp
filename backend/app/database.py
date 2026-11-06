from collections.abc import Mapping

from pymongo import MongoClient
from pymongo.database import Database

from app.config import Settings

USERS_COLLECTION = "users"
TODOS_COLLECTION = "todos"


def create_client(settings: Settings) -> MongoClient:
    return MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=2000)


def get_database(client: MongoClient, settings: Settings) -> Database:
    return client[settings.mongodb_database]


def validate_connection(client: MongoClient) -> None:
    client.admin.command("ping")


def initialize_database(database: Database) -> Mapping[str, str]:
    users = database[USERS_COLLECTION]
    todos = database[TODOS_COLLECTION]

    users.create_index("email", unique=True, name="users_email_unique")
    todos.create_index(
        [("user_id", 1), ("created_at", -1)],
        name="todos_user_created_at",
    )
    todos.create_index(
        [("user_id", 1), ("completed", 1)],
        name="todos_user_completed",
    )

    return {
        "users_collection": USERS_COLLECTION,
        "todos_collection": TODOS_COLLECTION,
    }
