from app.repository.task_reposirtoy import TaskRepository
from app.schema.schema import TaskResponse, CreateTaskRequest


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, create_task_request: CreateTaskRequest, user_id) -> TaskResponse:
        task = self.repository.create_task(create_task_request, user_id)
        return TaskResponse(
            task_id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority
        )
