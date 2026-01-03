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


def test_get_user_by_email():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = User(id=1,
                                                                             email="example@gmail.com",
                                                                             username="username",
                                                                             hashed_password="password",
                                                                             created_at=datetime.datetime.now(),
                                                                             updated_at=datetime.datetime.now())
    repository = AuthRepository(db=mock_db)
    user = repository.get_user_by_email("example@gmail.com")

    assert user is not None
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.first.assert_called_once()
