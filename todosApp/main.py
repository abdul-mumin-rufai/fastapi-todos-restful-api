from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

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


@app.get('/')
async def read_all(db: db_dependency_injection):
    return db.query(Todos).all()


@app.get('/todo/{todo_id}')
async def get_todo_by_id(db: db_dependency_injection, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')
