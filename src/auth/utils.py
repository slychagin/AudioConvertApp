from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Get User by session and User model"""
    yield SQLAlchemyUserDatabase(session, User)
