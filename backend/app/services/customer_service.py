"""Customer service for business logic."""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from app.models.customer import Customer, CustomerSegment
from app.schemas.customer import CustomerCreate, CustomerUpdate
from fastapi import HTTPException, status


class CustomerService:
    """Service for customer-related business logic."""

    @staticmethod
    async def create_customer(
        db: AsyncSession, customer_data: CustomerCreate
    ) -> Customer:
        """
        Create a new customer.

        Args:
            db: Database session
            customer_data: Customer creation data

        Returns:
            Created customer

        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        result = await db.execute(
            select(Customer).where(Customer.email == customer_data.email)
        )
        existing_customer = result.scalar_one_or_none()
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with email '{customer_data.email}' already exists"
            )

        customer = Customer(**customer_data.model_dump())
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer

    @staticmethod
    async def get_customer(
        db: AsyncSession, customer_id: int
    ) -> Optional[Customer]:
        """
        Get a customer by ID.

        Args:
            db: Database session
            customer_id: Customer ID

        Returns:
            Customer if found, None otherwise
        """
        result = await db.execute(
            select(Customer).where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_customer_by_email(
        db: AsyncSession, email: str
    ) -> Optional[Customer]:
        """
        Get a customer by email.

        Args:
            db: Database session
            email: Customer email

        Returns:
            Customer if found, None otherwise
        """
        result = await db.execute(
            select(Customer).where(Customer.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_customers(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        loyalty_tier: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> List[Customer]:
        """
        Get a list of customers with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            loyalty_tier: Filter by loyalty tier
            is_active: Filter by active status
            search: Search term for name or email

        Returns:
            List of customers
        """
        query = select(Customer)

        # Apply filters
        filters = []
        if loyalty_tier:
            filters.append(Customer.loyalty_tier == loyalty_tier)
        if is_active is not None:
            filters.append(Customer.is_active == is_active)
        if search:
            filters.append(
                or_(
                    Customer.email.ilike(f"%{search}%"),
                    Customer.first_name.ilike(f"%{search}%"),
                    Customer.last_name.ilike(f"%{search}%")
                )
            )

        if filters:
            query = query.where(and_(*filters))

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_customer(
        db: AsyncSession, customer_id: int, customer_data: CustomerUpdate
    ) -> Optional[Customer]:
        """
        Update a customer.

        Args:
            db: Database session
            customer_id: Customer ID
            customer_data: Customer update data

        Returns:
            Updated customer if found, None otherwise
        """
        customer = await CustomerService.get_customer(db, customer_id)
        if not customer:
            return None

        update_data = customer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)

        await db.commit()
        await db.refresh(customer)
        return customer

    @staticmethod
    async def calculate_rfm_scores(
        db: AsyncSession, customer_id: int
    ) -> Optional[Customer]:
        """
        Calculate RFM (Recency, Frequency, Monetary) scores for a customer.

        Args:
            db: Database session
            customer_id: Customer ID

        Returns:
            Updated customer with RFM scores
        """
        customer = await CustomerService.get_customer(db, customer_id)
        if not customer:
            return None

        # Recency score (0-10): based on days since last purchase
        if customer.last_purchase_date:
            days_since_purchase = (datetime.utcnow() - customer.last_purchase_date).days
            customer.recency_score = max(0, 10 - (days_since_purchase / 30))
        else:
            customer.recency_score = 0

        # Frequency score (0-10): based on total orders
        customer.frequency_score = min(10, customer.total_orders / 5)

        # Monetary score (0-10): based on total purchases
        customer.monetary_score = min(10, customer.total_purchases / 1000)

        # Combined RFM score
        customer.rfm_score = (
            customer.recency_score + customer.frequency_score + customer.monetary_score
        ) / 3

        # Update loyalty tier based on RFM score
        if customer.rfm_score >= 8:
            customer.loyalty_tier = "Platinum"
        elif customer.rfm_score >= 6:
            customer.loyalty_tier = "Gold"
        elif customer.rfm_score >= 4:
            customer.loyalty_tier = "Silver"
        else:
            customer.loyalty_tier = "Bronze"

        await db.commit()
        await db.refresh(customer)
        return customer

    @staticmethod
    async def update_customer_metrics(
        db: AsyncSession, customer_id: int, order_total: float
    ) -> Optional[Customer]:
        """
        Update customer purchase metrics after an order.

        Args:
            db: Database session
            customer_id: Customer ID
            order_total: Total amount of the order

        Returns:
            Updated customer
        """
        customer = await CustomerService.get_customer(db, customer_id)
        if not customer:
            return None

        customer.total_purchases += order_total
        customer.total_orders += 1
        customer.average_order_value = customer.total_purchases / customer.total_orders
        customer.last_purchase_date = datetime.utcnow()

        # Recalculate RFM scores
        await CustomerService.calculate_rfm_scores(db, customer_id)

        return customer

    @staticmethod
    async def get_high_value_customers(
        db: AsyncSession, limit: int = 50
    ) -> List[Customer]:
        """
        Get high-value customers based on lifetime value.

        Args:
            db: Database session
            limit: Maximum number of customers to return

        Returns:
            List of high-value customers
        """
        query = (
            select(Customer)
            .where(Customer.is_active == True)
            .order_by(Customer.lifetime_value.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_at_risk_customers(
        db: AsyncSession, risk_threshold: float = 0.7, limit: int = 50
    ) -> List[Customer]:
        """
        Get customers at risk of churning.

        Args:
            db: Database session
            risk_threshold: Minimum churn risk threshold (0.0 to 1.0)
            limit: Maximum number of customers to return

        Returns:
            List of at-risk customers
        """
        query = (
            select(Customer)
            .where(
                and_(
                    Customer.is_active == True,
                    Customer.churn_risk >= risk_threshold
                )
            )
            .order_by(Customer.churn_risk.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_total_customers_count(
        db: AsyncSession,
        is_active: Optional[bool] = None,
    ) -> int:
        """
        Get total count of customers.

        Args:
            db: Database session
            is_active: Filter by active status

        Returns:
            Total count
        """
        query = select(func.count(Customer.id))

        if is_active is not None:
            query = query.where(Customer.is_active == is_active)

        result = await db.execute(query)
        return result.scalar()
