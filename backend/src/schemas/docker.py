"""Pydantic models for Docker container management responses."""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class ContainerInfo(BaseModel):
    """Container information model."""
    
    id: str
    name: str
    status: str
    image: str


class ContainerListResponse(BaseModel):
    """Response model for listing containers."""
    
    success: bool
    data: Dict[str, Any]


class ContainerStatusResponse(BaseModel):
    """Response model for getting container status."""
    
    success: bool
    data: Dict[str, Any]


class ContainerActionResponse(BaseModel):
    """Response model for container start/stop operations."""
    
    success: bool
    data: Dict[str, str]
