"""Integration tests for Terraria server creation."""

import time
import pytest
from fastapi import FastAPI
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import create_app


@pytest.fixture
def app() -> FastAPI:
    """Create and return a FastAPI app instance for testing."""
    return create_app()


@pytest.fixture
def sync_client(app: FastAPI):
    """Create a synchronous test client."""
    from fastapi.testclient import TestClient
    return TestClient(app)


def test_create_and_verify_terraria_server(sync_client):
    """
    Test creating a Terraria server and verifying it reaches running state.
    
    This test:
    1. Creates a new vanilla Terraria server via POST /terraria/servers
    2. Verifies the creation response indicates success
    3. Polls GET /terraria/servers/{server_name} to verify server status
    4. Asserts the server reaches "running" state within 30 seconds
    5. Cleans up by stopping the server
    """
    
    # Step 1: Create a Terraria server
    server_create_payload = {
        "server_type": "vanilla",
        "server_name": f"test-server-{int(time.time() * 1000) % 1000000}",
        "worldname": "TestWorld",
        "maxplayers": 8,
        "password": None,
        "difficulty": 0,
        "port": 7778,  # Use non-default port to avoid conflicts
    }
    
    response = sync_client.post(
        "/terraria/servers",
        json=server_create_payload,
    )
    
    # Verify creation response
    assert response.status_code == 200, f"Failed to create server: {response.text}"
    
    response_data = response.json()
    assert "success" in response_data, f"Response missing 'success' field: {response_data}"
    assert response_data["success"] is True, f"Server creation failed: {response_data}"
    
    # Extract server details from data field
    data = response_data.get("data", {})
    server_name = data.get("server_name")
    container_id = data.get("container_id")
    
    assert server_name is not None, f"Response missing server_name in data: {response_data}"
    assert container_id is not None, f"Response missing container_id in data: {response_data}"
    
    print(f"\n✓ Server created: {server_name} (container: {container_id})")
    
    # Step 2: Poll for server status until it's running (up to 30 seconds)
    max_retries = 30
    retry_count = 0
    server_running = False
    last_status_response = None
    
    while retry_count < max_retries:
        try:
            status_response = sync_client.get(f"/terraria/servers/{server_name}")
            last_status_response = status_response
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                server_info = status_data.get("data", {})
                current_status = server_info.get("status") if server_info else None
                
                print(f"  [{retry_count + 1}/{max_retries}] Server status: {current_status}")
                
                if current_status == "running":
                    server_running = True
                    print(f"✓ Server reached running state")
                    break
            else:
                print(f"  Status check failed (HTTP {status_response.status_code}), retrying...")
        
        except Exception as e:
            print(f"  Status check error: {e}, retrying...")
        
        retry_count += 1
        if retry_count < max_retries:
            time.sleep(1)
    
    # Step 3: Assert server is running
    assert server_running, (
        f"Server {server_name} failed to reach 'running' state within "
        f"{max_retries} seconds. Last status: {last_status_response.json() if last_status_response else 'N/A'}"
    )
    
    print(f"✓ Test passed: Terraria server {server_name} created and verified running")
    
    # Cleanup: Stop the server
    try:
        stop_response = sync_client.post(f"/terraria/servers/{server_name}/stop")
        if stop_response.status_code == 200:
            print(f"✓ Server stopped successfully")
        else:
            print(f"⚠ Stop request failed (HTTP {stop_response.status_code})")
    except Exception as e:
        print(f"⚠ Cleanup failed: {e}")
