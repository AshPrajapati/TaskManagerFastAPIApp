import datetime
from unittest.mock import Mock

import pytest
from fastapi import HTTPException, BackgroundTasks

from app.models.model import Task
from app.schema.schema import CreateTaskRequest, UpdateTaskRequest
from app.service.task_service import TaskService


def test_create_task():
    mock_repo = Mock()
    email_service = Mock()
    background_tasks = BackgroundTasks()
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

    service = TaskService(repository=mock_repo, email_service=email_service)

    payload = CreateTaskRequest(
        title="Test",
        description="Desc",
        status="pending",
        priority="low",
    )

    result = service.create_task(payload, user_id=1, background_tasks=background_tasks)

    assert result.task_id == 1
    assert len(background_tasks.tasks) == 1
    mock_repo.create_task.assert_called_once()


def test_get_all_tasks():
    mock_repo = Mock()
    email_service = Mock()
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

    service = TaskService(repository=mock_repo, email_service=email_service)
    tasks = service.get_all_tasks(user_id=1)

    assert len(tasks) == 1
    mock_repo.get_all_tasks.assert_called_once()


def test_get_task_by_id():
    mock_repo = Mock()
    email_service = Mock()
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

    service = TaskService(repository=mock_repo, email_service=email_service)
    task = service.get_task_by_id(1, 1)

    assert task.id == 1
    mock_repo.get_task_by_id.assert_called_once()


def test_get_task_by_id_not_found():
    mock_repo = Mock()
    email_service = Mock()
    mock_repo.get_task_by_id.return_value = None

    service = TaskService(repository=mock_repo, email_service=email_service)
    with pytest.raises(HTTPException) as e:
        service.get_task_by_id(1, 1)

    assert e.value.status_code == 404
    assert e.value.detail == "Task not found"
    mock_repo.get_task_by_id.assert_called_once()


def test_update_task():
    mock_repo = Mock()
    email_service = Mock()
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
    mock_repo.save_task.return_value = Task(
        id=1,
        title="Updated title",
        description="Desc",
        status="pending",
        priority="high",
        user_id=1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    service = TaskService(repository=mock_repo, email_service=email_service)
    task = service.update_task(1, UpdateTaskRequest(title="Updated title", priority="high"), 1)

    assert task.title == "Updated title"
    assert task.priority == "high"
    mock_repo.get_task_by_id.assert_called_once_with(1, 1)
    mock_repo.save_task.assert_called_once()


def test_update_task_not_found():
    mock_repo = Mock()
    email_service = Mock()
    mock_repo.get_task_by_id.return_value = None

    service = TaskService(repository=mock_repo, email_service=email_service)
    with pytest.raises(HTTPException) as e:
        service.update_task(1, UpdateTaskRequest(title="Updated title", priority="high"), 1)

    assert e.value.status_code == 404
    assert e.value.detail == "Task not found"


def test_delete_task():
    mock_repo = Mock()
    email_service = Mock()
    task = Task(id=1, title="Test", description="Desc", status="pending", priority="low", user_id=1,
                created_at=datetime.datetime.now(), updated_at=datetime.datetime.now(), )
    mock_repo.get_task_by_id.return_value = task

    service = TaskService(repository=mock_repo, email_service=email_service)
    service.delete_task(1, 1)
    mock_repo.get_task_by_id.assert_called_once_with(1, 1)
    mock_repo.delete_task.assert_called_once_with(task)


def test_delete_task_not_found():
    mock_repo = Mock()
    email_service = Mock()
    mock_repo.get_task_by_id.return_value = None

    service = TaskService(repository=mock_repo, email_service=email_service)
    with pytest.raises(HTTPException) as e:
        service.delete_task(1, 1)

    assert e.value.status_code == 404
    assert e.value.detail == "Task not found to delete"
    mock_repo.get_task_by_id.assert_called_once_with(1, 1)
