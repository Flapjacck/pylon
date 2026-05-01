"""Docker client initialization and management utilities."""

import logging
from typing import Optional
import docker
from docker.client import DockerClient

logger = logging.getLogger(__name__)


def get_docker_client() -> Optional[DockerClient]:
    """
    Initialize and return a Docker client.
    
    Attempts to connect to Docker daemon via Unix socket (most reliable method).
    Falls back gracefully if Docker is not available.
    
    Returns:
        Optional[DockerClient]: Docker client instance if successful, None otherwise
        
    Raises:
        Logs errors but does not raise exceptions - returns None on failure
    """
    try:
        # Direct socket connection - most reliable method
        client = docker.DockerClient(base_url='unix:///run/docker.sock')
        logger.info("Docker client initialized successfully via socket")
        return client
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to initialize Docker client: {error_msg}")
        logger.error(
            "Make sure Docker daemon is running. On Linux: systemctl start docker. "
            "Check that /run/docker.sock exists and is readable."
        )
        return None
