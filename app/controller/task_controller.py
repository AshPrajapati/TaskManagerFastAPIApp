from typing import Optional

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.background_tasks.emailService import EmailService
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.model import User
from app.repository.task_repository import TaskRepository
from app.schema.schema import TaskResponse, CreateTaskRequest, UpdateTaskRequest, TaskStatus, TaskPriority, TaskSortBy, \
    SortOrder, PaginatedTasksResponse
from app.service.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db=db)


def get_email_service():
    return EmailService()


def get_task_service(repository: TaskRepository = Depends(get_task_repository),
                     email_service: EmailService = Depends(get_email_service)) -> TaskService:
    return TaskService(repository=repository, email_service=email_service)


@task_router.post("/", response_model=TaskResponse)
def create_task(create_task_request: CreateTaskRequest,
                background_tasks: BackgroundTasks,
                service: TaskService = Depends(get_task_service),
                user: User = Depends(get_current_user)):
    task = service.create_task(create_task_request, user.id, background_tasks)
    return task


@task_router.get("/", response_model=PaginatedTasksResponse)
def get_all_tasks(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        status: Optional[TaskStatus] = Query(None),
        priority: Optional[TaskPriority] = Query(None),
        search: Optional[str] = Query(None),
        sort_by: TaskSortBy = Query(TaskSortBy.created_at),
        order: SortOrder = Query(SortOrder.desc),
        service: TaskService = Depends(get_task_service),
        user: User = Depends(get_current_user)):
    paginated_task_response = service.get_all_tasks(user_id=user.id,
                                                    page=page,
                                                    size=size,
                                                    status=status,
                                                    priority=priority,
                                                    search=search,
                                                    sort_by=sort_by,
                                                    order=order, )
    return paginated_task_response


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, service: TaskService = Depends(get_task_service),
                   user: User = Depends(get_current_user)):
    task = service.get_task_by_id(task_id, user.id)
    return task


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: UpdateTaskRequest,
                background_tasks: BackgroundTasks,
                service: TaskService = Depends(get_task_service),
                user: User = Depends(get_current_user)):
    task = service.update_task(task_id, payload, user.id, background_tasks)
    return task


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int,
                service: TaskService = Depends(get_task_service),
                user: User = Depends(get_current_user)):
    service.delete_task(task_id, user.id)
