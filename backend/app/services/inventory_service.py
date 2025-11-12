"""Inventory service for business logic."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from app.models.inventory import InventoryMovement, MovementType
from app.models.product import Product
from fastapi import HTTPException, status


class InventoryService:
    """Service for inventory-related business logic."""

    @staticmethod
    async def record_movement(
        db: AsyncSession,
        product_id: int,
        movement_type: MovementType,
        quantity: int,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = None,
        performed_by: Optional[str] = None,
        notes: Optional[str] = None,
        location: Optional[str] = None,
    ) -> InventoryMovement:
        """
        Record an inventory movement.

        Args:
            db: Database session
            product_id: Product ID
            movement_type: Type of movement
            quantity: Quantity change (positive or negative)
            reference_id: Reference ID (e.g., order ID)
            reference_type: Reference type (e.g., "order")
            performed_by: User who performed the action
            notes: Additional notes
            location: Warehouse location

        Returns:
            Created inventory movement

        Raises:
            HTTPException: If product not found
        """
        # Get current product stock
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )

        previous_stock = product.current_stock
        new_stock = previous_stock + quantity

        movement = InventoryMovement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            reference_id=reference_id,
            reference_type=reference_type,
            performed_by=performed_by,
            notes=notes,
            location=location,
        )

        db.add(movement)
        return movement

    @staticmethod
    async def get_movements(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50,
        product_id: Optional[int] = None,
        movement_type: Optional[MovementType] = None,
    ) -> List[InventoryMovement]:
        """
        Get inventory movements with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            product_id: Filter by product ID
            movement_type: Filter by movement type

        Returns:
            List of inventory movements
        """
        query = select(InventoryMovement).options(
            selectinload(InventoryMovement.product)
        )

        filters = []
        if product_id:
            filters.append(InventoryMovement.product_id == product_id)
        if movement_type:
            filters.append(InventoryMovement.movement_type == movement_type)

        if filters:
            query = query.where(and_(*filters))

        query = query.order_by(InventoryMovement.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_movement_by_id(
        db: AsyncSession, movement_id: int
    ) -> Optional[InventoryMovement]:
        """
        Get an inventory movement by ID.

        Args:
            db: Database session
            movement_id: Movement ID

        Returns:
            Inventory movement if found, None otherwise
        """
        result = await db.execute(
            select(InventoryMovement)
            .options(selectinload(InventoryMovement.product))
            .where(InventoryMovement.id == movement_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_product_movements(
        db: AsyncSession, product_id: int, limit: int = 100
    ) -> List[InventoryMovement]:
        """
        Get all movements for a specific product.

        Args:
            db: Database session
            product_id: Product ID
            limit: Maximum number of movements to return

        Returns:
            List of inventory movements
        """
        query = (
            select(InventoryMovement)
            .where(InventoryMovement.product_id == product_id)
            .order_by(InventoryMovement.created_at.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_total_movements_count(
        db: AsyncSession,
        product_id: Optional[int] = None,
        movement_type: Optional[MovementType] = None,
    ) -> int:
        """
        Get total count of inventory movements.

        Args:
            db: Database session
            product_id: Filter by product ID
            movement_type: Filter by movement type

        Returns:
            Total count
        """
        query = select(func.count(InventoryMovement.id))

        filters = []
        if product_id:
            filters.append(InventoryMovement.product_id == product_id)
        if movement_type:
            filters.append(InventoryMovement.movement_type == movement_type)

        if filters:
            query = query.where(and_(*filters))

        result = await db.execute(query)
        return result.scalar()
