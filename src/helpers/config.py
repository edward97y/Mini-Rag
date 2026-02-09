from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_UPLOAD_EXTNSIONS: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE:int
    MONGO_DB_URL:str
    MONGO_DB_NAME:str

    class Config:
        env_file = ".env"
def get_settings():
    return Settings()