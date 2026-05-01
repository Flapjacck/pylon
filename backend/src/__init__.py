"""Backend application modules.

Core package containing configuration, routes, and the FastAPI application instance.
"""

from .main import app, create_app

__all__ = ["app", "create_app"]
