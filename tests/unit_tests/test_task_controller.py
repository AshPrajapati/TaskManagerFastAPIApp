from unittest.mock import Mock

from starlette.testclient import TestClient

from app.controller.task_controller import get_task_service
from app.core.security import get_current_user
from app.main import app
from app.schema.schema import TaskResponse, CreateTaskRequest


def test_create_task():
    mock_service = Mock()
    mock_service.create_task.return_value = TaskResponse(task_id=1,
                                                         title="title",
                                                         description="description",
                                                         status="pending",
                                                         priority="low")

    def get_override_task_service():
        return mock_service

    def get_override_current_user():
        return Mock(id=1)

    app.dependency_overrides[get_task_service] = get_override_task_service
    app.dependency_overrides[get_current_user] = get_override_current_user

    client = TestClient(app)
    create_task_request = CreateTaskRequest(title="title",
                                            description="description",
                                            status="pending",
                                            priority="low")
    client.headers.update({"Authorization": f"Bearer access_token"})

    response = client.post("/tasks",
                           json=create_task_request.model_dump())

    assert response.status_code == 200
    mock_service.create_task.assert_called_once_with(create_task_request, 1)
    app.dependency_overrides.clear()
