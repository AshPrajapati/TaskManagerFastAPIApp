from typing import Generator, Any
import pytest
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.core.database import get_engine, Base, get_db
from app.main import app


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
