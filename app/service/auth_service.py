from datetime import timedelta

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
        verify_password(payload.password, user.hashed_password)
        access_token = create_access_token(data={"sub": user.id},
                                           expires_delta=timedelta(settings.TOKEN_EXPIRES))
        return TokenResponse(access_token=access_token, token_type="bearer")
