from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.database import USERS_COLLECTION
from app.models.documents import UserDocument


class DuplicateEmailError(Exception):
    """Raised when a user email already exists."""


class UserRepository:
    def __init__(self, database: Database) -> None:
        self.collection = database[USERS_COLLECTION]

    def create(self, user: UserDocument) -> str:
        try:
            self.collection.insert_one(
                {
                    "_id": user.id,
                    "name": user.name,
                    "email": str(user.email),
                    "password_hash": user.password_hash,
                    "created_at": user.created_at,
                }
            )
        except DuplicateKeyError as exc:
            raise DuplicateEmailError from exc
        return user.id

    def find_by_email(self, email: str) -> UserDocument | None:
        document = self.collection.find_one({"email": email})
        return self._to_document(document)

    def find_by_id(self, user_id: str) -> UserDocument | None:
        document = self.collection.find_one({"_id": user_id})
        return self._to_document(document)

    @staticmethod
    def _to_document(document: dict | None) -> UserDocument | None:
        if document is None:
            return None
        return UserDocument(
            id=document["_id"],
            name=document["name"],
            email=document["email"],
            password_hash=document["password_hash"],
            created_at=document["created_at"],
        )
