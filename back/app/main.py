import uvicorn
from fastapi import FastAPI
from app.core.database import db
from app.controller.auth_routers import include_routers


# функция инициализации приложения
def init_app():
    db.init()  # инициализируем базу данных

    # создаем приложение
    app = FastAPI(
        title="IPTV",
        description="MicroService",
        version="1",
    )

    # функция-обработчик, вызываемая при запуске приложения
    @app.on_event("startup")
    async def on_startup():
        # Not needed if you setup a migration system like Alembic
        await db.create_db_and_tables()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    include_routers(app)

    return app


app = init_app()


# функция запуска приложения
def start():
    """Запускается с помощью "poetry run start" на корневом уровне """
    uvicorn.run("app.main:app", host="localhost", port=8000,
                reload=True)  # запускаем приложение с помощью uvicorn. Настройки указаны в параметрах.
