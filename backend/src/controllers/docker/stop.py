"""Stop container controller."""

import logging
from docker.client import DockerClient
from docker.errors import APIError, NotFound
from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def stop_container_controller(
    container_id: str,
    docker_client: DockerClient
) -> dict:
    """
    Stop a Docker container.
    
    Args:
        container_id: Container ID or name
        docker_client: Docker client instance from dependency injection
        
    Returns:
        dict with success=True and data containing:
            - message: Status message
            - container_id: The container ID/name that was stopped
            
    Raises:
        HTTPException(404): If container not found
        HTTPException(409): If container is already stopped
        HTTPException(500): If Docker daemon error occurs
    """
    try:
        container = docker_client.containers.get(container_id)
        
        # Check if already stopped
        if container.status == "exited":
            error_msg = f"Container '{container_id}' is already stopped"
            logger.warning(error_msg)
            raise HTTPException(status_code=409, detail=error_msg)
        
        # Stop the container
        container.stop()
        
        logger.info(f"Stopped container: {container_id}")
        
        return {
            "success": True,
            "data": {
                "message": f"Container '{container_id}' stopped successfully",
                "container_id": container_id
            }
        }
        
    except HTTPException:
        # Re-raise HTTPExceptions (already formatted)
        raise
        
    except NotFound:
        error_msg = f"Container '{container_id}' not found"
        logger.error(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)
        
    except APIError as e:
        error_msg = f"Docker API error: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail="Docker daemon error")
        
    except Exception as e:
        error_msg = f"Error stopping container '{container_id}': {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail="Failed to stop container")
