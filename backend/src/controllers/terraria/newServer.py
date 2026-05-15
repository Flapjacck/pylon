"""Controller for creating new Terraria servers."""

import os
from pathlib import Path
from docker import DockerClient
from docker.errors import APIError
from ..schemas.terraria import TerrariaServerCreateRequest, TerrariaServerActionResponse


async def new_server_controller(
    docker_client: DockerClient,
    request: TerrariaServerCreateRequest,
    config_path: str,
) -> TerrariaServerActionResponse:
    """
    Create a new Terraria server container.
    
    Args:
        docker_client: Docker SDK client
        request: TerrariaServerCreateRequest with server configuration
        config_path: Base path on host for storing server configs (e.g., /opt/pylon/servers/)
    
    Returns:
        TerrariaServerActionResponse with creation result
    
    Raises:
        APIError: If Docker operation fails
    """
    try:
        # Auto-generate server name if not provided
        server_name = request.server_name
        if not server_name:
            server_name = _generate_server_name(docker_client)
        
        # Build host config directory path
        host_config_dir = os.path.join(config_path, server_name)
        
        # Create config directory structure on host
        _create_config_directories(host_config_dir)
        
        # Select Docker image based on server type
        if request.server_type == "vanilla":
            docker_image = "passivelemon/terraria-docker:terraria-latest"
        else:  # modded
            docker_image = "passivelemon/terraria-docker:tmodloader-latest"
        
        # Build environment variables
        env_vars = {
            "WORLDNAME": request.worldname,
            "MAXPLAYERS": str(request.maxplayers),
            "DIFFICULTY": str(request.difficulty),
            "PORT": str(request.port),
        }
        
        # Add password only if provided
        if request.password:
            env_vars["PASSWORD"] = request.password
        
        # Create the Docker container
        container = docker_client.containers.run(
            image=docker_image,
            name=server_name,
            ports={f"{request.port}/tcp": request.port},
            volumes={host_config_dir: {"bind": "/opt/terraria/config/", "mode": "rw"}},
            environment=env_vars,
            detach=True,
            remove=False,
        )
        
        return TerrariaServerActionResponse(
            success=True,
            message=f"Terraria {request.server_type} server '{server_name}' created successfully",
            data={
                "container_id": container.short_id,
                "server_name": server_name,
                "server_type": request.server_type,
                "port": request.port,
                "status": "created",
            },
        )
    
    except APIError as e:
        # Return detailed Docker error for debugging
        error_msg = str(e)
        return TerrariaServerActionResponse(
            success=False,
            message=f"Failed to create Terraria server",
            error=error_msg,
        )
    except Exception as e:
        # Catch any other unexpected errors
        return TerrariaServerActionResponse(
            success=False,
            message=f"Failed to create Terraria server",
            error=str(e),
        )


def _generate_server_name(docker_client: DockerClient) -> str:
    """
    Auto-generate a unique server name based on existing containers.
    
    Args:
        docker_client: Docker SDK client
    
    Returns:
        Generated server name like 'terraria-1', 'terraria-2', etc.
    """
    # Get all containers (running and stopped) with names starting with 'terraria-'
    try:
        containers = docker_client.containers.list(all=True)
        terraria_containers = [
            c.name for c in containers 
            if c.name.startswith("terraria-")
        ]
        
        if not terraria_containers:
            return "terraria-1"
        
        # Extract numbers from names like 'terraria-1', 'terraria-2', etc.
        numbers = []
        for name in terraria_containers:
            try:
                num = int(name.split("-")[-1])
                numbers.append(num)
            except ValueError:
                continue
        
        # Find next available number
        next_num = max(numbers) + 1 if numbers else 1
        return f"terraria-{next_num}"
    
    except Exception:
        # Fallback if we can't query containers
        return "terraria-1"


def _create_config_directories(host_config_dir: str) -> None:
    """
    Create the directory structure needed for a Terraria server.
    
    Args:
        host_config_dir: Full path to the server's config directory
    
    Raises:
        OSError: If directory creation fails
    """
    config_path = Path(host_config_dir)
    
    # Create base directory
    config_path.mkdir(parents=True, exist_ok=True)
    
    # Create required subdirectories
    (config_path / "Worlds").mkdir(exist_ok=True)
    (config_path / "Logs").mkdir(exist_ok=True)
