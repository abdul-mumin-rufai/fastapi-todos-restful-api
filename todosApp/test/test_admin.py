from .utils import *
from ..routers.admin import get_current_user, get_db
from fastapi import status
from ..models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user


def test_get_admin_all_todos(test_todo):
    response = client.get('/admin/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': 'FastAPI testing',
                                'description': 'Testing my FastAPI application',
                                'priority': 5,
                                'complete': False,
                                'owner_id': 1,
                                'id': 1
                                }]


def test_delete_admin_todo(test_todo):
    response = client.delete('/admin/delete_todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_admin_todo_not_found(test_todo):
    response = client.delete('/admin/delete_todo/99')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo Not Found'}
