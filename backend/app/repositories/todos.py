from pymongo.database import Database

from app.database import TODOS_COLLECTION
from app.models.documents import TodoDocument


class TodoRepository:
    def __init__(self, database: Database) -> None:
        self.collection = database[TODOS_COLLECTION]

    def create(self, todo: TodoDocument) -> str:
        self.collection.insert_one(self._to_document(todo))
        return todo.id

    def list_for_user(self, user_id: str) -> list[TodoDocument]:
        return [
            self._from_document(document)
            for document in self.collection.find({"user_id": user_id}).sort(
                "created_at", -1
            )
        ]

    def get_for_user(self, todo_id: str, user_id: str) -> TodoDocument | None:
        document = self.collection.find_one({"_id": todo_id, "user_id": user_id})
        return self._from_document(document) if document else None

    def update_for_user(
        self,
        todo_id: str,
        user_id: str,
        *,
        title: str,
        description: str,
        updated_at,
    ) -> TodoDocument | None:
        result = self.collection.find_one_and_update(
            {"_id": todo_id, "user_id": user_id},
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "updated_at": updated_at,
                }
            },
            return_document=True,
        )
        return self._from_document(result) if result else None

    def set_completed(
        self, todo_id: str, user_id: str, completed: bool, updated_at
    ) -> TodoDocument | None:
        result = self.collection.find_one_and_update(
            {"_id": todo_id, "user_id": user_id},
            {"$set": {"completed": completed, "updated_at": updated_at}},
            return_document=True,
        )
        return self._from_document(result) if result else None

    def delete_for_user(self, todo_id: str, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": todo_id, "user_id": user_id})
        return result.deleted_count == 1

    def statistics_for_user(self, user_id: str) -> dict[str, int]:
        result = next(
            self.collection.aggregate(
                [
                    {"$match": {"user_id": user_id}},
                    {
                        "$group": {
                            "_id": None,
                            "total": {"$sum": 1},
                            "completed": {
                                "$sum": {"$cond": ["$completed", 1, 0]}
                            },
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "total": 1,
                            "completed": 1,
                            "pending": {
                                "$subtract": ["$total", "$completed"]
                            },
                        }
                    },
                ]
            ),
            None,
        )
        if result is None:
            return {"total": 0, "completed": 0, "pending": 0}
        return {
            "total": int(result["total"]),
            "completed": int(result["completed"]),
            "pending": int(result["pending"]),
        }

    @staticmethod
    def _to_document(todo: TodoDocument) -> dict:
        return {
            "_id": todo.id,
            "user_id": todo.user_id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at,
        }

    @staticmethod
    def _from_document(document: dict) -> TodoDocument:
        return TodoDocument(
            id=document["_id"],
            user_id=document["user_id"],
            title=document["title"],
            description=document.get("description", ""),
            completed=document["completed"],
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )
