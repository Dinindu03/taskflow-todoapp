from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.config import Settings, get_settings
from app.models.documents import UserResponse
from app.repositories.users import DuplicateEmailError, UserRepository
from app.schemas.auth import AuthResponse, SigninRequest, SignupRequest
from app.security import (
    create_access_token,
    get_current_user,
    new_csrf_token,
    require_authenticated_state_change,
    require_state_change_protection,
)
from app.services.auth import InvalidCredentialsError, signin, signup

router = APIRouter(prefix="/api/auth", tags=["authentication"])


def repository_for(request: Request) -> UserRepository:
    return UserRepository(request.app.state.database)


def set_auth_cookies(
    response: Response,
    access_token: str,
    csrf_token: str,
    settings: Settings,
) -> None:
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.jwt_expire_minutes * 60,
        path="/",
    )
    response.set_cookie(
        key=settings.csrf_cookie_name,
        value=csrf_token,
        httponly=False,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.jwt_expire_minutes * 60,
        path="/",
    )


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_state_change_protection)],
)
def signup_user(
    request: Request,
    payload: SignupRequest,
    settings: Settings = Depends(get_settings),
) -> AuthResponse:
    try:
        user = signup(repository_for(request), payload)
    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email already exists.",
        ) from exc

    return AuthResponse(user=user)


@router.post(
    "/signin",
    response_model=AuthResponse,
    dependencies=[Depends(require_state_change_protection)],
)
def signin_user(
    request: Request,
    payload: SigninRequest,
    response: Response,
    settings: Settings = Depends(get_settings),
) -> AuthResponse:
    try:
        user = signin(repository_for(request), payload)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    set_auth_cookies(
        response,
        create_access_token(user.id, settings),
        new_csrf_token(),
        settings,
    )
    return AuthResponse(
        user=UserResponse.model_validate(user.model_dump(exclude={"password_hash"}))
    )


@router.get("/me", response_model=UserResponse)
def current_user(user=Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user.model_dump(exclude={"password_hash"}))


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_authenticated_state_change)],
)
def logout(
    response: Response,
    settings: Settings = Depends(get_settings),
    _user=Depends(get_current_user),
) -> None:
    response.delete_cookie(settings.auth_cookie_name, path="/")
    response.delete_cookie(settings.csrf_cookie_name, path="/")
