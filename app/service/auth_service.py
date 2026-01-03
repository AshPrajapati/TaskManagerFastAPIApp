from datetime import timedelta

from fastapi import HTTPException
from starlette import status

from app.core.config import settings
from app.core.security import hash_password, create_access_token, verify_password
from app.models.model import User
from app.repository.auth_repository import AuthRepository
from app.schema.schema import SignupRequest, TokenResponse, LoginRequest


def get_auth_repository() -> AuthRepository:
    return AuthRepository()


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def signup(self, payload: SignupRequest):
        user_by_email = self.repository.get_user_by_email(payload.email)
        if user_by_email:
            raise HTTPException(status_code=400, detail="User already exists with same email")

        user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=hash_password(payload.password)
        )
        saved_user = self.repository.create_user(user)
        access_token = create_access_token(data={"sub": saved_user.id},
                                           expires_delta=timedelta(settings.TOKEN_EXPIRES))
        return TokenResponse(access_token=access_token, token_type="bearer")

    def login(self, payload: LoginRequest):
        user: User = self.repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="password mismatch")

        access_token = create_access_token(data={"sub": user.id},
                                           expires_delta=timedelta(settings.TOKEN_EXPIRES))
        return TokenResponse(access_token=access_token, token_type="bearer")
