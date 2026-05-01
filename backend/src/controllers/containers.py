"""Docker container management utilities."""

import logging
from typing import Optional, Any
import docker
from docker.errors import APIError

logger = logging.getLogger(__name__)


def get_docker_client() -> Optional[Any]:
    """
    Get a Docker client and test daemon connection.
    
    Returns:
        Docker client if connection successful, None otherwise
    """
    try:
        # Direct socket connection for Linux
        client = docker.DockerClient(base_url='unix:///run/docker.sock')
        # Test connection by pinging the daemon
        client.ping()
        logger.info("Docker daemon connection successful")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Docker daemon: {e}")
        return None


def list_containers() -> dict:
    """
    List all running containers.
    
    Returns:
        dict with keys:
            - success (bool): Whether operation succeeded
            - containers (list): List of running containers
            - count (int): Number of containers
            - error (str): Error message if failed
    """
    try:
        # Get Docker client
        client = get_docker_client()
        if not client:
            return {
                "success": False,
                "containers": [],
                "count": 0,
                "error": "Docker daemon is not running or unreachable"
            }
        
        # List all containers (not just running)
        containers = client.containers.list(all=True)
        
        container_list = []
        for container in containers:
            container_list.append({
                "id": container.id[:12],
                "name": container.name,
                "status": container.status,
                "image": container.attrs.get("Config", {}).get("Image", "")
            })
        
        logger.info(f"Retrieved {len(container_list)} containers")
        return {
            "success": True,
            "containers": container_list,
            "count": len(container_list),
            "error": None
        }
    
    except APIError as e:
        error_msg = f"Docker API error: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "containers": [],
            "count": 0,
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Error listing containers: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "containers": [],
            "count": 0,
            "error": error_msg
        }


if __name__ == "__main__":
    import json
    
    print("=== All Containers ===")
    result = list_containers()
    print(json.dumps(result, indent=2))