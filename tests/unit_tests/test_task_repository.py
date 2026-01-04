import datetime
from unittest.mock import Mock

from app.models.model import Task
from app.repository.task_reposirtoy import TaskRepository
from app.schema.schema import CreateTaskRequest


def test_create_task():
    mock_db = Mock()

    repository = TaskRepository(mock_db)
    repository.create_task(
        CreateTaskRequest(title="title", description="description", status="pending", priority="low"),
        user_id=1
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_get_all_tasks():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.all.return_value = [
        Task(
            id=1,
            title="title1",
            description="description",
            status="pending",
            priority="low",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            user_id=1
        ),
        Task(
            id=2,
            title="title2",
            description="description",
            status="pending",
            priority="low",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            user_id=1
        )
    ]

    repository = TaskRepository(mock_db)
    tasks = repository.get_all_tasks(user_id=1)

    assert tasks is not None
    assert len(tasks) == 2
    mock_db.query.return_value.filter.return_value.all.assert_called_once()

def test_get_task_by_id():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = Task(
        id=1,
        title="title1",
        description="description",
        status="pending",
        priority="low",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        user_id=1
    )

    repository = TaskRepository(mock_db)
    task = repository.get_task_by_id(task_id=1, user_id=1)

    assert task is not None
    assert task.id == 1
    mock_db.query.return_value.filter.return_value.first.assert_called_once()
