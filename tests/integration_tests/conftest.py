import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.core.database import get_engine, Base, get_db
from app.main import app
from app.models.model import User, Task
from app.schema.schema import TaskStatus, TaskPriority
from tests.utils.auth import get_test_token


# ---------- ENGINE ----------

@pytest.fixture(scope="session")
def test_engine():
    engine = get_engine(test=True)
    yield engine
    engine.dispose()


# ---------- CREATE TABLES ONCE ----------

@pytest.fixture(scope="session", autouse=True)
def create_test_tables(test_engine):
    from app.models.model import User
    from app.models.model import Task
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# ---------- DB SESSION (TRANSACTION PER TEST) ----------

@pytest.fixture(scope="function")
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
    )
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ---------- CLIENT ----------

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def get_test_user(db_session):
    user = User(email="testuser@gmail.com",
                username="testuser",
                hashed_password="hashed-password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def authenticated_client(client: TestClient, get_test_user):
    test_token = get_test_token(get_test_user.id)
    client.headers.update(
        {"Authorization": f"Bearer {test_token}"}
    )
    return client


@pytest.fixture
def seeded_tasks(authenticated_client):
    task_one_response = authenticated_client.post("/tasks",
                                                  json={"title": "task1",
                                                        "description": "desc1",
                                                        "status": "pending",
                                                        "priority": "low", }
                                                  )

    task_two_response = authenticated_client.post("/tasks",
                                                  json={"title": "task2",
                                                        "description": "desc2",
                                                        "status": "pending",
                                                        "priority": "high", }
                                                  )
    return [task_one_response.json()["task_id"], task_two_response.json()["task_id"]]


@pytest.fixture
def seeded_tasks_get_all_tasks(db_session, get_test_user):
    user = get_test_user
    tasks = [
        Task(
            title="Buy milk",
            description="desc1",
            status=TaskStatus.pending.value,
            priority=TaskPriority.low.value,
            user_id=user.id
        ),
        Task(
            title="Fix bugs",
            description="desc2",
            status=TaskStatus.in_progress.value,
            priority=TaskPriority.high.value,
            user_id=user.id
        ),
        Task(
            title="Prepare meeting",
            description="desc3",
            status=TaskStatus.completed.value,
            priority=TaskPriority.medium.value,
            user_id=user.id
        ),
        Task(
            title="Buy groceries",
            description="desc4",
            status=TaskStatus.pending.value,
            priority=TaskPriority.low.value,
            user_id=user.id
        )
    ]
    db_session.add_all(tasks)
    db_session.commit()
