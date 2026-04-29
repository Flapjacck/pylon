"""Docker container management utilities."""

import logging
from typing import Optional, Any
import subprocess
import json

logger = logging.getLogger(__name__)


def get_docker_client() -> Optional[Any]:
    """
    Test Docker daemon connection via CLI.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        # Test connection by running docker ps
        subprocess.run(['docker', 'ps'], capture_output=True, check=True, timeout=5)
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Docker daemon: {e}")
        return False


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
        # Use docker CLI to get running containers in JSON format
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{json .}}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or "Failed to list containers"
            logger.error(f"Docker error: {error_msg}")
            return {
                "success": False,
                "containers": [],
                "count": 0,
                "error": error_msg
            }
        
        # Parse JSON output - each line is a container
        container_list = []
        for line in result.stdout.strip().split('\n'):
            if line:
                container = json.loads(line)
                container_list.append({
                    "id": container.get('ID', '')[:12],
                    "name": container.get('Names', ''),
                    "status": container.get('Status', ''),
                    "image": container.get('Image', '')
                })
        
        return {
            "success": True,
            "containers": container_list,
            "count": len(container_list),
            "error": None
        }
    except subprocess.TimeoutExpired:
        error_msg = "Docker command timed out"
        logger.error(error_msg)
        return {
            "success": False,
            "containers": [],
            "count": 0,
            "error": error_msg
        }
    except Exception as e:
        logger.error(f"Error listing containers: {e}")
        return {
            "success": False,
            "containers": [],
            "count": 0,
            "error": str(e)
        }

if __name__ == "__main__":
    import json
    
    print("=== All Running Containers ===")
    result = list_containers()
    print(json.dumps(result, indent=2))