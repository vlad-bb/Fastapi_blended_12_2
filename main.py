from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from connect import get_async_session, create_db_and_tables
from src.contacts.routes import router

app = FastAPI()
app.include_router(router, prefix='/api')


@app.on_event('startup')
async def on_startup(db: AsyncSession = Depends(get_async_session)):
    await create_db_and_tables()
