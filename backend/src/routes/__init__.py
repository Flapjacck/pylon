"""Application routes module.

This package organizes all API routes by feature/domain.
Each module exports an APIRouter that is registered in the main application.
"""

from .health import router as health_router

__all__ = ["health_router"]
