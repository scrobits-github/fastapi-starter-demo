from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.common.db import init_db
from app.routers import cricketers, health


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Awesome Project", lifespan=lifespan)

app.include_router(health.router)
app.include_router(cricketers.router)
