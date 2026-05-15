"""Pydantic models for Terraria server management."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal


class TerrariaServerCreateRequest(BaseModel):
    """Request model for creating a Terraria server."""
    
    server_type: Literal["vanilla", "modded"]
    """Type of Terraria server: vanilla or tModLoader modded"""
    
    server_name: Optional[str] = None
    """Custom server name. If not provided, will be auto-generated (e.g., terraria-1)"""
    
    worldname: str = "World"
    """Name of the world file to use. Default: World"""
    
    maxplayers: int = Field(default=8, ge=1, le=255)
    """Maximum number of players. Must be between 1 and 255. Default: 8"""
    
    password: Optional[str] = None
    """Optional password required to join the server"""
    
    difficulty: int = Field(default=0, ge=0, le=3)
    """World difficulty level: 0=Normal, 1=Expert, 2=Master, 3=Journey. Default: 0"""
    
    port: int = Field(default=7777, ge=1024, le=65535)
    """Server port to expose. Must be between 1024 and 65535. Default: 7777"""


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
