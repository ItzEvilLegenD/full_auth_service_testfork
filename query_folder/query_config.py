import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Загружает переменные из .env

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@host:5432/db")

    class Config:
        env_file = ".env" # Указываем, что нужно читать из .env (хотя load_dotenv уже сделал это)
        extra = "ignore" # Игнорировать лишние переменные в .env

settings = Settings()