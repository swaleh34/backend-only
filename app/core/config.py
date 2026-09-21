from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Any
import json
import os
from pathlib import Path

class Settings(BaseSettings):
    # Project Information
    PROJECT_NAME: str = "Swaleh AI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Advanced Islamic AI Assistant"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # LLM API Keys
    GROQ_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    
    # Server Configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS: int = 1
    RELOAD: bool = True
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # Database Configuration
    DATABASE_TYPE: str = "sqlite"
    SQLITE_DB_NAME: str = "swaleh_islamic.db"
    
    # PostgreSQL Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "swaleh_admin"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "swaleh_islamic_db"
    POSTGRES_PORT: int = 5432
    
    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600
    
    # AI Model Configuration
    AI_MODEL_TYPE: str = "openai"
    OPENAI_API_KEY: Optional[str] = None
    AI_TEMPERATURE: float = 0.3
    AI_MAX_TOKENS: int = 2000
    
    # Islamic Content Settings
    QURAN_API_BASE: str = "https://api.alquran.cloud/v1"
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: List[str] = ["en", "ar", "ur", "fr", "es"]
    
    # Authentic Sources
    AUTHENTIC_TAFSIR: List[str] = [
        "Ibn Kathir", "Al-Tabari", "Al-Qurtubi",
        "Al-Jalalayn", "Al-Baghawi", "Al-Muyassar"
    ]
    
    AUTHENTIC_HADITH_COLLECTIONS: List[str] = [
        "Sahih Bukhari", "Sahih Muslim", "Sunan Abu Dawud",
        "Jami at-Tirmidhi", "Sunan an-Nasa'i", "Sunan Ibn Majah",
        "Muwatta Malik", "Musnad Ahmad"
    ]
    
    AUTHENTIC_MADHABS: List[str] = [
        "Hanafi", "Maliki", "Shafi'i", "Hanbali"
    ]
    
    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]
    
    # Monitoring
    ENABLE_METRICS: bool = True
    ENABLE_LOGGING: bool = True
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name in ["CORS_ORIGINS", "SUPPORTED_LANGUAGES",
                            "AUTHENTIC_TAFSIR", "AUTHENTIC_HADITH_COLLECTIONS",
                            "AUTHENTIC_MADHABS"]:
                return json.loads(raw_val)
            return raw_val

settings = Settings()

# Create required directories
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.LOGS_DIR, exist_ok=True)