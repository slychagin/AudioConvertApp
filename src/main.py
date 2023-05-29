import uuid
from typing import Type

from fastapi import FastAPI, APIRouter
from fastapi_users import schemas

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.audios.router import router as router_audios

app = FastAPI(
    title="Audio Convert App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Authentication"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(router_audios)
