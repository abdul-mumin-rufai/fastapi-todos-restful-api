from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# this tells that our database is in the todosApp  folder
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

# this is the engine of to our database and connect_args is st to false because we want our db to have multiple thread
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

