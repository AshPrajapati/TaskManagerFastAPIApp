import datetime
from unittest.mock import Mock

from app.models.model import User
from app.repository.auth_repository import AuthRepository


def test_create_user():
    mock_db = Mock()

    repository = AuthRepository(db=mock_db)
    user = repository.create_user(
        User(email="email", username="username", hashed_password="password", created_at=datetime.datetime.now(),
             updated_at=datetime.datetime.now()))

    assert user is not None
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
