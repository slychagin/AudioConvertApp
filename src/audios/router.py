import uuid
from io import BytesIO
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    Request,
    Response,
    File,
    HTTPException,
    Query
)
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pydub import AudioSegment

from src.audios.models import Audio
from src.auth.models import User
from src.database import get_async_session

router = APIRouter(
    prefix="/record",
    tags=["Audio converter"]
)


async def convert_wav_to_mp3(wav_file: UploadFile) -> BytesIO:
    """Convert .wav file to .mp3 with 'pydub' module"""
    file = BytesIO()
    wav_audio = AudioSegment.from_file(wav_file.file, format='wav')
    mp3_audio = wav_audio.export(file, format='mp3')
    return mp3_audio


async def create_file_name(file: UploadFile) -> str:
    """Parses the file name and appends to the extension .mp3"""
    file_name = file.filename
    if file_name[-4:] == '.wav':
        new_name = file_name.replace('.wav', '.mp3')
    else:
        new_name = file_name + '.mp3'
    return new_name


async def check_user(
        user_id: int,
        user_uuid_token: uuid.UUID,
        session: AsyncSession
):
    """Checks if the user exists in the database"""
    query = select(User).where(User.id == user_id, User.uuid_token == user_uuid_token)
    result = await session.execute(query)
    user_data = result.fetchone()
    return user_data


@router.post('/', response_description='Link for download your audio file in mp3 format')
async def upload_file(
        user_id: Annotated[
            int,
            Query(description='Enter your id received during registration')
        ],
        user_uuid_token: Annotated[
            uuid.UUID,
            Query(description='Enter your UUID token received during registration')
        ],
        audio_file: Annotated[
            UploadFile,
            File(
                alias='Audio .wav file',
                description="Add file in .wav format to convert him in mp3"
            )
        ],
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Upload file to the database by entered user id and uuid token,
    which you can get after registration.
    """
    # Check exists user in the database or not
    user = await check_user(user_id, user_uuid_token, session)

    if user:
        # Check audio format
        if audio_file.content_type != 'audio/wav':
            raise HTTPException(
                400, detail='This is not a wav format! '
                            'You need to upload an audio file in wav format.'
            )
        try:
            # Convert wav to mp3
            mp3_audio = await convert_wav_to_mp3(audio_file)

            # Save mp3 file to the database and return his id
            stmt = insert(Audio).values(
                filename=await create_file_name(audio_file),
                audio_file=mp3_audio.read(),
                user_id=user_id
            ).returning(Audio.id)
            result = await session.execute(stmt)

            mp3_audio.close()
            record_id = result.fetchone()[0]
            await session.commit()

            # Generate a link to download the file
            link = str(request.url).split('?')[0]
            params = f'?id={record_id}&user={user_id}'
            download_link = link + params
            return {
                'record_id': record_id,
                'user_id': user_id,
                'download_link': download_link
            }
        except Exception:
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'details': None
            })
    else:
        raise HTTPException(
            400, detail='User with this id and token does not exist! '
                        'Check your credentials or register a new user.'
        )


@router.get('/')
async def download_file(
        record_id: Annotated[
            int,
            Query(
                alias='id',
                description='Enter record ID'
            )
        ],
        user_id: Annotated[
            int,
            Query(
                alias='user',
                description='Enter user ID'
            )
        ],
        session: AsyncSession = Depends(get_async_session)
):
    """Download file by record and user id's"""
    query = select(Audio).where(Audio.id == record_id, Audio.user_id == user_id)
    result = await session.execute(query)
    file_data = result.fetchone()

    if file_data:

        headers = {
            'Content-Disposition': f'attachment; filename="{file_data[0].filename}"',
            'Content-Type': 'audio/mp3',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }
        return Response(file_data[0].audio_file, headers=headers)
    else:
        raise HTTPException(
            400, detail='Audio file with this parameters does not exists.'
        )
