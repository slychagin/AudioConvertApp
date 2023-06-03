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

from src.audios.router import upload_file
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
    """Return index template"""
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
