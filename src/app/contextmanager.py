from fastapi.concurrency import asynccontextmanager
from fastapi import FastAPI
async def startup():
    ...

async def shutdown():
    ...

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield 
    await shutdown()
