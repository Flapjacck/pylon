"""Get container status controller."""

import logging
from docker.client import DockerClient
from docker.errors import APIError, NotFound
from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def get_container_status_controller(
    container_id: str,
    docker_client: DockerClient
) -> dict:
    """
    Get detailed status of a specific Docker container.
    
    Args:
        container_id: Container ID or name
        docker_client: Docker client instance from dependency injection
        
    Returns:
        dict with success=True and data containing detailed container status:
            - id, name, status, running, paused, restarting
            - pid, exit_code, started_at, finished_at, image
            
    Raises:
        HTTPException(404): If container not found
        HTTPException(500): If Docker daemon error occurs
    """
    try:
        container = docker_client.containers.get(container_id)
        
        # Extract detailed status information
        state = container.attrs.get("State", {})
        status_info = {
            "id": container.id[:12],
            "name": container.name,
            "status": container.status,
            "running": state.get("Running", False),
            "paused": state.get("Paused", False),
            "restarting": state.get("Restarting", False),
            "pid": state.get("Pid", None),
            "exit_code": state.get("ExitCode", None),
            "started_at": state.get("StartedAt", None),
            "finished_at": state.get("FinishedAt", None),
            "image": container.attrs.get("Config", {}).get("Image", ""),
        }
        
        logger.info(f"Retrieved status for container: {container_id}")
        
        return {
            "success": True,
            "data": status_info
        }
        
    except NotFound:
        error_msg = f"Container '{container_id}' not found"
        logger.error(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)
        
    except APIError as e:
        error_msg = f"Docker API error: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail="Docker daemon error")
        
    except Exception as e:
        error_msg = f"Error getting container status: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail="Failed to get container status")
