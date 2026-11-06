from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TodoCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Title must not be blank.")
        return normalized


class TodoUpdateRequest(TodoCreateRequest):
    pass


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
