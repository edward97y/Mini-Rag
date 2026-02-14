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
    PROVIDER_BACK_END:str

    EMBED_URL:str


    DEFAULT_OUTPUT_MAX_CHARACTERS:int
    DEFAULT_TEMPERATUR:float
    DEFAULT_INPUT_MAX_CHARACTERS:int
    

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()