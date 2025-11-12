"""Customer-related database models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class CustomerSegment(BaseModel):
    """Customer segment model for grouping customers."""

    __tablename__ = "customer_segments"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    criteria = Column(Text, nullable=True)  # JSON string of segmentation criteria
    is_active = Column(Boolean, default=True)

    # Relationships
    customers = relationship("Customer", back_populates="segment")


class Customer(BaseModel):
    """Customer model."""

    __tablename__ = "customers"

    # Personal Information
    email = Column(String(100), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)

    # Address
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True, default="USA")

    # Purchase Behavior
    total_purchases = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    average_order_value = Column(Float, default=0.0)
    last_purchase_date = Column(DateTime, nullable=True)

    # Customer Analytics
    frequency_score = Column(Float, default=0.0)  # How often they buy
    recency_score = Column(Float, default=0.0)  # How recently they bought
    monetary_score = Column(Float, default=0.0)  # How much they spend
    rfm_score = Column(Float, default=0.0)  # Combined RFM score

    # Loyalty & Risk
    loyalty_tier = Column(String(20), default="Bronze")  # Bronze, Silver, Gold, Platinum
    loyalty_points = Column(Integer, default=0)
    churn_risk = Column(Float, default=0.0)  # 0.0 to 1.0 probability
    lifetime_value = Column(Float, default=0.0)

    # Segmentation
    segment_id = Column(Integer, ForeignKey("customer_segments.id"), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)

    # Relationships
    segment = relationship("CustomerSegment", back_populates="customers")
    orders = relationship("Order", back_populates="customer")
