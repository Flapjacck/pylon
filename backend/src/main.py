"""FastAPI application factory and server entry point.

This module initializes the FastAPI application with middleware configuration,
registers all route modules, and provides the uvicorn server entry point.
All requests from the Vite frontend (localhost:5173) are allowed via CORS.
"""

import logging
import socket
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import Dict, Any

from .config import settings
from .routes import health_router, docker_router

# Configure logging for request/response tracking
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Sets up:
    - CORS middleware for frontend requests from Vite
    - Trusted host middleware for security
    - All route modules (health, future features)
    - Root metadata endpoint
    
    Returns:
        FastAPI: Configured application instance ready for uvicorn
    """
    
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="T",
    )

    # CORS Middleware: Allow requests from Vite frontend dev server
    # In production, update cors_origins in .env to match your domain
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Security: Only allow requests from trusted hosts
    # Prevents DNS rebinding attacks
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*"],  # "*" for dev; tighten in production
    )

    # Register route modules
    app.include_router(health_router)
    app.include_router(docker_router)

    # Root endpoint: Returns API metadata
    @app.get("/", response_model=Dict[str, Any])
    async def root() -> Dict[str, Any]:
        """
        API root endpoint.
        
        Returns:
            dict: API metadata including title, version, and status
        """
        return {
            "message": "Hey bro",
            "version": settings.api_version,
            "status": "running"
        }

    # Mount static files (favicon, site.webmanifest, etc.) at root LAST
    # After all other routes to avoid catching API requests
    # Serve favicon files directly at / (e.g., /favicon.ico, /site.webmanifest)
    static_path = Path(__file__).parent.parent / "public"
    if static_path.exists():
        app.mount("/", StaticFiles(directory=str(static_path), html=False), name="static")

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    # Get network IP address for cross-device access
    try:
        # Create a socket connection to determine local IP
        # (doesn't actually connect, just determines the IP that would be used)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        network_ip = sock.getsockname()[0]
        sock.close()
    except Exception:
        # Fallback if network detection fails
        network_ip = socket.gethostbyname(socket.gethostname())
    
    logger.info(f"Server running at http://{network_ip}:{settings.api_port}")
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
    )
