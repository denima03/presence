import secrets
import os
from typing import List, Union

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "localhost"
    SERVER_HOST: AnyHttpUrl = "http://localhost"

    OPENAI_API_TYPE: str = "azure"
    OPENAI_API_KEY: str = ""
    OPENAI_API_VERSION: str = "2023-03-15-preview"
    OPENAI_API_BASE: str = ""
    OPENAI_API_ENGINE: str = "gpt3.5-turbo"
    OPENAI_API_DEPLOYMENT: str = "lunaAIChat"
    OPENAI_API_DEPLOYMENT_EMBEDDING: str = "lunaAIEmbedding"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://127.0.0.1:5173",
    ]
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgres://postgres:password@localhost/presence"
    )

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "FastAPI"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
