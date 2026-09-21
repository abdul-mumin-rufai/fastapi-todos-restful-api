from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


#  this includes the auth file as a router to connect the auth to the main port
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


# this function opens and close database(dependencies injection)
def get_db():
    db = SessionLocal()
    try:
        yield db  # this is run before our request happens
    finally:
        db.close()  # this closes db after our response is returned


db_dependency_injection = Annotated[Session, Depends(get_db)]  # this runs ie interact with the database before our


# request

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post('/auth', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency_injection, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()


@router.post('/token')
async def create_user_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                            db: db_dependency_injection):  # using OAuth as dependency injection
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'
    return 'Successful Authentication'
