from pydantic_settings import BaseSettings
from typing import List
from pydantic import validator

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./coffee_shop.db"
    
    # JWT Settings
    secret_key: str = "your-super-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000"
    allowed_credentials: bool = True
    allowed_methods: str = "GET,POST,PUT,DELETE,OPTIONS"
    allowed_headers: str = "*"
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    # Environment
    environment: str = "development"
    
    # Logging
    log_level: str = "INFO"
    
    @validator('allowed_origins')
    def parse_origins(cls, v):
        if isinstance(v, str):
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
