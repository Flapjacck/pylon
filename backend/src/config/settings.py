"""Application configuration and environment settings.

This module uses Pydantic BaseSettings to manage environment variables
and provide type-safe configuration across the application.
"""

from pydantic import ConfigDict, field_validator
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
        cors_origins: List of allowed CORS origins for frontend requests (comma-separated)
        environment: Runtime environment (development/production)
    """
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra environment variables
    )

    api_title: str = "Title"
    api_version: str = "0.1.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:5173"]
    environment: str = "development"
    
    # Terraria server configuration
    terraria_config_path: str = "/opt/pylon/servers/"
    """Base path on the host where Terraria server configs and worlds are stored"""
    
    terraria_docker_image_vanilla: str = "passivelemon/terraria-docker:terraria-latest"
    """Docker image for vanilla Terraria servers"""
    
    terraria_docker_image_modded: str = "passivelemon/terraria-docker:tmodloader-latest"
    """Docker image for modded Terraria servers with tModLoader support"""
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins from environment variables."""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


# Create global settings instance
settings = Settings()
