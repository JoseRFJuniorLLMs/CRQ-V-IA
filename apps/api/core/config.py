import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "CRQ-V-IA - Prospecção Fiscal Inteligente"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./crqvia.db"
    )
    
    # Security / Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "crqv_super_secret_jwt_key_2026_fiscalizacao_rs")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 horas
    
    # Concurrency TR requirement (Mínimo 2 acessos simultâneos)
    MIN_CONCURRENT_USERS: int = 2
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

settings = Settings()
