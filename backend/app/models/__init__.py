"""Database models for Retail AI Pro."""
from app.models.base import BaseModel
from app.models.product import Product, Category, Supplier
from app.models.customer import Customer, CustomerSegment
from app.models.order import Order, OrderItem
from app.models.inventory import InventoryMovement
from app.models.analytics import PriceHistory, AIPrediction
from app.models.user import User

__all__ = [
    "BaseModel",
    "Product",
    "Category",
    "Supplier",
    "Customer",
    "CustomerSegment",
    "Order",
    "OrderItem",
    "InventoryMovement",
    "PriceHistory",
    "AIPrediction",
    "User",
]
