"""Analytics API endpoints."""
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get key metrics for the dashboard."""
    return await AnalyticsService.get_dashboard_metrics(db)


@router.get("/revenue", response_model=List[Dict[str, Any]])
async def get_revenue_by_period(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get revenue data grouped by day for the last N days."""
    return await AnalyticsService.get_revenue_by_period(db, days)


@router.get("/top-products", response_model=List[Dict[str, Any]])
async def get_top_selling_products(
    limit: int = Query(10, ge=1, le=100),
    days: Optional[int] = Query(None, ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get top-selling products by revenue."""
    return await AnalyticsService.get_top_selling_products(db, limit, days)


@router.get("/customer-segments", response_model=List[Dict[str, Any]])
async def get_customer_segments_distribution(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get distribution of customers by loyalty tier."""
    return await AnalyticsService.get_customer_segments_distribution(db)


@router.get("/order-status", response_model=List[Dict[str, Any]])
async def get_order_status_distribution(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get distribution of orders by status."""
    return await AnalyticsService.get_order_status_distribution(db)


@router.get("/inventory-alerts", response_model=Dict[str, List[Dict[str, Any]]])
async def get_inventory_alerts(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get inventory alerts (low stock, out of stock, overstock)."""
    return await AnalyticsService.get_inventory_alerts(db)
