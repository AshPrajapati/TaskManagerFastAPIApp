from sqlalchemy.orm import Session

from app.models.model import Task
from app.schema.schema import CreateTaskRequest


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, create_task: CreateTaskRequest, user_id):
        task = Task(title=create_task.title, description=create_task.description, priority=create_task.priority,
                    status=create_task.status, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
