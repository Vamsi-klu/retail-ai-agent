"""Inventory-related database models."""
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class MovementType(str, enum.Enum):
    """Inventory movement type enumeration."""
    PURCHASE = "purchase"  # Stock in from supplier
    SALE = "sale"  # Stock out to customer
    RETURN = "return"  # Customer return
    ADJUSTMENT = "adjustment"  # Manual adjustment
    DAMAGE = "damage"  # Damaged goods
    TRANSFER = "transfer"  # Transfer between locations
    RESTOCK = "restock"  # Restock from warehouse


class InventoryMovement(BaseModel):
    """Inventory movement tracking model."""

    __tablename__ = "inventory_movements"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(SQLEnum(MovementType), nullable=False)

    # Quantity (positive for stock in, negative for stock out)
    quantity = Column(Integer, nullable=False)
    previous_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)

    # Reference
    reference_id = Column(Integer, nullable=True)  # Order ID, PO ID, etc.
    reference_type = Column(String(50), nullable=True)  # order, purchase_order, etc.

    # Metadata
    performed_by = Column(String(100), nullable=True)  # User who performed the action
    notes = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)  # Warehouse location

    # Relationships
    product = relationship("Product", back_populates="inventory_movements")
