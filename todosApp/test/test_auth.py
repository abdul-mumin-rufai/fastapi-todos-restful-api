from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, ALGORITHM, SECRET_KEY
from datetime import timedelta
from jose import jwt


app.dependency_overrides[get_db] = override_get_db


def test_authenticated_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'testing', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    invalid_username = authenticate_user('wrongusername', 'testing', db)
    assert invalid_username is False

    invalid_password = authenticate_user(test_user.username, 'wrongpassword', db)
    assert invalid_password is False


def test_create_access_token():
    username = 'rufaisontest'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decode_token['sub'] == username
    assert decode_token['id'] == user_id
    assert decode_token['role'] == role




