from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from starlette import status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


# this function opens and close database(dependencies injection)
def get_db():
    db = SessionLocal()
    try:
        yield db  # this is run before our request happens
    finally:
        db.close()  # this closes db after our response is returned


db_dependency_injection = Annotated[Session, Depends(get_db)]
user_token_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todos', status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_token_dependency, db: db_dependency_injection):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Not Authorised for this page')
    return db.query(Todos).all()


@router.delete('/delete_todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_token_dependency, db: db_dependency_injection, todo_id: int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Not Authorised for this page')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo Not Found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
