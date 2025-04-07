from pydantic_settings import BaseSettings
from typing import Dict, ClassVar

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    PG_DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/multi_tenant_pg_db"
    OPENAI_API_KEY: str = "dummy_key"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TENANT_MAPPING: ClassVar[Dict[str, Dict[str, any]]] = {
        "tenant_1": {"id": 1, "db_type": "postgresql"},
        "tenant_2": {"id": 2, "db_type": "postgresql"},
        "testtenant1": {"id": 3, "db_type": "sqlite"},
        "testtenant2": {"id": 4, "db_type": "sqlite"}
    }

    class Config:
        env_file = ".env"

settings = Settings()