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
