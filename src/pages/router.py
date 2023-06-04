import uuid

from fastapi import (
    APIRouter,
    Request,
    Form,
    UploadFile,
    File,
    Depends,
    HTTPException
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, JSONResponse

from src.audios.router import upload_file, download_file
from src.auth.schemas import UserCreate
from src.database import get_async_session

router = APIRouter(
    prefix='/html',
    tags=['HTML Template']
)


templates = Jinja2Templates(directory='src/templates')


@router.get('/', response_class=HTMLResponse)
def get_index_template(request: Request):
    """Return index template"""
    return templates.TemplateResponse('index.html', {'request': request})


@router.post('/upload')
async def post_index_template(
        request: Request,
        user_id: int = Form(ge=1),
        uuid_token: str = Form(...),
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Return converted audio data"""
    try:
        uuid_token_hex = uuid.UUID(uuid_token)
        result = await upload_file(
            user_id=user_id,
            user_uuid_token=uuid_token_hex,
            audio_file=file,
            request=request,
            session=session
        )
    except ValueError:
        raise HTTPException(
            400, detail='This is not UUID format!'
                        '<br>UUID token example:'
                        '<br>f4c74013-9e09-41de-8681-08546a2ed6bf'
        )
    return JSONResponse(content=result)


@router.get('/download', response_class=HTMLResponse)
def get_download_template(request: Request):
    """Return download template"""
    return templates.TemplateResponse('download.html', {'request': request})


@router.post('/download')
async def download_audio(
        request: Request,
        record_id: int = Form(ge=1),
        user_id: int = Form(ge=1),
        session: AsyncSession = Depends(get_async_session)
):
    """Download audio from database"""
    audio_file = await download_file(
        record_id=record_id,
        user_id=user_id,
        session=session
    )
    if audio_file:
        link = str(request.base_url).split('?')[0]
        params = f'?id={record_id}&user={user_id}'
        download_link = link + 'record/' + params
        return download_link


@router.get('/register', response_class=HTMLResponse)
def get_register_template(request: Request):
    """Return registration template"""
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register')
async def register_user(
        request: Request,
        user_data=Depends(UserCreate),
        email: str = Form(...),
        password: str = Form(...),
        username: str = File(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Register new user in the database"""
    print(user_data)
    print(email, password, username)
