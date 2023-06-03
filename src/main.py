from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.audios.router import router as router_audios
from src.pages.router import router as router_pages

app = FastAPI(
    title='Audio Convert App'
)

app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth',
    tags=['Authentication'],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Authentication'],
)

app.include_router(router_audios)
app.include_router(router_pages)

templates = Jinja2Templates(directory='src/templates')
