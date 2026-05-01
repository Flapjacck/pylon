"""Application configuration and environment settings.

This module uses Pydantic BaseSettings to manage environment variables
and provide type-safe configuration across the application.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        api_title: FastAPI application title
        api_version: API semantic version
        api_host: Server bind address (default: 0.0.0.0)
        api_port: Server port (default: 8000)
        cors_origins: List of allowed CORS origins for frontend requests
        environment: Runtime environment (development/production)
    """

    api_title: str = "Title"
    api_version: str = "0.1.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:5173"]

    class Config:
        """Pydantic config - load from .env file in project root."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()
