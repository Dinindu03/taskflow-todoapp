from datetime import UTC, datetime
from uuid import uuid4

from app.models.documents import UserDocument, UserResponse
from app.repositories.users import DuplicateEmailError, UserRepository
from app.schemas.auth import SignupRequest, SigninRequest
from app.security import hash_password, verify_password


class InvalidCredentialsError(Exception):
    """Raised when an email/password pair cannot be authenticated."""


def signup(repository: UserRepository, request: SignupRequest) -> UserResponse:
    user = UserDocument(
        id=str(uuid4()),
        name=request.name.strip(),
        email=str(request.email).lower(),
        password_hash=hash_password(request.password),
        created_at=datetime.now(UTC),
    )
    repository.create(user)
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )


def signin(repository: UserRepository, request: SigninRequest) -> UserDocument:
    user = repository.find_by_email(str(request.email).lower())
    if user is None or not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsError
    return user


__all__ = [
    "DuplicateEmailError",
    "InvalidCredentialsError",
    "signin",
    "signup",
]
