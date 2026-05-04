"""Docker container management routes.

This module provides endpoints for managing Docker containers including
listing, starting, stopping, and checking status of containers.

Routes delegate to modular controller functions that handle business logic
and error handling.
"""

from fastapi import APIRouter, Depends
from docker.client import DockerClient
from docker.errors import APIError

from ..middleware.docker_client import get_docker_client_dependency
from ..controllers.docker import (
    list_containers_controller,
    get_container_status_controller,
    start_container_controller,
    stop_container_controller,
)
from ..schemas.docker import (
    ContainerListResponse,
    ContainerStatusResponse,
    ContainerActionResponse,
)

router = APIRouter(
    prefix="/docker",
    tags=["docker"],
    responses={200: {"description": "Docker operation successful"}},
)


@router.get("/containers", response_model=ContainerListResponse)
async def list_containers(
    docker_client: DockerClient = Depends(get_docker_client_dependency),
) -> ContainerListResponse:
    """
    List all Docker containers (running and stopped).
    
    Returns:
        ContainerListResponse with list of all containers and count
    """
    try:
        return await list_containers_controller(docker_client)
    except APIError as e:
        raise
    except Exception as e:
        raise


@router.get("/containers/{container_id}", response_model=ContainerStatusResponse)
async def get_container_status(
    container_id: str,
    docker_client: DockerClient = Depends(get_docker_client_dependency),
) -> ContainerStatusResponse:
    """
    Get the detailed status of a specific Docker container.
    
    Args:
        container_id: The ID or name of the container
    
    Returns:
        ContainerStatusResponse with detailed container status
    """
    return await get_container_status_controller(container_id, docker_client)


@router.post("/containers/{container_id}/start", response_model=ContainerActionResponse)
async def start_container(
    container_id: str,
    docker_client: DockerClient = Depends(get_docker_client_dependency),
) -> ContainerActionResponse:
    """
    Start a Docker container.
    
    Args:
        container_id: The ID or name of the container to start
    
    Returns:
        ContainerActionResponse with start operation result
    """
    return await start_container_controller(container_id, docker_client)


@router.post("/containers/{container_id}/stop", response_model=ContainerActionResponse)
async def stop_container(
    container_id: str,
    docker_client: DockerClient = Depends(get_docker_client_dependency),
) -> ContainerActionResponse:
    """
    Stop a Docker container.
    
    Args:
        container_id: The ID or name of the container to stop
    
    Returns:
        ContainerActionResponse with stop operation result
    """
    return await stop_container_controller(container_id, docker_client)
