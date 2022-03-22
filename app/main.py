from fastapi import FastAPI
from . import auth, users, models, recipes
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
db = SessionLocal()



app.include_router(auth.router)
app.include_router(users.router)
app.include_router(recipes.router)


