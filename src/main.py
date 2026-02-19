from fastapi import FastAPI
from routes import base,data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager
from Stores.llm.LLMProviderFactory import LLMProviderFactorys
from Stores.VectorDB.VectorDBFactory import DataBaseFactory
from Stores.llm.templates.template_parser import TemplateParser
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings=get_settings()
    app.mongodb_client=AsyncIOMotorClient(settings.MONGO_DB_URL)
    app.db_client=app.mongodb_client[settings.MONGO_DB_NAME]

    llm_provider=LLMProviderFactorys(settings)
    app.generation_client=llm_provider.create(provider=settings.GOOGLE_GENERATE_MODEL_PROVIDER)
    app.generation_client.set_generation_model(model_id=settings.GOOGLE_GENERATE_MODEL)

    app.embed_client=llm_provider.create(provider=settings.EMBED_MODEL)
    app.embed_client.set_embedding_model(model_id=settings.EMBED_URL,embed_size=settings.COHERE_EMBEDDING_MODEL_SIZE)

    vector_db_factory=DataBaseFactory(settings)
    app.vector_db_client=vector_db_factory.create_connection_with_db(settings.DATA_BASE_PROVIDER)

    app.vector_db_client.connect()


    app.template_parser=TemplateParser(language=settings.DEFAULT_LANGUAGE)


    yield   
    app.mongodb_client.close()
    app.vector_db_client.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)