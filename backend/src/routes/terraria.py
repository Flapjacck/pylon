"""Terraria server management routes.

This module provides endpoints for managing Terraria servers including
creating, listing, configuring, deleting, and monitoring Terraria game servers.

Routes delegate to modular controller functions that handle business logic
and error handling.
"""

from fastapi import APIRouter, Depends, HTTPException
from docker.errors import APIError
from docker import DockerClient

from ..schemas.terraria import (
    TerrariaServerListResponse,
    TerrariaServerStatusResponse,
    TerrariaServerCreateRequest,
    TerrariaServerConfigRequest,
    TerrariaServerActionResponse,
)
from ..controllers.terraria.newServer import new_server_controller
from ..controllers.terraria.listServers import list_servers_controller
from ..middleware.docker_client import get_docker_client_dependency
from ..config.settings import settings

router = APIRouter(
    prefix="/terraria",
    tags=["terraria"],
    responses={200: {"description": "Terraria operation successful"}},
)


@router.post("/servers", response_model=TerrariaServerActionResponse)
async def create_terraria_server(
    request: TerrariaServerCreateRequest,
    docker_client: DockerClient = Depends(get_docker_client_dependency),
) -> TerrariaServerActionResponse:
    """
    Create a new Terraria server.
    
    Args:
        request: TerrariaServerCreateRequest with server_type, server_name, worldname, maxplayers, password, difficulty, port
        docker_client: Docker SDK client (injected dependency)
    
    Returns:
        TerrariaServerActionResponse with creation result and server details
    """
    try:
        result = await new_server_controller(
            docker_client=docker_client,
            request=request,
            config_path=settings.terraria_config_path,
        )
        
        # If controller returned success=False, still return 200 but client should check success flag
        if not result.success:
            # Optionally could raise HTTPException here instead
            return result
        
        return result
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Terraria server: {str(e)}")


@router.get("/servers", response_model=TerrariaServerListResponse)
async def list_terraria_servers(
    docker_client: DockerClient = Depends(get_docker_client_dependency),
) -> TerrariaServerListResponse:
    """
    List all Terraria servers.
    
    Returns:
        TerrariaServerListResponse with list of all servers and count
    """
    try:
        result = await list_servers_controller(docker_client=docker_client)
        return result
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list Terraria servers: {str(e)}")


@router.get("/servers/{server_name}", response_model=TerrariaServerStatusResponse)
async def get_terraria_server_status(
    server_name: str,
) -> TerrariaServerStatusResponse:
    """
    Get the detailed status of a specific Terraria server.
    
    Args:
        server_name: The name of the server
    
    Returns:
        TerrariaServerStatusResponse with detailed server status
    
    TODO: Call get_terraria_server_status_controller(server_name)
    """
    try:
        # TODO: Call controller
        # result = await get_terraria_server_status_controller(server_name)
        # return result
        pass
    except APIError as e:
        raise
    except Exception as e:
        raise


@router.put("/servers/{server_name}/config", response_model=TerrariaServerActionResponse)
async def update_terraria_server_config(
    server_name: str,
    config: TerrariaServerConfigRequest,
) -> TerrariaServerActionResponse:
    """
    Update Terraria server configuration (difficulty, max players, etc).
    
    Args:
        server_name: The name of the server
        config: TerrariaServerConfigRequest with new configuration values
    
    Returns:
        TerrariaServerActionResponse with update result
    
    TODO: Call update_terraria_server_config_controller(server_name, config)
    """
    try:
        # TODO: Call controller
        # result = await update_terraria_server_config_controller(server_name, config)
        # return result
        pass
    except APIError as e:
        raise
    except Exception as e:
        raise


@router.delete("/servers/{server_name}", response_model=TerrariaServerActionResponse)
async def delete_terraria_server(
    server_name: str,
) -> TerrariaServerActionResponse:
    """
    Delete/destroy a Terraria server.
    
    Args:
        server_name: The name of the server to delete
    
    Returns:
        TerrariaServerActionResponse with deletion result
    
    TODO: Call delete_terraria_server_controller(server_name)
    """
    try:
        # TODO: Call controller
        # result = await delete_terraria_server_controller(server_name)
        # return result
        pass
    except APIError as e:
        raise
    except Exception as e:
        raise


@router.post("/servers/{server_name}/start", response_model=TerrariaServerActionResponse)
async def start_terraria_server(
    server_name: str,
) -> TerrariaServerActionResponse:
    """
    Start a Terraria server.
    
    Args:
        server_name: The name of the server to start
    
    Returns:
        TerrariaServerActionResponse with start operation result
    
    TODO: Call start_terraria_server_controller(server_name)
    """
    try:
        # TODO: Call controller
        # result = await start_terraria_server_controller(server_name)
        # return result
        pass
    except APIError as e:
        raise
    except Exception as e:
        raise


@router.post("/servers/{server_name}/stop", response_model=TerrariaServerActionResponse)
async def stop_terraria_server(
    server_name: str,
) -> TerrariaServerActionResponse:
    """
    Stop a Terraria server.
    
    Args:
        server_name: The name of the server to stop
    
    Returns:
        TerrariaServerActionResponse with stop operation result
    
    TODO: Call stop_terraria_server_controller(server_name)
    """
    try:
        # TODO: Call controller
        # result = await stop_terraria_server_controller(server_name)
        # return result
        pass
    except APIError as e:
        raise
    except Exception as e:
        raise
