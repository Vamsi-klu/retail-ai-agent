"""Product service for business logic."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from app.models.product import Product, Category, Supplier
from app.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException, status


class ProductService:
    """Service for product-related business logic."""

    @staticmethod
    async def create_product(
        db: AsyncSession, product_data: ProductCreate
    ) -> Product:
        """
        Create a new product.

        Args:
            db: Database session
            product_data: Product creation data

        Returns:
            Created product

        Raises:
            HTTPException: If SKU already exists
        """
        # Check if SKU already exists
        result = await db.execute(select(Product).where(Product.sku == product_data.sku))
        existing_product = result.scalar_one_or_none()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with SKU '{product_data.sku}' already exists"
            )

        product = Product(**product_data.model_dump())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_product(
        db: AsyncSession, product_id: int
    ) -> Optional[Product]:
        """
        Get a product by ID.

        Args:
            db: Database session
            product_id: Product ID

        Returns:
            Product if found, None otherwise
        """
        result = await db.execute(
            select(Product)
            .options(selectinload(Product.category), selectinload(Product.supplier))
            .where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_product_by_sku(
        db: AsyncSession, sku: str
    ) -> Optional[Product]:
        """
        Get a product by SKU.

        Args:
            db: Database session
            sku: Product SKU

        Returns:
            Product if found, None otherwise
        """
        result = await db.execute(
            select(Product)
            .options(selectinload(Product.category), selectinload(Product.supplier))
            .where(Product.sku == sku)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_products(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> List[Product]:
        """
        Get a list of products with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            category_id: Filter by category ID
            is_active: Filter by active status
            search: Search term for name or SKU

        Returns:
            List of products
        """
        query = select(Product).options(
            selectinload(Product.category),
            selectinload(Product.supplier)
        )

        # Apply filters
        filters = []
        if category_id is not None:
            filters.append(Product.category_id == category_id)
        if is_active is not None:
            filters.append(Product.is_active == is_active)
        if search:
            filters.append(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.sku.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%")
                )
            )

        if filters:
            query = query.where(and_(*filters))

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_product(
        db: AsyncSession, product_id: int, product_data: ProductUpdate
    ) -> Optional[Product]:
        """
        Update a product.

        Args:
            db: Database session
            product_id: Product ID
            product_data: Product update data

        Returns:
            Updated product if found, None otherwise
        """
        product = await ProductService.get_product(db, product_id)
        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete_product(
        db: AsyncSession, product_id: int
    ) -> bool:
        """
        Soft delete a product (set is_active to False).

        Args:
            db: Database session
            product_id: Product ID

        Returns:
            True if product was deleted, False if not found
        """
        product = await ProductService.get_product(db, product_id)
        if not product:
            return False

        product.is_active = False
        await db.commit()
        return True

    @staticmethod
    async def get_low_stock_products(
        db: AsyncSession, limit: int = 50
    ) -> List[Product]:
        """
        Get products with stock below reorder point.

        Args:
            db: Database session
            limit: Maximum number of products to return

        Returns:
            List of low-stock products
        """
        query = (
            select(Product)
            .where(
                and_(
                    Product.current_stock <= Product.reorder_point,
                    Product.is_active == True
                )
            )
            .order_by(Product.current_stock.asc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_stock(
        db: AsyncSession, product_id: int, quantity_change: int
    ) -> Optional[Product]:
        """
        Update product stock quantity.

        Args:
            db: Database session
            product_id: Product ID
            quantity_change: Quantity to add (positive) or subtract (negative)

        Returns:
            Updated product if found and valid, None otherwise

        Raises:
            HTTPException: If stock would become negative
        """
        product = await ProductService.get_product(db, product_id)
        if not product:
            return None

        new_stock = product.current_stock + quantity_change
        if new_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock quantity"
            )

        product.current_stock = new_stock
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_total_products_count(
        db: AsyncSession,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = None,
    ) -> int:
        """
        Get total count of products.

        Args:
            db: Database session
            category_id: Filter by category ID
            is_active: Filter by active status

        Returns:
            Total count
        """
        query = select(func.count(Product.id))

        filters = []
        if category_id is not None:
            filters.append(Product.category_id == category_id)
        if is_active is not None:
            filters.append(Product.is_active == is_active)

        if filters:
            query = query.where(and_(*filters))

        result = await db.execute(query)
        return result.scalar()
