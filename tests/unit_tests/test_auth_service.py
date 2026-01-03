from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from app.core.config import settings
from app.models.model import User
from app.schema.schema import SignupRequest, TokenResponse
from app.service.auth_service import AuthService


@patch('app.service.auth_service.hash_password')
@patch('app.service.auth_service.create_access_token')
def test_signup(mock_create_access_token, mock_hash_password):
    mock_repository = Mock()
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
    mock_create_access_token.assert_called_once_with(data={"sub": 1},
                                                     expires_delta=timedelta(settings.TOKEN_EXPIRES))
