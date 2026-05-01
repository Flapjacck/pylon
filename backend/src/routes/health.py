"""Health check routes for API server status monitoring.

This module provides endpoints to verify the API server is running
and responsive. Health checks are critical for load balancers, 
monitoring systems, and frontend error handling.
"""

from fastapi import APIRouter
from datetime import datetime, timezone
from typing import Dict, Any

# Record server start time
START_TIME = datetime.now(timezone.utc)

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={200: {"description": "API is healthy"}},
)


@router.get("", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Check API server health statuuptime and timestamp info
            - status: "healthy" if server is operational
            - uptime_seconds: Server uptime in seconds
            - timestamp: ISO 8601 datetime of check
    
    Example response:
        {
            "status": "healthy",
            "uptime_seconds": 3600.5,
            "timestamp": "2026-04-30T10:15:30.123456"
        }
    """
    # Calculate uptime in seconds
    current_time = datetime.now(timezone.utc)
    uptime = (current_time - START_TIME).total_seconds()
    
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "timestamp": current_time
    }
