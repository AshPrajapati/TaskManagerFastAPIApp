import datetime
from unittest.mock import Mock

from app.models.model import Task
from app.schema.schema import CreateTaskRequest
from app.service.task_service import TaskService


def test_create_task():
    mock_repo = Mock()
    mock_repo.create_task.return_value = Task(
        id=1,
        title="Test",
        description="Desc",
        status="pending",
        priority="low",
        user_id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    service = TaskService(repository=mock_repo)

    payload = CreateTaskRequest(
        title="Test",
        description="Desc",
        status="pending",
        priority="low",
    )

    result = service.create_task(payload, user_id=1)

    assert result.task_id == 1
    mock_repo.create_task.assert_called_once()


def test_get_all_tasks():
    mock_repo = Mock()
    mock_repo.get_all_tasks.return_value = [
        Task(
            id=1,
            title="Test",
            description="Desc",
            status="pending",
            priority="low",
            user_id=1,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
    ]

    service = TaskService(repository=mock_repo)
    tasks = service.get_all_tasks(user_id=1)

    assert len(tasks) == 1
    mock_repo.get_all_tasks.assert_called_once()


def test_get_task_by_id():
    mock_repo = Mock()
    mock_repo.get_task_by_id.return_value = Task(
        id=1,
        title="Test",
        description="Desc",
        status="pending",
        priority="low",
        user_id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    service = TaskService(repository=mock_repo)
    task = service.get_task_by_id(1, 1)

    assert task.id == 1
    mock_repo.get_task_by_id.assert_called_once()
