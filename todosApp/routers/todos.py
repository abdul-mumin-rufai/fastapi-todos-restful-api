from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from starlette import status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='todosApp/templates')

router = APIRouter(
    prefix='/todos',
    tags=['todos']
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


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    priority: int = Field(gt=0, lt=6)
    description: str = Field(min_length=5, max_length=200)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


# PAGES #

@router.get('/todo-page')
async def render_todo_page(request: Request, db: db_dependency_injection):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()  # type:ignore

        return templates.TemplateResponse(request, 'todos.html', context={'todos': todos, 'user': user})

    except:
        return redirect_to_login()


@router.get('/add-todo-page')
async def render_add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse(request, 'create-todo.html', context={'user': user})

    except:
        return redirect_to_login()


@router.get('/update-todo-page/{todo_id}')
async def render_update_todo(request: Request, db: db_dependency_injection, todo_id: int):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse(request, 'update-todo.html', context={'todo': todo, 'user': user})
    except:
        return redirect_to_login()


# ENDPOINTS #
@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_token_dependency, db: db_dependency_injection):
    if not user:
        raise HTTPException(status_code=401, detail='Could Not Authenticate User')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()  # type: ignore


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_token_dependency, db: db_dependency_injection, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()  # type: ignore
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_token_dependency, db: db_dependency_injection, todo_request: TodoRequest):
    if not user:
        raise HTTPException(status_code=401, detail='Could Not Authenticate User')
    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_token_dependency, db: db_dependency_injection,
                      request_update: TodoRequest, todo_id: int = Path(gt=0)):
    if not user:
        if not user:
            raise HTTPException(status_code=401, detail='Could Not Authenticate User')
    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()  # type: ignore
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found in todos list')
    todo_model.title = request_update.title
    todo_model.priority = request_update.priority
    todo_model.complete = request_update.complete
    todo_model.description = request_update.description

    db.add(todo_model)
    db.commit()


@router.delete('/todos/delete_todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_token_dependency, db: db_dependency_injection, todo_id: int = Path(gt=0)):
    if not user:
        if not user:
            raise HTTPException(status_code=401, detail='Could Not Authenticate User')
    todo_model = db.query(Todos).filter(Todos.id == todo_id). \
        filter(Todos.owner_id == user.get('id')).first()  # type: ignore
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found in todos list')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()  # type: ignore

    db.commit()
