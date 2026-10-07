from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///./testDatabase.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_current_user():
    return {'username': 'rufaison', 'id': 1, 'role': 'admin'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user

client = TestClient(app)


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


def test_read_all_authenticated_user_todos(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': 'FastAPI testing',
                                'description': 'Testing my FastAPI application',
                                'priority': 5,
                                'complete': False,
                                'owner_id': 1,
                                'id': 1
                                }]


def test_read_authenticated_user_todos_by_id(test_todo):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title': 'FastAPI testing',
                               'description': 'Testing my FastAPI application',
                               'priority': 5,
                               'complete': False,
                               'owner_id': 1,
                               'id': 1
                               }


def test_read_authenticated_user_todos_by_id_if_id_not_found(test_todo):
    response = client.get('/todo/33')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}


def test_create_testing_todo(test_todo):
    test_request = {'title': 'My testing',
                    'description': 'Testing is part of SDLC',
                    'priority': 5,
                    'complete': False
                    }
    response = client.post('/todo/', json=test_request)
    assert response.status_code == 201

    db = TestingSessionLocal()

    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == test_request.get('title')
    assert model.description == test_request.get('description')
    assert model.priority == test_request.get('priority')
    assert model.complete == test_request.get('complete')


def test_update_todo(test_todo):
    test_request = {
        'title': 'Updated my FastAPI title',
        'description': 'Testing is part of SDLC',
        'priority': 5,
        'complete': False,
    }
    response = client.put('/todo/1', json=test_request)
    assert response.status_code == 204
    db = TestingSessionLocal()  # getting the databases
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == test_request.get('title')


def test_update_todo_not_found(test_todo):
    test_request = {
        'title': 'Updated my FastAPI title',
        'description': 'Testing is part of SDLC',
        'priority': 5,
        'complete': False,
    }
    response = client.put('/todo/999', json=test_request)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found in todos list'}



