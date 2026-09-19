import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Locate project root directory containing .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # NVIDIA NIM / LLM API (Loaded securely from .env file)
    NVIDIA_API_KEY: str = ""
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    LLM_MODEL: str = "nvidia/nemotron-3-ultra-550b-a55b"


    # JWT Authentication
    JWT_SECRET_KEY: str = "fitness_ai_super_secret_jwt_key_change_in_production_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Databases
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'fitness_ai.db'}"
    CHROMA_PERSIST_DIR: str = str(BASE_DIR / "chroma_db")

    # Product Data
    PRODUCTS_FILE: str = str(BASE_DIR / "backend" / "data" / "products.json")

    # Networking
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 8501
    BACKEND_URL: str = "http://127.0.0.1:8000"

    class Config:
        env_file = str(ENV_PATH)
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
