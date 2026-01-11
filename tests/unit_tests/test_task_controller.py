from unittest.mock import Mock, ANY

from starlette.testclient import TestClient

from app.controller.task_controller import get_task_service
from app.core.security import get_current_user
from app.main import app
from app.schema.schema import TaskResponse, CreateTaskRequest, PaginatedTasksResponse


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

    mock_service.create_task.assert_called_once_with(create_task_request, 1, ANY)
    app.dependency_overrides.clear()


def test_get_all_tasks():
    mock_service = Mock()
    mock_service.get_all_tasks.return_value = PaginatedTasksResponse(
        tasks=[
            TaskResponse(task_id=1, title="title", description="description", status="pending", priority="high"),
            TaskResponse(task_id=2, title="title2", description="description2", status="pending", priority="high"),
            TaskResponse(task_id=3, title="title3", description="description3", status="pending", priority="high"),
        ],
        total=3,
        page=1,
        size=5,
        total_pages=1
    )

    setup_dependency_overrides(mock_service)
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer access_token"})

    response = client.get("/tasks?page=1&size=5&status=pending&priority=high")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert body["page"] == 1
    assert body["size"] == 5
    assert body["total_pages"] == 1
    assert len(body["tasks"]) == 3
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
    app.dependency_overrides.clear()


def test_delete_task():
    mock_service = Mock()

    setup_dependency_overrides(mock_service)
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer access_token"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    app.dependency_overrides.clear()


def setup_dependency_overrides(mock_service: Mock):
    def get_override_task_service():
        return mock_service

    def get_override_current_user():
        return Mock(id=1)

    app.dependency_overrides[get_task_service] = get_override_task_service
    app.dependency_overrides[get_current_user] = get_override_current_user
