from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    table_name: str = "currencies"

settings = Settings()