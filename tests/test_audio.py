import pytest
import magic
from httpx import AsyncClient
from pydub import AudioSegment
from sqlalchemy import select, insert

from src.audios.models import Audio
from src.auth.models import User
from tests.conftest import async_session_maker


@pytest.fixture()
async def add_user_to_db():
    """
    This fixture insert user to the database.
    """
    async with async_session_maker() as session:
        stmt = insert(User).values(
            email='example@gmail.com',
            hashed_password='password',
            username='Serhio',
        )
        await session.execute(stmt)
        await session.commit()


@pytest.fixture()
async def get_created_user():
    """
    This fixture insert user to the database.
    """
    async with async_session_maker() as session:
        query = select(User)
        result = await session.execute(query)
        return result.fetchone()[0]


async def test_convert_wav_to_mp3():
    """Test converting .wav file to .mp3"""
    AudioSegment.from_file('song.wav', format='wav').export('song.mp3', format='mp3')
    mime = magic.Magic(mime=True)

    assert mime.from_file('song.wav') == 'audio/x-wav'
    assert mime.from_file('song.mp3') == 'audio/mpeg'


async def test_create_file_name():
    """Test correct file name creating"""
    file_name_with_wav = 'song.wav'
    file_name_without_wav = 'song'
    result_name = 'song.mp3'

    new_name = file_name_with_wav.replace('.wav', '.mp3')
    assert new_name == result_name

    new_name = file_name_without_wav + '.mp3'
    assert new_name == result_name


async def test_check_user(add_user_to_db):
    """Test checking that user exists in the database"""
    async with async_session_maker() as session:
        query = select(User).where(
            User.email == 'example@gmail.com',
            User.username == 'Serhio'
        )
        result = await session.execute(query)
    user_data = result.fetchone()

    assert len(user_data) == 1
    assert user_data[0].email == 'example@gmail.com'
    assert user_data[0].username == 'Serhio'


async def test_upload_file(ac: AsyncClient, get_created_user):
    """Test that audio file in mp3 format was added to the database"""
    user = get_created_user

    response = await ac.post(
        '/record/',
        params={
            'user_id': user.id,
            'user_uuid_token': user.uuid_token,
        },
        files={'Audio .wav file': open('song.wav', 'rb')}
    )

    # Check record in the database
    async with async_session_maker() as session:
        query = select(Audio)
        result = await session.execute(query)
        loaded_files = result.fetchone()

    assert response.status_code == 200
    assert response.json()['download_link'] == 'http://test/record/?id=1&user=1'
    assert len(loaded_files) == 1


async def test_download_file(ac: AsyncClient, get_created_user):
    """Test that audio file in mp3 format was added to the database"""
    user = get_created_user

    response = await ac.get(
        '/record/',
        params={
            'id': 1,
            'user': user.id
        }
    )

    assert response.status_code == 200
    assert response.url == 'http://test/record/?id=1&user=1'
    assert response.headers['content-disposition'] == 'attachment; filename="song.mp3"'
    assert response.headers['content-type'] == 'audio/mp3'
