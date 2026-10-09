from .utils import *
from ..routers.auth import get_db, authenticate_user


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


