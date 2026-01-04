import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, status
from jose import JWTError

from app.core.security import get_current_user
from app.models.model import User


def test_get_current_user_success():
    mock_db = Mock()
    fake_user = User(
        id=1,
        email="test@gmail.com",
        username="test",
        hashed_password="hashed",
    )

    mock_db.query.return_value.filter.return_value.first.return_value = fake_user

    with patch("app.core.security.jwt.decode") as mock_decode:
        mock_decode.return_value = {"sub": 1}

        user = get_current_user(token="valid-token", db=mock_db)

    assert user == fake_user
    mock_decode.assert_called_once()
    mock_db.query.assert_called_once_with(User)


@patch("app.core.security.jwt.decode")
def test_get_current_user_missing_sub(mock_decode):
    mock_db = Mock()

    mock_decode.return_value = {}

    with pytest.raises(HTTPException) as exc:
        get_current_user(token="valid-token", db=mock_db)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "invalid user"


@patch("app.core.security.jwt.decode")
def test_get_current_user_invalid_token(mock_decode):
    mock_db = Mock()
    mock_decode.side_effect = JWTError()

    with pytest.raises(HTTPException) as exc:
        get_current_user(token="bad-token", db=mock_db)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Unable to validate credentials"


@patch("app.core.security.jwt.decode")
def test_get_current_user_user_not_found(mock_decode):
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_decode.return_value = {"sub": 999}

    with pytest.raises(HTTPException) as exc:
        get_current_user(token="valid-token", db=mock_db)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "User not found"
