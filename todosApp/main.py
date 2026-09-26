from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin

app = FastAPI()

# this creates a new database
models.Base.metadata.create_all(bind=engine)
#  this includes the auth file as a router to connect the auth to the main port
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
