from .utils import *
from ..routers.users import get_current_user, get_db, bcrypt_context
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_current_user


def test_users(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'rufaisontest'
    assert response.json()['first_name'] == 'abdul-mumintest'
    assert response.json()['last_name'] == 'rufaitest'
    assert response.json()['email'] == 'test@hotmail.com'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '0240481753'


