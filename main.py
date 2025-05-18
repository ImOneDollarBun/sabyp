import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config import APP_PORT
from src import rout

app = FastAPI()
app.include_router(rout)
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def startup():
    ...


if __name__ == '__main__':
    asyncio.run(startup())
    uvicorn.run("main:app", port=int(APP_PORT), reload=True)
