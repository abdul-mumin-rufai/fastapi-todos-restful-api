from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from starlette import status

import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

# this creates a new database
models.Base.metadata.create_all(bind=engine)


# this function opens and close database(dependencies injection)
def get_db():
    db = SessionLocal()
    try:
        yield db  # this is run before our request happens
    finally:
        db.close()  # this closes db after our response is returned


db_dependency_injection = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    priority: int = Field(gt=0, lt=6)
    description: str = Field(min_length=5, max_length=200)
    complete: bool


@app.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency_injection):
    return db.query(Todos).all()


@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency_injection, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')


@app.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency_injection, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()


@app.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency_injection, request_update: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found in todos list')
    todo_model.title = request_update.title
    todo_model.priority = request_update.priority
    todo_model.complete = request_update.complete
    todo_model.description = request_update.description

    db.add(todo_model)
    db.commit()


@app.delete('/todos/delete_todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency_injection, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found in todos list')
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()

