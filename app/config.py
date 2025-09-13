from pydantic_settings import BaseSettings
from typing import List
from pydantic import validator
import os

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./coffee_shop.db")
    
    # JWT Settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS Settings
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")
    allowed_credentials: bool = True
    allowed_methods: str = "GET,POST,PUT,DELETE,OPTIONS"
    allowed_headers: str = "*"
    
    # Rate Limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = 60
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    @validator('database_url')
    def fix_postgres_url(cls, v):
        # Heroku provides postgres:// but SQLAlchemy 1.4+ requires postgresql://
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v
    
    @validator('allowed_origins')
    def parse_origins(cls, v):
        if isinstance(v, str):
            if v == "*":
                return ["*"]  # Allow all origins for testing
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('allowed_methods')
    def parse_methods(cls, v):
        if isinstance(v, str):
            return [method.strip() for method in v.split(',')]
        return v
    
    @validator('allowed_headers')
    def parse_headers(cls, v):
        if isinstance(v, str):
            return [header.strip() for header in v.split(',')]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
