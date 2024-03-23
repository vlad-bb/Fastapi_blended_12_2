import typing
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from dotenv import load_dotenv
from os import getenv

import src.contacts.models


load_dotenv()
BASES = [
    src.contacts.models.Base.metadata
]
engine = create_async_engine(getenv('DB'))
async_session_maker = async_sessionmaker(engine)


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        for base in BASES:
            await conn.run_sync(base.create_all)
