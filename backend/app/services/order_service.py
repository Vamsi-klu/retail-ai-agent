"""Order service for business logic."""
from typing import List, Optional
from datetime import datetime
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from app.models.order import Order, OrderItem, OrderStatus
from app.models.inventory import InventoryMovement, MovementType
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate
from app.services.product_service import ProductService
from app.services.customer_service import CustomerService
from app.services.inventory_service import InventoryService
from fastapi import HTTPException, status


class OrderService:
    """Service for order-related business logic."""

    @staticmethod
    def generate_order_number() -> str:
        """
        Generate a unique order number.

        Returns:
            Order number string
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        random_suffix = secrets.token_hex(4).upper()
        return f"ORD-{timestamp}-{random_suffix}"

    @staticmethod
    async def create_order(
        db: AsyncSession, order_data: OrderCreate
    ) -> Order:
        """
        Create a new order with items.

        Args:
            db: Database session
            order_data: Order creation data

        Returns:
            Created order

        Raises:
            HTTPException: If customer not found or insufficient stock
        """
        # Verify customer exists
        customer = await CustomerService.get_customer(db, order_data.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {order_data.customer_id} not found"
            )

        # Create order
        order = Order(
            order_number=OrderService.generate_order_number(),
            customer_id=order_data.customer_id,
            payment_method=order_data.payment_method,
            shipping_address=order_data.shipping_address,
            notes=order_data.notes,
            subtotal=0,
            tax_amount=0,
            discount_amount=0,
            shipping_cost=0,
            total_amount=0,
        )

        # Process order items
        subtotal = 0
        order_items = []

        for item_data in order_data.items:
            # Get product
            product = await ProductService.get_product(db, item_data.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {item_data.product_id} not found"
                )

            # Check stock availability
            if product.current_stock < item_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product '{product.name}'. Available: {product.current_stock}, Requested: {item_data.quantity}"
                )

            # Calculate item total
            item_subtotal = item_data.unit_price * item_data.quantity
            item_discount = item_data.discount
            item_tax = item_data.tax
            item_total = item_subtotal - item_discount + item_tax

            # Create order item
            order_item = OrderItem(
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                discount=item_discount,
                tax=item_tax,
                total=item_total,
                product_name=product.name,
                product_sku=product.sku,
            )
            order_items.append(order_item)
            subtotal += item_subtotal

        # Calculate order totals
        order.subtotal = subtotal
        order.tax_amount = sum(item.tax for item in order_items)
        order.discount_amount = sum(item.discount for item in order_items)
        order.total_amount = subtotal - order.discount_amount + order.tax_amount + order.shipping_cost

        # Save order
        db.add(order)
        await db.flush()  # Get order ID

        # Add items to order
        for item in order_items:
            item.order_id = order.id
            db.add(item)

            # Update product stock
            await ProductService.update_stock(db, item.product_id, -item.quantity)

            # Record inventory movement
            await InventoryService.record_movement(
                db=db,
                product_id=item.product_id,
                movement_type=MovementType.SALE,
                quantity=-item.quantity,
                reference_id=order.id,
                reference_type="order",
                notes=f"Sale via order {order.order_number}"
            )

        # Update customer metrics
        await CustomerService.update_customer_metrics(
            db, order.customer_id, order.total_amount
        )

        await db.commit()
        await db.refresh(order)

        # Load items
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order.id)
        )
        return result.scalar_one()

    @staticmethod
    async def get_order(
        db: AsyncSession, order_id: int
    ) -> Optional[Order]:
        """
        Get an order by ID with items.

        Args:
            db: Database session
            order_id: Order ID

        Returns:
            Order if found, None otherwise
        """
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_order_by_number(
        db: AsyncSession, order_number: str
    ) -> Optional[Order]:
        """
        Get an order by order number.

        Args:
            db: Database session
            order_number: Order number

        Returns:
            Order if found, None otherwise
        """
        result = await db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_orders(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        customer_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
    ) -> List[Order]:
        """
        Get a list of orders with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            customer_id: Filter by customer ID
            status: Filter by order status

        Returns:
            List of orders
        """
        query = select(Order).options(selectinload(Order.items))

        filters = []
        if customer_id:
            filters.append(Order.customer_id == customer_id)
        if status:
            filters.append(Order.status == status)

        if filters:
            query = query.where(and_(*filters))

        query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_order_status(
        db: AsyncSession, order_id: int, order_data: OrderUpdate
    ) -> Optional[Order]:
        """
        Update an order's status and other fields.

        Args:
            db: Database session
            order_id: Order ID
            order_data: Order update data

        Returns:
            Updated order if found, None otherwise
        """
        order = await OrderService.get_order(db, order_id)
        if not order:
            return None

        update_data = order_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)

        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def cancel_order(
        db: AsyncSession, order_id: int
    ) -> Optional[Order]:
        """
        Cancel an order and restore stock.

        Args:
            db: Database session
            order_id: Order ID

        Returns:
            Cancelled order if found, None otherwise

        Raises:
            HTTPException: If order cannot be cancelled
        """
        order = await OrderService.get_order(db, order_id)
        if not order:
            return None

        if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel order with status '{order.status}'"
            )

        # Restore stock for each item
        for item in order.items:
            await ProductService.update_stock(db, item.product_id, item.quantity)

            # Record inventory movement
            await InventoryService.record_movement(
                db=db,
                product_id=item.product_id,
                movement_type=MovementType.RETURN,
                quantity=item.quantity,
                reference_id=order.id,
                reference_type="order_cancellation",
                notes=f"Order {order.order_number} cancelled"
            )

        order.status = OrderStatus.CANCELLED
        await db.commit()
        await db.refresh(order)
        return order

    @staticmethod
    async def get_total_orders_count(
        db: AsyncSession,
        customer_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
    ) -> int:
        """
        Get total count of orders.

        Args:
            db: Database session
            customer_id: Filter by customer ID
            status: Filter by order status

        Returns:
            Total count
        """
        query = select(func.count(Order.id))

        filters = []
        if customer_id:
            filters.append(Order.customer_id == customer_id)
        if status:
            filters.append(Order.status == status)

        if filters:
            query = query.where(and_(*filters))

        result = await db.execute(query)
        return result.scalar()

    @staticmethod
    async def get_total_revenue(
        db: AsyncSession,
        status: Optional[OrderStatus] = None,
    ) -> float:
        """
        Get total revenue from orders.

        Args:
            db: Database session
            status: Filter by order status

        Returns:
            Total revenue
        """
        query = select(func.sum(Order.total_amount))

        if status:
            query = query.where(Order.status == status)
        else:
            # Exclude cancelled orders by default
            query = query.where(Order.status != OrderStatus.CANCELLED)

        result = await db.execute(query)
        total = result.scalar()
        return total if total else 0.0
