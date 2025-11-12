"""Product-related Pydantic schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""
    pass


class CategoryResponse(CategoryBase):
    """Schema for category response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SupplierBase(BaseModel):
    """Base supplier schema."""
    name: str = Field(..., max_length=200)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=100)
    is_active: bool = True
    rating: float = Field(default=5.0, ge=0.0, le=5.0)


class SupplierCreate(SupplierBase):
    """Schema for creating a supplier."""
    pass


class SupplierResponse(SupplierBase):
    """Schema for supplier response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base product schema."""
    sku: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    cost_price: float = Field(..., gt=0)
    selling_price: float = Field(..., gt=0)
    discount_price: Optional[float] = Field(None, gt=0)
    current_stock: int = Field(default=0, ge=0)
    reorder_point: int = Field(default=10, ge=0)
    reorder_quantity: int = Field(default=50, ge=0)
    min_stock_level: int = Field(default=5, ge=0)
    max_stock_level: int = Field(default=1000, ge=0)
    barcode: Optional[str] = Field(None, max_length=100)
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    size: Optional[str] = Field(None, max_length=50)
    is_active: bool = True
    is_featured: bool = False
    is_on_sale: bool = False

    @validator('selling_price')
    def selling_price_must_be_greater_than_cost(cls, v, values):
        if 'cost_price' in values and v < values['cost_price']:
            raise ValueError('Selling price must be greater than or equal to cost price')
        return v


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    cost_price: Optional[float] = Field(None, gt=0)
    selling_price: Optional[float] = Field(None, gt=0)
    discount_price: Optional[float] = Field(None, gt=0)
    current_stock: Optional[int] = Field(None, ge=0)
    reorder_point: Optional[int] = Field(None, ge=0)
    reorder_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_on_sale: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    supplier: Optional[SupplierResponse] = None

    class Config:
        from_attributes = True
