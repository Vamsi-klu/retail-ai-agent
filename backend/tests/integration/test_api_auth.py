"""
Integration tests for Authentication API.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_user_api(client: AsyncClient, sample_user_data: dict):
    """Test user registration via API."""
    response = await client.post(
        "/api/v1/auth/register",
        json=sample_user_data
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["username"] == sample_user_data["username"]
    assert "id" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_user_api(client: AsyncClient, sample_user_data: dict):
    """Test user login via API."""
    # Register user first
    await client.post("/api/v1/auth/register", json=sample_user_data)

    # Login
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["password"]
    }
    response = await client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_current_user_api(client: AsyncClient, sample_user_data: dict):
    """Test getting current user info via API."""
    # Register user
    await client.post("/api/v1/auth/register", json=sample_user_data)

    # Login
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["password"]
    }
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    token = login_response.json()["access_token"]

    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 401
