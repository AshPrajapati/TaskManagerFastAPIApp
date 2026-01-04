from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.model import User
from app.repository.task_reposirtoy import TaskRepository
from app.schema.schema import TaskResponse, CreateTaskRequest
from app.service.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db=db)


def get_task_service(repository: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(repository=repository)


@task_router.post("/", response_model=TaskResponse)
def create_task(create_task_request: CreateTaskRequest,
                service: TaskService = Depends(get_task_service),
                user: User = Depends(get_current_user)):
    task = service.create_task(create_task_request, user.id)
    return task
