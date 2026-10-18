from fastapi import FastAPI, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()


app.mount('/static', StaticFiles(directory='todosApp/static'), name='static')  # connecting the css and js to the app


@app.get("/")
def test():
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)


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
