"""Start Terraria server controller."""

import logging
from docker.client import DockerClient
from docker.errors import APIError, NotFound
from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def start_terraria_server_controller(
    server_name: str,
    docker_client: DockerClient
) -> dict:
    """
    Start a Terraria server container by server name.
    
    Args:
        server_name: The name of the Terraria server (e.g., 'terraria-1' or 'my-server')
        docker_client: Docker client instance from dependency injection
        
    Returns:
        dict with success=True and data containing:
            - message: Status message
            - server_name: The server name that was started
            - container_id: The container ID that was started
            
    Raises:
        HTTPException(404): If server/container not found
        HTTPException(409): If server is already running
        HTTPException(500): If Docker daemon error occurs
    """
    try:
        # Resolve server_name to container
        container = _resolve_server_container(server_name, docker_client)
        
        # Check if already running
        if container.status == "running":
            error_msg = f"Terraria server '{server_name}' is already running"
            logger.warning(error_msg)
            raise HTTPException(status_code=409, detail=error_msg)
        
        # Start the container
        container.start()
        
        logger.info(f"Started Terraria server: {server_name} (container: {container.short_id})")
        
        return {
            "success": True,
            "data": {
                "message": f"Terraria server '{server_name}' started successfully",
                "server_name": server_name,
                "container_id": container.short_id
            }
        }
        
    except HTTPException:
        # Re-raise HTTPExceptions (already formatted)
        raise
        
    except NotFound:
        error_msg = f"Terraria server '{server_name}' not found"
        logger.error(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)
        
    except APIError as e:
        error_msg = f"Docker daemon error while starting server '{server_name}': {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected error starting Terraria server '{server_name}': {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


def _resolve_server_container(server_name: str, docker_client: DockerClient):
    """
    Resolve a server name to a Docker container object.
    
    Args:
        server_name: The name of the Terraria server (e.g., 'terraria-1' or 'my-server')
        docker_client: Docker client instance
        
    Returns:
        Docker container object
        
    Raises:
        HTTPException(404): If container not found
    """
    try:
        # Try to get container by exact name first
        try:
            container = docker_client.containers.get(server_name)
            if container.name.startswith("terraria-"):
                return container
        except NotFound:
            pass
        
        # Try with 'terraria-' prefix if not found
        prefixed_name = f"terraria-{server_name}"
        try:
            container = docker_client.containers.get(prefixed_name)
            return container
        except NotFound:
            pass
        
        # If still not found, list all terraria containers and search
        all_containers = docker_client.containers.list(all=True)
        terraria_containers = [c for c in all_containers if c.name.startswith("terraria-")]
        
        # Check for exact match or matching suffix
        for container in terraria_containers:
            if container.name == server_name or container.name == prefixed_name:
                return container
        
        # Not found
        raise HTTPException(status_code=404, detail=f"Terraria server '{server_name}' not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resolving server container '{server_name}': {str(e)}")
        raise HTTPException(status_code=404, detail=f"Terraria server '{server_name}' not found")
