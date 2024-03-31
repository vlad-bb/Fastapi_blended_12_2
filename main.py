import uvicorn

from fastapi import FastAPI

from src.contacts.routes import router as contacts_router
from src.auth.routes import router as auth_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(contacts_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
