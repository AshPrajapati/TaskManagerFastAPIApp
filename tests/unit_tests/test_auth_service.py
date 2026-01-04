from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException

from app.core.config import settings
from app.models.model import User
from app.schema.schema import SignupRequest, TokenResponse, LoginRequest
from app.service.auth_service import AuthService


@patch('app.service.auth_service.hash_password')
@patch('app.service.auth_service.create_access_token')
def test_signup(mock_create_access_token, mock_hash_password):
    mock_repository = Mock()
    mock_repository.get_user_by_email.return_value = None
    mock_repository.create_user.return_value = User(
        id=1,
        username="username",
        email="email",
        hashed_password="hashed-password",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    mock_hash_password.return_value = "hashed-password"
    mock_create_access_token.return_value = "encoded-token"

    service = AuthService(mock_repository)
    token_response: TokenResponse = service.signup(
        SignupRequest(username="username", email="email", password="password")
    )

    assert token_response is not None
    assert token_response.token_type == "bearer"
    mock_repository.create_user.assert_called_once()
    mock_hash_password.assert_called_once_with("password")
    mock_create_access_token.assert_called_once_with(data={"sub": "1"},
                                                     expires_delta=timedelta(settings.TOKEN_EXPIRES))


def test_signup_when_user_already_with_email():
    mock_repository = Mock()
    mock_repository.get_user_by_email.return_value = User(
        id=1,
        username="user1",
        email="email@gmail.com",
        hashed_password="hashed-password",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    service = AuthService(mock_repository)

    with pytest.raises(HTTPException) as e:
        service.signup(payload=SignupRequest(username="user2", email="email@gmail.com", password="new-password"))

    assert e.value.status_code == 400
    assert e.value.detail == "User already exists with same email"
    mock_repository.get_user_by_email.assert_called_once()
    assert mock_repository.create_user.call_count == 0


@patch('app.service.auth_service.create_access_token')
@patch('app.service.auth_service.verify_password')
def test_login(mock_verify_password, mock_create_access_token):
    mock_repository = Mock()
    mock_repository.get_user_by_email.return_value = User(
        id=1,
        username="username",
        email="email",
        hashed_password="hashed-password",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "encoded-token"

    service = AuthService(mock_repository)
    token_response = service.login(OAuth2PasswordRequestForm(username="email@email.com", password="password"))
    assert token_response is not None
    assert token_response.token_type == "bearer"
    mock_repository.get_user_by_email.assert_called_once()
    mock_verify_password.assert_called_once_with("password", "hashed-password")
    mock_create_access_token.assert_called_once_with(data={"sub": "1"},
                                                     expires_delta=timedelta(settings.TOKEN_EXPIRES))


def test_login_when_user_not_found():
    with pytest.raises(HTTPException) as e:
        mock_repository = Mock()
        mock_repository.get_user_by_email.return_value = None

        service = AuthService(mock_repository)
        service.login(form_data=OAuth2PasswordRequestForm(username="dummy@email.com", password="password"))

        mock_repository.get_user_by_email.assert_called_once()


@patch('app.service.auth_service.verify_password')
def test_login_when_password_mismatch(mock_verify_password):
    with pytest.raises(HTTPException) as e:
        mock_repository = Mock()
        mock_repository.get_user_by_email.return_value = User(
            id=1,
            username="username",
            email="user@gmail.com",
            hashed_password="hashed-password",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        mock_verify_password.return_value = False

        service = AuthService(mock_repository)
        service.login(form_data=OAuth2PasswordRequestForm(username="user@gmail.com", password="dummy-password"))
