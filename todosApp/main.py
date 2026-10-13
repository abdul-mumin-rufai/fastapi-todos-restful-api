from fastapi import FastAPI, Request
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()


templates = Jinja2Templates(directory='todosApp/templates')  # location of the html file


app.mount('/static', StaticFiles(directory='todosApp/static'), name='static')


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse(request, "home.html", context={})


@app.get('/healthy')
async def health_check():
    return {'status': 'Healthy'}


# this creates a new database
Base.metadata.create_all(bind=engine)
#  this includes the auth file as a router to connect the auth to the main port
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
