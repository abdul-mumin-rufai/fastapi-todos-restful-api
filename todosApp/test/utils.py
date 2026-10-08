from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from ..models import Todos, Users
from ..database import Base
from ..main import app
import pytest
from ..routers.users import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testDatabase.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_current_user():
    return {'username': 'rufaison', 'id': 1, 'role': 'admin'}


@pytest.fixture()
def test_todo():
    todo = Todos(
        title='FastAPI testing',
        description='Testing my FastAPI application',
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture()
def test_user():
    user = Users(
        username='rufaisontest',
        first_name='abdul-mumintest',
        last_name='rufaitest',
        email='test@hotmail.com',
        hashed_password=bcrypt_context.hash('testing'),
        role='admin',
        phone_number='0240481753'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
