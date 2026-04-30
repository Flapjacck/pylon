"""Docker container management - start, stop, and status operations."""

import logging
import sys
from typing import Optional, Any
import docker
from docker.errors import APIError, NotFound

logger = logging.getLogger(__name__)


class DockerManager:
    """Manager class for Docker container operations."""

    def __init__(self):
        """Initialize Docker client."""
        try:
            # Direct socket connection - most reliable method
            self.client = docker.DockerClient(base_url='unix:///run/docker.sock')
            logger.info("Docker client initialized successfully via socket")
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to initialize Docker client: {error_msg}")
            logger.error(
                "Make sure Docker daemon is running. On Linux: systemctl start docker. "
                "Check that /run/docker.sock exists and is readable."
            )
            self.client = None

    def start_container(self, name: str) -> dict:
        """
        Start a Docker container.

        Args:
            name (str): Name or ID of the container to start

        Returns:
            dict with keys:
                - success (bool): Whether operation succeeded
                - message (str): Status message or error description
        """
        if not self.client:
            return {
                "success": False,
                "message": "Docker daemon is not running or unreachable. Check logs for details."
            }

        try:
            container = self.client.containers.get(name)
            
            # Check if already running
            if container.status == "running":
                return {
                    "success": False,
                    "message": f"Container '{name}' is already running"
                }
            
            container.start()
            logger.info(f"Started container: {name}")
            return {
                "success": True,
                "message": f"Container '{name}' started successfully"
            }
        
        except NotFound:
            error_msg = f"Container '{name}' not found"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg
            }
        
        except APIError as e:
            error_msg = f"Docker daemon error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": "Docker daemon unreachable or API error"
            }
        
        except Exception as e:
            error_msg = f"Error starting container '{name}': {e}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": str(e)
            }

    def stop_container(self, name: str) -> dict:
        """
        Stop a Docker container.

        Args:
            name (str): Name or ID of the container to stop

        Returns:
            dict with keys:
                - success (bool): Whether operation succeeded
                - message (str): Status message or error description
        """
        if not self.client:
            return {
                "success": False,
                "message": "Docker daemon is not running or unreachable. Check logs for details."
            }

        try:
            container = self.client.containers.get(name)
            
            # Check if already stopped
            if container.status == "exited":
                return {
                    "success": False,
                    "message": f"Container '{name}' is already stopped"
                }
            
            container.stop()
            logger.info(f"Stopped container: {name}")
            return {
                "success": True,
                "message": f"Container '{name}' stopped successfully"
            }
        
        except NotFound:
            error_msg = f"Container '{name}' not found"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg
            }
        
        except APIError as e:
            error_msg = f"Docker daemon error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": "Docker daemon unreachable or API error"
            }
        
        except Exception as e:
            error_msg = f"Error stopping container '{name}': {e}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": str(e)
            }

    def get_status(self, name: str) -> dict:
        """
        Get status of a Docker container.

        Args:
            name (str): Name or ID of the container

        Returns:
            dict with keys:
                - success (bool): Whether operation succeeded
                - message (str): Status message
                - data (dict): Container status information if successful
        """
        if not self.client:
            return {
                "success": False,
                "message": "Docker daemon is not running or unreachable. Check logs for details.",
                "data": None
            }

        try:
            container = self.client.containers.get(name)
            
            # Extract relevant status information
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
            
            logger.info(f"Retrieved status for container: {name}")
            return {
                "success": True,
                "message": f"Status retrieved for '{name}'",
                "data": status_info
            }
        
        except NotFound:
            error_msg = f"Container '{name}' not found"
            logger.error(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "data": None
            }
        
        except APIError as e:
            error_msg = f"Docker daemon error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": "Docker daemon unreachable or API error",
                "data": None
            }
        
        except Exception as e:
            error_msg = f"Error retrieving status for '{name}': {e}"
            logger.error(error_msg)
            return {
                "success": False,
                "message": str(e),
                "data": None
            }


def display_status_details(status_data: dict) -> None:
    """
    Pretty-print container status details.

    Args:
        status_data (dict): Status information from get_status()
    """
    print("\n" + "=" * 60)
    print(f"Container: {status_data['name']}")
    print("=" * 60)
    print(f"ID:         {status_data['id']}")
    print(f"Status:     {status_data['status']}")
    print(f"Running:    {status_data['running']}")
    print(f"Paused:     {status_data['paused']}")
    print(f"Restarting: {status_data['restarting']}")
    print(f"Image:      {status_data['image']}")
    print(f"PID:        {status_data['pid']}")
    print(f"Exit Code:  {status_data['exit_code']}")
    print(f"Started:    {status_data['started_at']}")
    print(f"Finished:   {status_data['finished_at']}")
    print("=" * 60 + "\n")


def interactive_menu(container_name: str) -> None:
    """
    Display interactive menu for container operations.

    Args:
        container_name (str): Name of the container to operate on
    """
    manager = DockerManager()
    
    while True:
        print(f"\n{'=' * 60}")
        print(f"Container Manager: {container_name}")
        print(f"{'=' * 60}")
        print("[1] Start")
        print("[2] Stop")
        print("[3] Status")
        print("[4] Exit")
        print(f"{'=' * 60}")
        
        choice = input("Choose action (1-4): ").strip()
        
        if choice == "1":
            print(f"\nStarting container '{container_name}'...")
            result = manager.start_container(container_name)
            print(f"Result: {result['message']}")
        
        elif choice == "2":
            print(f"\nStopping container '{container_name}'...")
            result = manager.stop_container(container_name)
            print(f"Result: {result['message']}")
        
        elif choice == "3":
            print(f"\nFetching status for container '{container_name}'...")
            result = manager.get_status(container_name)
            if result['success']:
                display_status_details(result['data'])
            else:
                print(f"Error: {result['message']}")
        
        elif choice == "4":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check for container name argument
    if len(sys.argv) < 2:
        print("Usage: python manager.py <container_name>")
        print("Example: python manager.py my_container")
        sys.exit(1)
    
    container_name = sys.argv[1]
    interactive_menu(container_name)
