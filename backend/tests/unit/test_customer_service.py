"""
Unit tests for Customer Service.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.customer_service import CustomerService
from app.schemas.customer import CustomerCreate, CustomerUpdate
from fastapi import HTTPException


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_customer(db_session: AsyncSession, sample_customer_data: dict):
    """Test creating a customer."""
    customer_data = CustomerCreate(**sample_customer_data)
    customer = await CustomerService.create_customer(db_session, customer_data)

    assert customer.id is not None
    assert customer.email == sample_customer_data["email"]
    assert customer.first_name == sample_customer_data["first_name"]
    assert customer.loyalty_tier == "Bronze"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_duplicate_customer(db_session: AsyncSession, sample_customer_data: dict):
    """Test creating a customer with duplicate email raises error."""
    customer_data = CustomerCreate(**sample_customer_data)
    await CustomerService.create_customer(db_session, customer_data)

    with pytest.raises(HTTPException) as exc_info:
        await CustomerService.create_customer(db_session, customer_data)

    assert exc_info.value.status_code == 400


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_customer(db_session: AsyncSession, sample_customer_data: dict):
    """Test getting a customer by ID."""
    customer_data = CustomerCreate(**sample_customer_data)
    created_customer = await CustomerService.create_customer(db_session, customer_data)

    customer = await CustomerService.get_customer(db_session, created_customer.id)

    assert customer is not None
    assert customer.id == created_customer.id


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_customer_by_email(db_session: AsyncSession, sample_customer_data: dict):
    """Test getting a customer by email."""
    customer_data = CustomerCreate(**sample_customer_data)
    await CustomerService.create_customer(db_session, customer_data)

    customer = await CustomerService.get_customer_by_email(
        db_session, sample_customer_data["email"]
    )

    assert customer is not None
    assert customer.email == sample_customer_data["email"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_customer(db_session: AsyncSession, sample_customer_data: dict):
    """Test updating a customer."""
    customer_data = CustomerCreate(**sample_customer_data)
    created_customer = await CustomerService.create_customer(db_session, customer_data)

    update_data = CustomerUpdate(first_name="Jane", phone="999-999-9999")
    updated_customer = await CustomerService.update_customer(
        db_session, created_customer.id, update_data
    )

    assert updated_customer is not None
    assert updated_customer.first_name == "Jane"
    assert updated_customer.phone == "999-999-9999"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_calculate_rfm_scores(db_session: AsyncSession, sample_customer_data: dict):
    """Test calculating RFM scores for a customer."""
    customer_data = CustomerCreate(**sample_customer_data)
    created_customer = await CustomerService.create_customer(db_session, customer_data)

    # Update customer metrics
    created_customer.total_orders = 10
    created_customer.total_purchases = 5000
    await db_session.commit()

    customer = await CustomerService.calculate_rfm_scores(db_session, created_customer.id)

    assert customer is not None
    assert customer.rfm_score > 0
    assert customer.loyalty_tier in ["Bronze", "Silver", "Gold", "Platinum"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_customer_metrics(db_session: AsyncSession, sample_customer_data: dict):
    """Test updating customer purchase metrics."""
    customer_data = CustomerCreate(**sample_customer_data)
    created_customer = await CustomerService.create_customer(db_session, customer_data)

    customer = await CustomerService.update_customer_metrics(
        db_session, created_customer.id, 150.0
    )

    assert customer is not None
    assert customer.total_purchases == 150.0
    assert customer.total_orders == 1
    assert customer.average_order_value == 150.0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_high_value_customers(db_session: AsyncSession):
    """Test getting high-value customers."""
    # Create customers with different lifetime values
    for i in range(3):
        customer_data = CustomerCreate(
            email=f"customer{i}@example.com",
            first_name=f"Customer{i}",
            last_name="Test"
        )
        customer = await CustomerService.create_customer(db_session, customer_data)
        customer.lifetime_value = (i + 1) * 1000
        await db_session.commit()

    high_value_customers = await CustomerService.get_high_value_customers(db_session)

    assert len(high_value_customers) == 3
    assert high_value_customers[0].lifetime_value >= high_value_customers[1].lifetime_value
