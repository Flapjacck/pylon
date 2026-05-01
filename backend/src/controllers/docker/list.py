"""List Docker containers controller."""

import logging
from docker.client import DockerClient
from docker.errors import APIError

logger = logging.getLogger(__name__)


async def list_containers_controller(docker_client: DockerClient) -> dict:
    """
    List all Docker containers (running and stopped).
    
    Args:
        docker_client: Docker client instance from dependency injection
        
    Returns:
        dict with success=True and data containing:
            - containers: List of container objects with id, name, status, image
            - count: Total number of containers
            
    Raises:
        HTTPException: Handled in route, controller raises with dict return
    """
    try:
        # Fetch all containers (running and stopped)
        containers = docker_client.containers.list(all=True)
        
        container_list = []
        for container in containers:
            container_info = {
                "id": container.id[:12],
                "name": container.name,
                "status": container.status,
                "image": container.attrs.get("Config", {}).get("Image", "")
            }
            container_list.append(container_info)
        
        logger.info(f"Retrieved {len(container_list)} containers")
        
        return {
            "success": True,
            "data": {
                "containers": container_list,
                "count": len(container_list)
            }
        }
        
    except APIError as e:
        error_msg = f"Docker API error while listing containers: {str(e)}"
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Error listing containers: {str(e)}"
        logger.error(error_msg)
        raise
