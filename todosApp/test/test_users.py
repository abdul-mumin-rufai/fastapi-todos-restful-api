from .utils import *
from ..routers.users import get_current_user, get_db
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


def test_change_password(test_user):
    response = client.put('/user/change_password', json={'password': 'testing', 'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put('/user/change_password', json={'password': 'wrongpassword', 'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error On Password Change'}


def test_change_phone_number(test_user):
    response = client.put('/user/phone-number/0245662326')
    assert response.status_code == status.HTTP_204_NO_CONTENT



