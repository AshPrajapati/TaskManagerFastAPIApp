from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.controller.auth_controller import get_auth_service
from app.main import app

USERNAME = "testuser"
PASSWORD = "secret123"
EMAIL = "test@mail.com"
TOKEN_TYPE = "bearer"
FAKE_ACCESS_TOKEN = "fake-access-token"


def test_sign_up():
    mock_service = Mock()
    mock_service.signup.return_value = {
        "access_token": "fake-access-token",
        "token_type": "bearer",
    }

    def override_get_auth_service():
        return mock_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service

    client = TestClient(app)
    response = client.post("/auth/sign-up",
                           json={
                               "username": USERNAME,
                               "email": EMAIL,
                               "password": PASSWORD
                           })

    assert response.status_code == 200
    mock_service.signup.assert_called_once()
    app.dependency_overrides.clear()


def test_login():
    mock_service = Mock()
    mock_service.login.return_value = {
        "access_token": FAKE_ACCESS_TOKEN,
        "token_type": TOKEN_TYPE,
    }

    def override_get_auth_service():
        return mock_service

    app.dependency_overrides[get_auth_service] = override_get_auth_service
    test_client = TestClient(app)
    response = test_client.post(
        "/auth/login",
        json={
            "email": EMAIL,
            "password": PASSWORD
        }
    )
    assert response.status_code == 200
    mock_service.login.assert_called_once()
    app.dependency_overrides.clear()
