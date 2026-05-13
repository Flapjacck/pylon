"""Pydantic models for Terraria server management."""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class TerrariaServerCreateRequest(BaseModel):
    """Request model for creating a Terraria server."""
    
    server_name: str
    world_size: str  # "small", "medium", "large"
    difficulty: str  # "normal", "expert", "master"
    port: int


class TerrariaServerConfigRequest(BaseModel):
    """Request model for updating server configuration."""
    
    difficulty: Optional[str] = None
    max_players: Optional[int] = None
    mode: Optional[str] = None


class TerrariaServerInfo(BaseModel):
    """Information about a Terraria server."""
    
    server_name: str
    port: int
    status: str
    world_size: str
    difficulty: str
    player_count: int
    max_players: int


class TerrariaServerStatusResponse(BaseModel):
    """Response model for server status."""
    
    success: bool
    data: Optional[TerrariaServerInfo] = None
    error: Optional[str] = None


class TerrariaServerListResponse(BaseModel):
    """Response model for listing servers."""
    
    success: bool
    data: List[TerrariaServerInfo]
    count: int


class TerrariaServerActionResponse(BaseModel):
    """Response model for server actions (create, delete, start, stop)."""
    
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
