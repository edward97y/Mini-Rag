from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from .Stores.llm.LLMProviderFactory import LLMProviderFactorys
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings=get_settings()
    app.mongodb_client=AsyncIOMotorClient(settings.MONGO_DB_URL)
    app.db_client=app.mongodb_client[settings.MONGO_DB_NAME]

    llm_provider=LLMProviderFactorys(settings)
    app.generation_client=llm_provider.create(provider=settings.GENERATION_MODEL_BACK_END)
    app.generation_client.set_generation_model(model_id=settings.NVIDIA_MODEL)

    app.embed_client=llm_provider.create(provider=settings.EMBED_MODEL)
    app.embed_client.set_embedding_model(model_id=settings.NVIDIA_MODEL,embed_size=300)

    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)