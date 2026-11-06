from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.models.documents import UserDocument
from app.repositories.todos import TodoRepository
from app.schemas.todos import TodoCreateRequest, TodoResponse, TodoUpdateRequest
from app.security import get_current_user, require_authenticated_state_change

router = APIRouter(prefix="/api/todos", tags=["todos"])


def repository_for(request: Request) -> TodoRepository:
    return TodoRepository(request.app.state.database)


def not_found() -> HTTPException:
    return HTTPException(status_code=404, detail="Todo not found.")


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_authenticated_state_change)],
)
def create_todo(
    request: Request,
    payload: TodoCreateRequest,
    user: UserDocument = Depends(get_current_user),
) -> TodoResponse:
    now = datetime.now(UTC)
    todo = repository_for(request)
    from app.models.documents import TodoDocument

    created = TodoDocument(
        id=str(uuid4()),
        user_id=user.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        completed=False,
        created_at=now,
        updated_at=now,
    )
    todo.create(created)
    return TodoResponse.model_validate(created)


@router.get("", response_model=list[TodoResponse])
def list_todos(
    request: Request,
    user: UserDocument = Depends(get_current_user),
) -> list[TodoResponse]:
    return [
        TodoResponse.model_validate(todo)
        for todo in repository_for(request).list_for_user(user.id)
    ]


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: str,
    request: Request,
    user: UserDocument = Depends(get_current_user),
) -> TodoResponse:
    todo = repository_for(request).get_for_user(todo_id, user.id)
    if todo is None:
        raise not_found()
    return TodoResponse.model_validate(todo)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    dependencies=[Depends(require_authenticated_state_change)],
)
def update_todo(
    todo_id: str,
    request: Request,
    payload: TodoUpdateRequest,
    user: UserDocument = Depends(get_current_user),
) -> TodoResponse:
    todo = repository_for(request).update_for_user(
        todo_id,
        user.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        updated_at=datetime.now(UTC),
    )
    if todo is None:
        raise not_found()
    return TodoResponse.model_validate(todo)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_authenticated_state_change)],
)
def delete_todo(
    todo_id: str,
    request: Request,
    user: UserDocument = Depends(get_current_user),
) -> Response:
    if not repository_for(request).delete_for_user(todo_id, user.id):
        raise not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def set_status(
    todo_id: str,
    request: Request,
    user: UserDocument,
    completed: bool,
) -> TodoResponse:
    todo = repository_for(request).set_completed(
        todo_id, user.id, completed, datetime.now(UTC)
    )
    if todo is None:
        raise not_found()
    return TodoResponse.model_validate(todo)


@router.patch(
    "/{todo_id}/complete",
    response_model=TodoResponse,
    dependencies=[Depends(require_authenticated_state_change)],
)
def complete_todo(
    todo_id: str,
    request: Request,
    user: UserDocument = Depends(get_current_user),
) -> TodoResponse:
    return set_status(todo_id, request, user, True)


@router.patch(
    "/{todo_id}/pending",
    response_model=TodoResponse,
    dependencies=[Depends(require_authenticated_state_change)],
)
def pending_todo(
    todo_id: str,
    request: Request,
    user: UserDocument = Depends(get_current_user),
) -> TodoResponse:
    return set_status(todo_id, request, user, False)


@router.patch(
    "/{todo_id}/uncomplete",
    response_model=TodoResponse,
    dependencies=[Depends(require_authenticated_state_change)],
)
def uncomplete_todo(
    todo_id: str,
    request: Request,
    user: UserDocument = Depends(get_current_user),
) -> TodoResponse:
    return set_status(todo_id, request, user, False)
