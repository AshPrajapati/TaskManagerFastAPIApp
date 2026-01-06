from fastapi import HTTPException, BackgroundTasks

from app.background_tasks.emailService import EmailService
from app.models.model import Task
from app.repository.task_repository import TaskRepository
from app.schema.schema import TaskResponse, CreateTaskRequest, UpdateTaskRequest


class TaskService:
    def __init__(self, repository: TaskRepository, email_service: EmailService):
        self.repository = repository
        self.email_service = email_service

    def create_task(self, create_task_request: CreateTaskRequest, user_id,
                    background_tasks: BackgroundTasks) -> TaskResponse:
        task = self.repository.create_task(create_task_request, user_id)
        background_tasks.add_task(self.email_service.send_email_on_task_created, task)
        return TaskResponse.model_validate(task)

    def get_all_tasks(self, user_id):
        tasks = self.repository.get_all_tasks(user_id)
        return [TaskResponse.model_validate(task) for task in tasks]

    def get_task_by_id(self, task_id, user_id):
        task = self.repository.get_task_by_id(task_id, user_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def update_task(self, task_id: int, payload: UpdateTaskRequest,
                    user_id: int,
                    background_tasks: BackgroundTasks):
        task = self.repository.get_task_by_id(task_id, user_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        update_task = payload.model_dump(exclude_unset=True)
        for key, value in update_task.items():
            setattr(task, key, value)
        saved_task: Task = self.repository.save_task(task)

        if saved_task.status == "completed":
            background_tasks.add_task(self.email_service.send_email_on_task_completed, saved_task)

        return TaskResponse.model_validate(saved_task)

    def delete_task(self, task_id, user_id):
        task = self.repository.get_task_by_id(task_id, user_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found to delete")
        self.repository.delete_task(task)
