from unittest.mock import Mock

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
