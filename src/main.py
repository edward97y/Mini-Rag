from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings=get_settings()
    app.mongodb_client=AsyncIOMotorClient(settings.MONGO_DB_URL)
    app.db_client=app.mongodb_client[settings.MONGO_DB_NAME]
    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)