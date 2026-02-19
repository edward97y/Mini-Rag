from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME:str
    APP_VERSION:str

    FILE_UPLOAD_EXTNSIONS:list[str]
    FILE_MAX_SIZE:int

    FILE_DEFAULT_CHUNK_SIZE:int

    MONGO_DB_URL:str
    MONGO_DB_NAME:str

    NVIDIA_API_KEY:str
    NVIDIA_BASE_URL:str
    NVIDIA_MODEL:str
    GENERATION_MODEL_BACK_END:str

    EMBED_MODEL:str
    EMBED_SIZE:int
    EMBED_URL:str


    DEFAULT_OUTPUT_MAX_CHARACTERS:int
    DEFAULT_TEMPERATURE:float
    DEFAULT_INPUT_MAX_CHARACTERS:int

    GEMINI_API_KEY:str
    GOOGLE_EMBED_MODEL_PROVIDER:str
    GOOGLE_GENERATE_MODEL_PROVIDER:str
    GOOGLE_EMBED_SIZE:int
    GOOGLE_GENERATE_MODEL:str
    GOOGLE_EMBED_MODEL:str

    DB_PATH:str
    DISTANCE_DataBase_Matrix:str
    DATA_BASE_PROVIDER:str

    COHERE_API_KEY:str
    COHERE_EMBEDDING_MODEL_ID:str
    COHERE_EMBEDDING_MODEL_SIZE:int
    COHERE_EMBED_MODEL_PROVIDER:str


    DEFAULT_LANGUAGE:str
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()