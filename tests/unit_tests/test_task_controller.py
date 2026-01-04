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

    setup_dependency_overrides(mock_service)
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


def test_get_all_tasks():
    mock_service = Mock()
    mock_service.get_all_tasks.return_value = [
        TaskResponse(
            task_id=1,
            title="title",
            description="description",
            status="pending",
            priority="low"
        )
        ,
        TaskResponse(
            task_id=2,
            title="title2",
            description="description2",
            status="pending",
            priority="medium"
        )
    ]

    setup_dependency_overrides(mock_service)
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer access_token"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_service.get_all_tasks.assert_called_once()
    app.dependency_overrides.clear()


def test_get_by_id():
    mock_service = Mock()
    mock_service.get_task_by_id.return_value = TaskResponse(
        task_id=1,
        title="title",
        description="description",
        status="pending",
        priority="low"
    )

    setup_dependency_overrides(mock_service)
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer access_token"})

    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {
        'description': 'description',
        'priority': 'low',
        'status': 'pending',
        'task_id': 1,
        'title': 'title',
    }
    mock_service.get_task_by_id.assert_called_once_with(1, 1)
    app.dependency_overrides.clear()


def test_update_task():
    mock_service = Mock()
    mock_service.update_task.return_value = TaskResponse(
        task_id=1,
        title="updated_title",
        description="description",
        status="pending",
        priority="high"
    )

    setup_dependency_overrides(mock_service)
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer access_token"})
    response = client.put("/tasks/1", json={"title": "updated_title", "priority": "high"})
    assert response.status_code == 200


def setup_dependency_overrides(mock_service: Mock):
    def get_override_task_service():
        return mock_service

    def get_override_current_user():
        return Mock(id=1)

    app.dependency_overrides[get_task_service] = get_override_task_service
    app.dependency_overrides[get_current_user] = get_override_current_user
