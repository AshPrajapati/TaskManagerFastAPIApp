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
