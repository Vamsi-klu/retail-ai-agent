"""Customer-related Pydantic schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class CustomerBase(BaseModel):
    """Base customer schema."""
    email: EmailStr
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: str = Field(default="USA", max_length=100)
    marketing_consent: bool = False


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer."""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    marketing_consent: Optional[bool] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response."""
    id: int
    total_purchases: float
    total_orders: int
    average_order_value: float
    last_purchase_date: Optional[datetime]
    frequency_score: float
    recency_score: float
    monetary_score: float
    rfm_score: float
    loyalty_tier: str
    loyalty_points: int
    churn_risk: float
    lifetime_value: float
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerSegmentResponse(BaseModel):
    """Schema for customer segment response."""
    id: int
    name: str
    description: Optional[str]
    customer_count: int
    created_at: datetime

    class Config:
        from_attributes = True
