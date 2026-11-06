from pydantic import BaseModel, ConfigDict, Field


class DashboardStatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int = Field(ge=0)
    completed: int = Field(ge=0)
    pending: int = Field(ge=0)
