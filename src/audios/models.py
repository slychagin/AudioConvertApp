import uuid

from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users_db_sqlalchemy.generics import GUID

from src.auth.models import User
from src.database import Base


class Audio(Base):
    """
    Create table in the database where save audio files in mp3 format
    """
    __tablename__ = 'audios'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid_token: Mapped[uuid.UUID] = mapped_column(GUID, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(length=100), nullable=False)
    audio_file = Column(LargeBinary, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
