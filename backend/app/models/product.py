"""Product-related database models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Category(BaseModel):
    """Product category model."""

    __tablename__ = "categories"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    parent = relationship("Category", remote_side="Category.id", backref="subcategories")
    products = relationship("Product", back_populates="category")


class Supplier(BaseModel):
    """Supplier model."""

    __tablename__ = "suppliers"

    name = Column(String(200), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    contact_person = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=5.0)

    # Relationships
    products = relationship("Product", back_populates="supplier")


class Product(BaseModel):
    """Product model."""

    __tablename__ = "products"

    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)

    # Pricing
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)

    # Inventory
    current_stock = Column(Integer, default=0)
    reorder_point = Column(Integer, default=10)
    reorder_quantity = Column(Integer, default=50)
    min_stock_level = Column(Integer, default=5)
    max_stock_level = Column(Integer, default=1000)

    # Product attributes
    barcode = Column(String(100), nullable=True, unique=True)
    weight = Column(Float, nullable=True)  # in kg
    dimensions = Column(String(50), nullable=True)  # LxWxH in cm
    color = Column(String(50), nullable=True)
    size = Column(String(50), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_on_sale = Column(Boolean, default=False)

    # Relationships
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    inventory_movements = relationship("InventoryMovement", back_populates="product")
    price_history = relationship("PriceHistory", back_populates="product")
