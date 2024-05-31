from fastapi import FastAPI
from ratings import *
from movies import *
import movies
import ratings
import models
from database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(movies.router)
app.include_router(ratings.router)
