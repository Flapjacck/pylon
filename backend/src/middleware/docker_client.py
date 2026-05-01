"""Docker client dependency injection for FastAPI route handlers."""

import logging
from typing import Optional
from fastapi import HTTPException
from docker.client import DockerClient
import docker

logger = logging.getLogger(__name__)


async def get_docker_client_dependency() -> DockerClient:
    """
    FastAPI dependency function that provides a fresh Docker client per request.
    
    Ensures always retrieving up-to-date container information by creating
    a new connection for each request. Raises HTTPException if Docker daemon
    is unavailable.
    
    Returns:
        DockerClient: Connected Docker client instance
        
    Raises:
        HTTPException: 500 if Docker daemon is unavailable or unreachable
    """
    try:
        # Create fresh client connection for this request
        client = docker.DockerClient(base_url='unix:///run/docker.sock')
        logger.debug("Docker client created for request")
        return client
    except Exception as e:
        error_msg = f"Failed to initialize Docker client: {str(e)}"
        logger.error(error_msg)
        logger.error(
            "Make sure Docker daemon is running. "
            "On Linux: systemctl start docker. "
            "Check that /run/docker.sock exists and is readable."
        )
        raise HTTPException(
            status_code=500,
            detail="Docker daemon unavailable"
        )
