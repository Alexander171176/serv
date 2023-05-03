from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.model.base import Base
from app.model.user import User
from app.core.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class AsyncDatabaseSession:

    def __init__(self) -> None:
        self.async_session_maker = None
        self.engine = None
        self.session = None

    def __getattr__(self, name):
        return getattr(self.async_session_maker(), name)

    def init(self):
        self.engine = create_async_engine(DATABASE_URL)
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_db_and_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self.session:
            self.init()
        async with self.async_session_maker() as session:
            yield session


db = AsyncDatabaseSession()


async def get_user_db(session: AsyncSession = Depends(db.get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
