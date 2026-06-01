"""Delete/destroy Terraria server controller with graceful cleanup."""

import asyncio
import logging
import shutil
from pathlib import Path
from docker.client import DockerClient
from docker.errors import APIError, NotFound
from fastapi import HTTPException

logger = logging.getLogger(__name__)


async def delete_terraria_server_controller(
    server_name: str,
    docker_client: DockerClient,
    config_path: str,
    save_wait_seconds: float = 3.0
) -> dict:
    """
    Delete a Terraria server container and its data directory with graceful shutdown.
    
    Performs the following steps:
    1. Resolves the server name to a container
    2. Gracefully stops the container if running (injects /save command)
    3. Removes the Docker container
    4. Removes the host directory containing server data
    
    This ensures safe cleanup without data corruption.
    
    Args:
        server_name: The name of the Terraria server (e.g., 'terraria-1' or 'my-server')
        docker_client: Docker client instance from dependency injection
        config_path: Base path on host where server configs are stored (e.g., '/opt/pylon/servers/')
        save_wait_seconds: Time to wait after injecting /save command before stopping (default: 3.0)
        
    Returns:
        dict with success=True and data containing:
            - message: Status message
            - server_name: The server name that was deleted
            - container_id: The container ID that was deleted
            
    Raises:
        HTTPException(404): If server/container not found
        HTTPException(500): If Docker daemon or filesystem error occurs
    """
    try:
        # Resolve server_name to container
        container = _resolve_server_container(server_name, docker_client)
        container_id = container.short_id
        
        # Gracefully shutdown if running
        if container.status == "running":
            try:
                await _graceful_shutdown(
                    container,
                    docker_client,
                    save_wait_seconds
                )
                logger.info(f"Graceful shutdown completed for container {container_id}")
            except Exception as e:
                logger.warning(f"Graceful shutdown failed for '{server_name}': {str(e)}. Forcing stop.")
                try:
                    container.stop()
                except Exception as stop_error:
                    logger.error(f"Force stop also failed: {str(stop_error)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to stop server '{server_name}': {str(stop_error)}"
                    )
        
        # Remove the Docker container
        try:
            docker_client.containers.get(container_id).remove()
            logger.info(f"Removed Docker container {container_id}")
        except Exception as e:
            error_msg = f"Failed to remove container '{server_name}': {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        # Remove the host directory
        host_dir = Path(config_path) / container.name
        if host_dir.exists():
            try:
                shutil.rmtree(host_dir)
                logger.info(f"Removed host directory: {host_dir}")
            except Exception as e:
                error_msg = f"Failed to remove server data directory '{host_dir}': {str(e)}"
                logger.error(error_msg)
                # Note: Container is already removed, but data cleanup failed
                raise HTTPException(status_code=500, detail=error_msg)
        else:
            logger.warning(f"Host directory '{host_dir}' does not exist or was already removed")
        
        logger.info(f"Successfully deleted Terraria server: {server_name}")
        
        return {
            "success": True,
            "data": {
                "message": f"Terraria server '{server_name}' deleted successfully with full cleanup",
                "server_name": server_name,
                "container_id": container_id
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
        error_msg = f"Docker daemon error while deleting server '{server_name}': {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected error deleting Terraria server '{server_name}': {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


async def _graceful_shutdown(
    container,
    docker_client: DockerClient,
    save_wait_seconds: float
) -> bool:
    """
    Perform graceful shutdown of Terraria server by injecting save command.
    
    Uses the passivelemon/terraria-docker image's command injection feature
    to safely save the world before stopping.
    
    Args:
        container: Docker container object
        docker_client: Docker client instance
        save_wait_seconds: Time to wait after save before stopping
        
    Returns:
        True if graceful shutdown succeeded, False otherwise
    """
    try:
        container_id = container.short_id
        logger.info(f"Starting graceful shutdown for container {container_id}")
        
        # Inject /save command via docker exec
        # The passivelemon/terraria-docker image supports: docker exec <id> inject "<command>"
        exec_result = docker_client.containers.get(container_id).exec_run(
            cmd='inject "/save"',
            stdout=True,
            stderr=True
        )
        
        if exec_result.exit_code != 0:
            logger.warning(
                f"Save command returned non-zero exit code: {exec_result.exit_code}. "
                f"stderr: {exec_result.output.decode('utf-8', errors='ignore')}"
            )
            return False
        
        logger.info(f"Save command injected successfully for {container_id}")
        
        # Wait for save to complete
        await asyncio.sleep(save_wait_seconds)
        logger.info(f"Graceful shutdown wait period ({save_wait_seconds}s) complete for {container_id}")
        
        # Now stop the container
        docker_client.containers.get(container_id).stop()
        logger.info(f"Container {container_id} stopped after graceful shutdown")
        
        return True
        
    except Exception as e:
        logger.error(f"Graceful shutdown attempt failed: {str(e)}")
        return False


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
        error_msg = f"Error resolving server '{server_name}': {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
