"""Application routes module.

This package organizes all API routes by feature/domain.
Each module exports an APIRouter that is registered in the main application.
"""

from .health import router as health_router
from .docker import router as docker_router
from .terraria import router as terraria_router

__all__ = ["health_router", "docker_router", "terraria_router"]
