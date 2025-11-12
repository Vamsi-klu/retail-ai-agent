"""
Integration tests for Products API.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_product_api(
    client: AsyncClient,
    auth_headers: dict,
    sample_product_data: dict
):
    """Test creating a product via API."""
    response = await client.post(
        "/api/v1/products/",
        json=sample_product_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == sample_product_data["sku"]
    assert data["name"] == sample_product_data["name"]
    assert "id" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_products_api(client: AsyncClient):
    """Test getting products list via API."""
    response = await client.get("/api/v1/products/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_product_by_id_api(
    client: AsyncClient,
    auth_headers: dict,
    sample_product_data: dict
):
    """Test getting a product by ID via API."""
    # Create product first
    create_response = await client.post(
        "/api/v1/products/",
        json=sample_product_data,
        headers=auth_headers
    )
    product_id = create_response.json()["id"]

    # Get product
    response = await client.get(f"/api/v1/products/{product_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_product_api(
    client: AsyncClient,
    auth_headers: dict,
    sample_product_data: dict
):
    """Test updating a product via API."""
    # Create product first
    create_response = await client.post(
        "/api/v1/products/",
        json=sample_product_data,
        headers=auth_headers
    )
    product_id = create_response.json()["id"]

    # Update product
    update_data = {"name": "Updated Product", "selling_price": 85.0}
    response = await client.put(
        f"/api/v1/products/{product_id}",
        json=update_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["selling_price"] == 85.0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_product_api(
    client: AsyncClient,
    auth_headers: dict,
    sample_product_data: dict
):
    """Test deleting a product via API."""
    # Create product first
    create_response = await client.post(
        "/api/v1/products/",
        json=sample_product_data,
        headers=auth_headers
    )
    product_id = create_response.json()["id"]

    # Delete product
    response = await client.delete(
        f"/api/v1/products/{product_id}",
        headers=auth_headers
    )

    assert response.status_code == 204


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_product_stock_api(
    client: AsyncClient,
    auth_headers: dict,
    sample_product_data: dict
):
    """Test updating product stock via API."""
    # Create product first
    create_response = await client.post(
        "/api/v1/products/",
        json=sample_product_data,
        headers=auth_headers
    )
    product_id = create_response.json()["id"]

    # Update stock
    response = await client.patch(
        f"/api/v1/products/{product_id}/stock",
        params={"quantity_change": -10},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["new_stock"] == 90
