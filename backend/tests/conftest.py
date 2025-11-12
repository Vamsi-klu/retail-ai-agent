"""
Pytest configuration and fixtures.
"""
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient
from app.core.database import Base, get_db
from app.main import app
from app.core.config import settings
from app.core.security import create_access_token

# Import all models to ensure they're registered with SQLAlchemy
from app.models import (
    Product, Category, Supplier,
    Customer, CustomerSegment,
    Order, OrderItem,
    InventoryMovement,
    PriceHistory, AIPrediction,
    User
)

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for each test.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Cleanup
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async HTTP client for testing API endpoints.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers() -> dict:
    """
    Create authentication headers for testing protected endpoints.
    """
    token = create_access_token(data={"sub": "1", "username": "testuser"})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_product_data() -> dict:
    """Sample product data for testing."""
    return {
        "sku": "TEST-001",
        "name": "Test Product",
        "description": "A test product",
        "cost_price": 50.0,
        "selling_price": 75.0,
        "current_stock": 100,
        "reorder_point": 20,
        "reorder_quantity": 50,
    }


@pytest.fixture
def sample_customer_data() -> dict:
    """Sample customer data for testing."""
    return {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "123-456-7890",
        "address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "zip_code": "12345",
    }


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "email": "user@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPassword123",
    }
