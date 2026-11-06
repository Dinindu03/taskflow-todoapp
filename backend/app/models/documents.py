from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    email: EmailStr
    password_hash: str = Field(min_length=1)
    created_at: datetime


class UserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    email: EmailStr
    created_at: datetime


class TodoDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    user_id: str
    title: str
    description: str
    completed: bool = False
    created_at: datetime
    updated_at: datetime
