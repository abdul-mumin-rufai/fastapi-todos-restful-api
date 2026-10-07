from .utils import *
from ..routers.admin import get_current_user, get_db
from fastapi import status


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
