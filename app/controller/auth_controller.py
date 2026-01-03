from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repository.auth_repository import AuthRepository
from app.schema.schema import SignupRequest, TokenResponse, LoginRequest
from app.service.auth_service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_repository(db: Session = Depends(get_db)):
    return AuthRepository(db)


def get_auth_service(
        repo: AuthRepository = Depends(get_auth_repository),
):
    return AuthService(repo)


@auth_router.post("/sign-up", response_model=TokenResponse)
def sign_up(payload: SignupRequest, service: AuthService = Depends(get_auth_service)):
    response = service.signup(payload)
    return response

@auth_router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    response = service.login(payload)
    return response
