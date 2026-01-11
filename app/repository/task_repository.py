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

    def get_all_tasks(self,
                      user_id: int,
                      page: int,
                      size: int,
                      status: str | None,
                      priority: str | None,
                      search: str | None,
                      sort_by: str,
                      order: str, ):
        query = self.db.query(Task).filter(Task.user_id == user_id)

        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if search:
            query = query.filter(Task.title.ilike(f"%{search}%"))

        total = query.count()

        sort_column = getattr(Task, sort_by)
        query = query.order_by(sort_column.asc() if order == "asc" else sort_column.desc())

        tasks = (
            query.offset((page - 1) * size)
            .limit(size)
            .all()
        )
        total_pages = (total + size - 1) // size

        return {
            "tasks": tasks,
            "total_pages": total_pages,
            "page": page,
            "size": size,
            "total": total,
        }

    def get_task_by_id(self, task_id, user_id):
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    def save_task(self, task):
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task):
        self.db.delete(task)
        self.db.commit()
