"""Controller for listing Terraria servers."""

from docker import DockerClient
from docker.errors import APIError
from ..schemas.terraria import TerrariaServerInfo, TerrariaServerListResponse


async def list_servers_controller(
    docker_client: DockerClient,
) -> TerrariaServerListResponse:
    """
    List all Terraria servers (all Docker containers with names starting with 'terraria-').
    
    Args:
        docker_client: Docker SDK client
    
    Returns:
        TerrariaServerListResponse with list of all servers
    
    Raises:
        APIError: If Docker operation fails
    """
    try:
        # Get all containers (running and stopped)
        all_containers = docker_client.containers.list(all=True)
        
        # Filter to only Terraria servers (names start with 'terraria-')
        terraria_servers = [c for c in all_containers if c.name.startswith("terraria-")]
        
        servers_list = []
        for container in terraria_servers:
            try:
                server_info = _extract_server_info(container)
                if server_info:
                    servers_list.append(server_info)
            except Exception as e:
                # Log but continue processing other containers
                # In production, you might want to log this error
                continue
        
        return TerrariaServerListResponse(
            success=True,
            data=servers_list,
            count=len(servers_list),
        )
    
    except APIError as e:
        return TerrariaServerListResponse(
            success=False,
            data=[],
            count=0,
        )
    except Exception as e:
        return TerrariaServerListResponse(
            success=False,
            data=[],
            count=0,
        )


def _extract_server_info(container) -> TerrariaServerInfo:
    """
    Extract Terraria server information from a Docker container.
    
    Args:
        container: Docker container object
    
    Returns:
        TerrariaServerInfo with server details extracted from container
    """
    # Get basic container info
    container_id = container.short_id
    server_name = container.name
    status = container.status
    
    # Extract environment variables from container config
    env_vars = {}
    if container.attrs and "Config" in container.attrs and "Env" in container.attrs["Config"]:
        for env_str in container.attrs["Config"]["Env"]:
            if "=" in env_str:
                key, value = env_str.split("=", 1)
                env_vars[key] = value
    
    # Determine server type based on image name
    image_name = ""
    if container.image and container.image.tags:
        image_name = container.image.tags[0] if container.image.tags else ""
    
    server_type = "modded" if "tmodloader" in image_name.lower() else "vanilla"
    
    # Extract configuration from environment variables
    worldname = env_vars.get("WORLDNAME", "World")
    port = int(env_vars.get("PORT", 7777))
    difficulty = int(env_vars.get("DIFFICULTY", 0))
    max_players = int(env_vars.get("MAXPLAYERS", 8))
    has_password = "PASSWORD" in env_vars
    
    return TerrariaServerInfo(
        container_id=container_id,
        server_name=server_name,
        server_type=server_type,
        status=status,
        port=port,
        worldname=worldname,
        difficulty=difficulty,
        max_players=max_players,
        has_password=has_password,
    )
