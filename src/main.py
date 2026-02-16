from fastapi import FastAPI
from routes import base,data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from Stores.llm.LLMProviderFactory import LLMProviderFactorys
from Stores.VectorDB.VectorDBFactory import DataBaseFactory
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings=get_settings()
    app.mongodb_client=AsyncIOMotorClient(settings.MONGO_DB_URL)
    app.db_client=app.mongodb_client[settings.MONGO_DB_NAME]

    llm_provider=LLMProviderFactorys(settings)
    app.generation_client=llm_provider.create(provider=settings.GENERATION_MODEL_BACK_END)
    app.generation_client.set_generation_model(model_id=settings.NVIDIA_MODEL)

    app.embed_client=llm_provider.create(provider=settings.EMBED_MODEL)
    app.embed_client.set_embedding_model(model_id=settings.NVIDIA_MODEL,embed_size=settings.EMBED_SIZE)

    vector_db_factory=DataBaseFactory(settings)
    app.vector_db_client=vector_db_factory.create_connection_with_db(settings.DATA_BASE_PROVIDER)

    app.vector_db_client.connect()


    yield
    app.mongodb_client.close()
    app.vector_db_client.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)