"""
Unit tests for Product Service.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product
from fastapi import HTTPException


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_product(db_session: AsyncSession, sample_product_data: dict):
    """Test creating a product."""
    product_data = ProductCreate(**sample_product_data)
    product = await ProductService.create_product(db_session, product_data)

    assert product.id is not None
    assert product.sku == sample_product_data["sku"]
    assert product.name == sample_product_data["name"]
    assert product.current_stock == sample_product_data["current_stock"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_duplicate_product(db_session: AsyncSession, sample_product_data: dict):
    """Test creating a product with duplicate SKU raises error."""
    product_data = ProductCreate(**sample_product_data)
    await ProductService.create_product(db_session, product_data)

    with pytest.raises(HTTPException) as exc_info:
        await ProductService.create_product(db_session, product_data)

    assert exc_info.value.status_code == 400


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product(db_session: AsyncSession, sample_product_data: dict):
    """Test getting a product by ID."""
    product_data = ProductCreate(**sample_product_data)
    created_product = await ProductService.create_product(db_session, product_data)

    product = await ProductService.get_product(db_session, created_product.id)

    assert product is not None
    assert product.id == created_product.id
    assert product.sku == sample_product_data["sku"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_product_by_sku(db_session: AsyncSession, sample_product_data: dict):
    """Test getting a product by SKU."""
    product_data = ProductCreate(**sample_product_data)
    await ProductService.create_product(db_session, product_data)

    product = await ProductService.get_product_by_sku(db_session, sample_product_data["sku"])

    assert product is not None
    assert product.sku == sample_product_data["sku"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_products(db_session: AsyncSession):
    """Test getting a list of products."""
    # Create multiple products
    for i in range(5):
        product_data = ProductCreate(
            sku=f"TEST-{i:03d}",
            name=f"Test Product {i}",
            cost_price=50.0,
            selling_price=75.0,
            current_stock=100
        )
        await ProductService.create_product(db_session, product_data)

    products = await ProductService.get_products(db_session, skip=0, limit=10)

    assert len(products) == 5


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_product(db_session: AsyncSession, sample_product_data: dict):
    """Test updating a product."""
    product_data = ProductCreate(**sample_product_data)
    created_product = await ProductService.create_product(db_session, product_data)

    update_data = ProductUpdate(name="Updated Product", selling_price=80.0)
    updated_product = await ProductService.update_product(
        db_session, created_product.id, update_data
    )

    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.selling_price == 80.0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_product(db_session: AsyncSession, sample_product_data: dict):
    """Test soft deleting a product."""
    product_data = ProductCreate(**sample_product_data)
    created_product = await ProductService.create_product(db_session, product_data)

    result = await ProductService.delete_product(db_session, created_product.id)

    assert result is True

    product = await ProductService.get_product(db_session, created_product.id)
    assert product.is_active is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_stock(db_session: AsyncSession, sample_product_data: dict):
    """Test updating product stock."""
    product_data = ProductCreate(**sample_product_data)
    created_product = await ProductService.create_product(db_session, product_data)

    updated_product = await ProductService.update_stock(db_session, created_product.id, -10)

    assert updated_product.current_stock == 90


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_stock_insufficient(db_session: AsyncSession, sample_product_data: dict):
    """Test updating stock with insufficient quantity raises error."""
    product_data = ProductCreate(**sample_product_data)
    created_product = await ProductService.create_product(db_session, product_data)

    with pytest.raises(HTTPException) as exc_info:
        await ProductService.update_stock(db_session, created_product.id, -200)

    assert exc_info.value.status_code == 400


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_low_stock_products(db_session: AsyncSession):
    """Test getting low stock products."""
    # Create products with different stock levels
    low_stock = ProductCreate(
        sku="LOW-001",
        name="Low Stock Product",
        cost_price=50.0,
        selling_price=75.0,
        current_stock=5,
        reorder_point=10
    )
    await ProductService.create_product(db_session, low_stock)

    normal_stock = ProductCreate(
        sku="NORMAL-001",
        name="Normal Stock Product",
        cost_price=50.0,
        selling_price=75.0,
        current_stock=100,
        reorder_point=10
    )
    await ProductService.create_product(db_session, normal_stock)

    low_stock_products = await ProductService.get_low_stock_products(db_session)

    assert len(low_stock_products) == 1
    assert low_stock_products[0].sku == "LOW-001"
