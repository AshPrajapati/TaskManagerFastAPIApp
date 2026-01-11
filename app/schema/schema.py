from enum import Enum

from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    username: str
    password: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: str
    password: str


class CreateTaskRequest(BaseModel):
    title: str
    description: str
    status: str
    priority: str


class TaskResponse(BaseModel):
    task_id: int = Field(validation_alias="id")
    title: str
    description: str
    status: str
    priority: str

    class Config:
        from_attributes = True
        populate_by_name = True


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None


class PaginatedTasksResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    page: int
    size: int
    total_pages: int


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskSortBy(str, Enum):
    created_at = "created_at"
    priority = "priority"
    title = "title"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
