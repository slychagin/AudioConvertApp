import uuid

from fastapi_users import models
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr
from pydantic.schema import Generic


class BaseUser(Generic[models.ID], CreateUpdateDictModel):
    """
    Redefine fastapi_users.schema.BaseUser class
    from fastapi-users module.
    """
    id: models.ID
    email: EmailStr

    class Config:
        orm_mode = True


class BaseUserCreate(CreateUpdateDictModel):
    """
    Redefine fastapi_users.schema.BaseUserCreate class
    from fastapi-users module.
    """
    email: EmailStr
    password: str


class UserRead(BaseUser[int]):
    id: int
    uuid_token: uuid.UUID
    username: str


class UserCreate(BaseUserCreate):
    username: str
