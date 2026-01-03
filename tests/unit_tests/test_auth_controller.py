from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.controller.auth_controller import get_auth_service
from app.main import app


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
                               "username": "testuser",
                               "email": "test@mail.com",
                               "password": "secret123"
                           })

    assert response.status_code == 200
    mock_service.signup.assert_called_once()
    app.dependency_overrides.clear()
