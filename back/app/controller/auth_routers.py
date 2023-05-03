from fastapi import APIRouter, Depends
from app.schema.user_schema import UserCreate, UserRead, UserUpdate
from app.core.database import User
from app.service.user_manager import auth_backend, fastapi_users

router = APIRouter()

current_user = fastapi_users.current_user()


@router.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


current_active_user = fastapi_users.current_user(active=True)


@router.get("/authenticated-route-active-user")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Приветствуем  {user.username}!"}


current_active_verified_user = fastapi_users.current_user(active=True, verified=True)


@router.get("/protected-route-active-verified-user")
def protected_route(user: User = Depends(current_active_verified_user)):
    return {"message": f"Приветствуем  {user.username}!"}


current_superuser = fastapi_users.current_user(active=True, superuser=True)


@router.get("/protected-route-superuser")
def protected_route(user: User = Depends(current_superuser)):
    return {"message": f"Приветствуем  {user.username}!"}


router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Авторизация"])

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["Авторизация"],)

router.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["Авторизация"],)

router.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["Авторизация"],)

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["Пользователь"],)


def include_routers(app):
    app.include_router(router)
