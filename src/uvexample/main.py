
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from uvexample.database import get_db
from uvexample.models import User

from .routers.users import router as user_router

app = FastAPI()

app.include_router(user_router)
