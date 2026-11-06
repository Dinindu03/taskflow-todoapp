from fastapi import APIRouter, Depends, Request

from app.models.documents import UserDocument
from app.repositories.todos import TodoRepository
from app.schemas.dashboard import DashboardStatsResponse
from app.security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
def dashboard_stats(
    request: Request,
    user: UserDocument = Depends(get_current_user),
) -> DashboardStatsResponse:
    stats = TodoRepository(request.app.state.database).statistics_for_user(user.id)
    return DashboardStatsResponse(**stats)
