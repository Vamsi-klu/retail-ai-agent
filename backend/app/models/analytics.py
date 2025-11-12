"""Analytics-related database models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class PriceHistory(BaseModel):
    """Price history tracking model."""

    __tablename__ = "price_history"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Price changes
    old_cost_price = Column(Float, nullable=True)
    new_cost_price = Column(Float, nullable=True)
    old_selling_price = Column(Float, nullable=False)
    new_selling_price = Column(Float, nullable=False)

    # Reason and metadata
    change_reason = Column(String(200), nullable=True)
    changed_by = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    product = relationship("Product", back_populates="price_history")


class AIPrediction(BaseModel):
    """AI prediction tracking model."""

    __tablename__ = "ai_predictions"

    # Prediction details
    prediction_type = Column(String(50), nullable=False, index=True)  # demand, churn, pricing, etc.
    entity_type = Column(String(50), nullable=False)  # product, customer, order
    entity_id = Column(Integer, nullable=False)

    # Prediction data
    prediction_data = Column(JSON, nullable=False)  # Actual prediction results
    confidence = Column(Float, nullable=True)  # Confidence score 0.0 to 1.0
    accuracy = Column(Float, nullable=True)  # Actual accuracy after verification

    # Model information
    model_name = Column(String(100), nullable=True)
    model_version = Column(String(50), nullable=True)

    # Status
    is_verified = Column(String(20), default="pending")  # pending, verified, incorrect
    notes = Column(Text, nullable=True)
