from fastapi import HTTPException

from app.repository.task_repository import TaskRepository
from app.schema.schema import TaskResponse, CreateTaskRequest, UpdateTaskRequest


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, create_task_request: CreateTaskRequest, user_id) -> TaskResponse:
        task = self.repository.create_task(create_task_request, user_id)
        return TaskResponse.model_validate(task)

    def get_all_tasks(self, user_id):
        tasks = self.repository.get_all_tasks(user_id)
        return [TaskResponse.model_validate(task) for task in tasks]

    def get_task_by_id(self, task_id, user_id):
        task = self.repository.get_task_by_id(task_id, user_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def update_task(self, task_id: int, payload: UpdateTaskRequest, user_id: int):
        task = self.repository.get_task_by_id(task_id, user_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        update_task = payload.model_dump(exclude_unset=True)
        for key, value in update_task.items():
            setattr(task, key, value)
        saved_task = self.repository.save_task(task)
        return TaskResponse.model_validate(saved_task)

    def delete_task(self, task_id, user_id):
        task = self.repository.get_task_by_id(task_id, user_id)
        self.repository.delete_task(task)
