"""Order-related Pydantic schemas."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.order import OrderStatus, PaymentMethod


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    discount: float = Field(default=0.0, ge=0)
    tax: float = Field(default=0.0, ge=0)


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item."""
    pass


class OrderItemResponse(OrderItemBase):
    """Schema for order item response."""
    id: int
    order_id: int
    total: float
    product_name: str
    product_sku: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order schema."""
    customer_id: int
    payment_method: PaymentMethod = PaymentMethod.CASH
    shipping_address: Optional[str] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Schema for creating an order."""
    items: List[OrderItemCreate] = Field(..., min_items=1)


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: Optional[OrderStatus] = None
    payment_status: Optional[str] = None
    tracking_number: Optional[str] = None
    internal_notes: Optional[str] = None


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: int
    order_number: str
    customer_id: int
    subtotal: float
    tax_amount: float
    discount_amount: float
    shipping_cost: float
    total_amount: float
    status: OrderStatus
    payment_method: PaymentMethod
    payment_status: str
    shipping_address: Optional[str]
    tracking_number: Optional[str]
    notes: Optional[str]
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
