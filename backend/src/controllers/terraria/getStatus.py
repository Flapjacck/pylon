"""Controller for getting the status of a specific Terraria server."""

from docker import DockerClient
from docker.errors import APIError
from ...schemas.terraria import TerrariaServerStatusResponse, TerrariaServerInfo
from .listServers import _extract_server_info


def get_terraria_server_status_controller(
    server_name: str,
    docker_client: DockerClient,
) -> TerrariaServerStatusResponse:
    """
    Get the status of a specific Terraria server.
    
    Args:
        server_name: The name of the server container
        docker_client: Docker SDK client
    
    Returns:
        TerrariaServerStatusResponse with server status details
    """
    try:
        # Try to get the container by name
        container = docker_client.containers.get(server_name)
        
        # Extract server info from container
        server_info = _extract_server_info(container)
        
        return TerrariaServerStatusResponse(
            success=True,
            data=server_info,
        )
    
    except Exception as e:
        return TerrariaServerStatusResponse(
            success=False,
            data=None,
            error=f"Server '{server_name}' not found or error retrieving status: {str(e)}",
        )
