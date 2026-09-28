from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from starlette import status
from models import Todos, Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# this function opens and close database(dependencies injection)
def get_db():
    db = SessionLocal()
    try:
        yield db  # this is run before our request happens
    finally:
        db.close()  # this closes db after our response is returned


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


db_dependency_injection = Annotated[Session, Depends(get_db)]
user_token_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_token_dependency, db: db_dependency_injection):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()  # type: ignore


@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_token_dependency, db: db_dependency_injection,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()  # type: ignore
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error On Password Change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
