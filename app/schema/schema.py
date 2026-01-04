from pydantic import BaseModel


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
    task_id: int
    title: str
    description: str
    status: str
    priority: str
