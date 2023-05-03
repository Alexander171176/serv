import uuid

from fastapi_users import schemas
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import EmailStr
from typing import Optional, TypeVar


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    password: Optional[str]
    email: Optional[EmailStr]
    role_id: int
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


U = TypeVar("U", bound=BaseUser)
UC = TypeVar("UC", bound=BaseUserCreate)
UU = TypeVar("UU", bound=BaseUserUpdate)
