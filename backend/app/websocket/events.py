"""
WebSocket event types for real-time updates.
"""
from enum import Enum


class WebSocketEventType(str, Enum):
    """WebSocket event type enumeration."""

    # Product events
    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"
    PRODUCT_LOW_STOCK = "product_low_stock"

    # Order events
    ORDER_CREATED = "order_created"
    ORDER_UPDATED = "order_updated"
    ORDER_CANCELLED = "order_cancelled"

    # Customer events
    CUSTOMER_CREATED = "customer_created"
    CUSTOMER_UPDATED = "customer_updated"
    CUSTOMER_AT_RISK = "customer_at_risk"

    # Inventory events
    INVENTORY_UPDATED = "inventory_updated"
    INVENTORY_ALERT = "inventory_alert"

    # Analytics events
    ANALYTICS_UPDATED = "analytics_updated"
    DASHBOARD_REFRESH = "dashboard_refresh"

    # System events
    NOTIFICATION = "notification"
    ALERT = "alert"
    ERROR = "error"
