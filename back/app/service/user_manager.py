import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas, models, exceptions
from fastapi_users.authentication import (AuthenticationBackend, BearerTransport, JWTStrategy, CookieTransport, )
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.database import User, get_user_db

SECRET = "SECRET"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"Пользователь {user.username} зарегистрирован.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Пользователь {user.username} забыл свой пароль. Сбросить токен: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Проверка, запрошенная для пользователя {user.username}. Проверочный токен: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

"""
У вас может быть столько серверных частей аутентификации, сколько вы пожелаете. 
Затем вам нужно будет передать эти серверные части своему FastAPIUsers экземпляру 
и сгенерировать маршрутизатор авторизации для каждого из них.
"""
# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(cookie_name="iptv", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# auth_backend2 = AuthenticationBackend(
#     name="bearer",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )

# Затем вам нужно будет передать эти серверные части своему FastAPIUsers экземпляру
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
