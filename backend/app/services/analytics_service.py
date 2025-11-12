"""Analytics service for business intelligence and reporting."""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order, OrderItem, OrderStatus
from app.models.analytics import PriceHistory, AIPrediction


class AnalyticsService:
    """Service for analytics and reporting."""

    @staticmethod
    async def get_dashboard_metrics(
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Get key metrics for the dashboard.

        Args:
            db: Database session

        Returns:
            Dictionary containing dashboard metrics
        """
        # Total revenue (excluding cancelled orders)
        revenue_result = await db.execute(
            select(func.sum(Order.total_amount)).where(
                Order.status != OrderStatus.CANCELLED
            )
        )
        total_revenue = revenue_result.scalar() or 0.0

        # Total orders
        orders_result = await db.execute(select(func.count(Order.id)))
        total_orders = orders_result.scalar() or 0

        # Total customers
        customers_result = await db.execute(
            select(func.count(Customer.id)).where(Customer.is_active == True)
        )
        total_customers = customers_result.scalar() or 0

        # Total products
        products_result = await db.execute(
            select(func.count(Product.id)).where(Product.is_active == True)
        )
        total_products = products_result.scalar() or 0

        # Low stock products
        low_stock_result = await db.execute(
            select(func.count(Product.id)).where(
                and_(
                    Product.current_stock <= Product.reorder_point,
                    Product.is_active == True
                )
            )
        )
        low_stock_count = low_stock_result.scalar() or 0

        # Average order value
        avg_order_result = await db.execute(
            select(func.avg(Order.total_amount)).where(
                Order.status != OrderStatus.CANCELLED
            )
        )
        average_order_value = avg_order_result.scalar() or 0.0

        # Today's revenue
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_revenue_result = await db.execute(
            select(func.sum(Order.total_amount)).where(
                and_(
                    Order.created_at >= today_start,
                    Order.status != OrderStatus.CANCELLED
                )
            )
        )
        today_revenue = today_revenue_result.scalar() or 0.0

        # Today's orders
        today_orders_result = await db.execute(
            select(func.count(Order.id)).where(
                Order.created_at >= today_start
            )
        )
        today_orders = today_orders_result.scalar() or 0

        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "low_stock_products": low_stock_count,
            "average_order_value": round(average_order_value, 2),
            "today_revenue": round(today_revenue, 2),
            "today_orders": today_orders,
        }

    @staticmethod
    async def get_revenue_by_period(
        db: AsyncSession,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get revenue data grouped by day for the last N days.

        Args:
            db: Database session
            days: Number of days to include

        Returns:
            List of daily revenue data
        """
        start_date = datetime.utcnow() - timedelta(days=days)

        query = (
            select(
                func.date(Order.created_at).label("date"),
                func.sum(Order.total_amount).label("revenue"),
                func.count(Order.id).label("orders")
            )
            .where(
                and_(
                    Order.created_at >= start_date,
                    Order.status != OrderStatus.CANCELLED
                )
            )
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at))
        )

        result = await db.execute(query)
        rows = result.all()

        return [
            {
                "date": row.date.isoformat() if row.date else None,
                "revenue": float(row.revenue) if row.revenue else 0.0,
                "orders": row.orders
            }
            for row in rows
        ]

    @staticmethod
    async def get_top_selling_products(
        db: AsyncSession,
        limit: int = 10,
        days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get top-selling products by quantity or revenue.

        Args:
            db: Database session
            limit: Number of products to return
            days: Optional filter for last N days

        Returns:
            List of top-selling products
        """
        query = (
            select(
                Product.id,
                Product.name,
                Product.sku,
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.total).label("total_revenue"),
                func.count(OrderItem.id).label("order_count")
            )
            .join(OrderItem, OrderItem.product_id == Product.id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(Order.status != OrderStatus.CANCELLED)
        )

        if days:
            start_date = datetime.utcnow() - timedelta(days=days)
            query = query.where(Order.created_at >= start_date)

        query = (
            query
            .group_by(Product.id, Product.name, Product.sku)
            .order_by(desc(func.sum(OrderItem.total)))
            .limit(limit)
        )

        result = await db.execute(query)
        rows = result.all()

        return [
            {
                "product_id": row.id,
                "product_name": row.name,
                "sku": row.sku,
                "total_quantity": row.total_quantity,
                "total_revenue": float(row.total_revenue) if row.total_revenue else 0.0,
                "order_count": row.order_count
            }
            for row in rows
        ]

    @staticmethod
    async def get_customer_segments_distribution(
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Get distribution of customers by loyalty tier.

        Args:
            db: Database session

        Returns:
            List of customer segments with counts
        """
        query = (
            select(
                Customer.loyalty_tier,
                func.count(Customer.id).label("count"),
                func.avg(Customer.total_purchases).label("avg_purchases"),
                func.avg(Customer.churn_risk).label("avg_churn_risk")
            )
            .where(Customer.is_active == True)
            .group_by(Customer.loyalty_tier)
            .order_by(Customer.loyalty_tier)
        )

        result = await db.execute(query)
        rows = result.all()

        return [
            {
                "tier": row.loyalty_tier,
                "count": row.count,
                "avg_purchases": float(row.avg_purchases) if row.avg_purchases else 0.0,
                "avg_churn_risk": float(row.avg_churn_risk) if row.avg_churn_risk else 0.0
            }
            for row in rows
        ]

    @staticmethod
    async def get_order_status_distribution(
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Get distribution of orders by status.

        Args:
            db: Database session

        Returns:
            List of order statuses with counts
        """
        query = (
            select(
                Order.status,
                func.count(Order.id).label("count"),
                func.sum(Order.total_amount).label("total_amount")
            )
            .group_by(Order.status)
            .order_by(Order.status)
        )

        result = await db.execute(query)
        rows = result.all()

        return [
            {
                "status": row.status.value,
                "count": row.count,
                "total_amount": float(row.total_amount) if row.total_amount else 0.0
            }
            for row in rows
        ]

    @staticmethod
    async def get_inventory_alerts(
        db: AsyncSession
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get inventory alerts (low stock, out of stock, overstock).

        Args:
            db: Database session

        Returns:
            Dictionary with different types of alerts
        """
        # Out of stock
        out_of_stock_query = (
            select(Product)
            .where(
                and_(
                    Product.current_stock == 0,
                    Product.is_active == True
                )
            )
            .limit(50)
        )
        out_of_stock_result = await db.execute(out_of_stock_query)
        out_of_stock = out_of_stock_result.scalars().all()

        # Low stock
        low_stock_query = (
            select(Product)
            .where(
                and_(
                    Product.current_stock > 0,
                    Product.current_stock <= Product.reorder_point,
                    Product.is_active == True
                )
            )
            .limit(50)
        )
        low_stock_result = await db.execute(low_stock_query)
        low_stock = low_stock_result.scalars().all()

        # Overstock
        overstock_query = (
            select(Product)
            .where(
                and_(
                    Product.current_stock >= Product.max_stock_level,
                    Product.is_active == True
                )
            )
            .limit(50)
        )
        overstock_result = await db.execute(overstock_query)
        overstock = overstock_result.scalars().all()

        return {
            "out_of_stock": [
                {
                    "id": p.id,
                    "name": p.name,
                    "sku": p.sku,
                    "current_stock": p.current_stock,
                    "reorder_point": p.reorder_point
                }
                for p in out_of_stock
            ],
            "low_stock": [
                {
                    "id": p.id,
                    "name": p.name,
                    "sku": p.sku,
                    "current_stock": p.current_stock,
                    "reorder_point": p.reorder_point
                }
                for p in low_stock
            ],
            "overstock": [
                {
                    "id": p.id,
                    "name": p.name,
                    "sku": p.sku,
                    "current_stock": p.current_stock,
                    "max_stock_level": p.max_stock_level
                }
                for p in overstock
            ]
        }

    @staticmethod
    async def record_price_change(
        db: AsyncSession,
        product_id: int,
        old_selling_price: float,
        new_selling_price: float,
        old_cost_price: Optional[float] = None,
        new_cost_price: Optional[float] = None,
        change_reason: Optional[str] = None,
        changed_by: Optional[str] = None,
    ) -> PriceHistory:
        """
        Record a price change in history.

        Args:
            db: Database session
            product_id: Product ID
            old_selling_price: Old selling price
            new_selling_price: New selling price
            old_cost_price: Old cost price
            new_cost_price: New cost price
            change_reason: Reason for price change
            changed_by: User who made the change

        Returns:
            Created price history record
        """
        price_history = PriceHistory(
            product_id=product_id,
            old_cost_price=old_cost_price,
            new_cost_price=new_cost_price,
            old_selling_price=old_selling_price,
            new_selling_price=new_selling_price,
            change_reason=change_reason,
            changed_by=changed_by
        )

        db.add(price_history)
        await db.commit()
        await db.refresh(price_history)
        return price_history
