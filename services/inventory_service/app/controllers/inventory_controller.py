from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import *
from sqlalchemy import select
from app.models.product import Inventory

class InventoryCRUD:
    @staticmethod
    async def add_inventory_item(db: AsyncSession, inventory: dict):
        try:
            record = Inventory(**inventory)
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return {"message": "Inventory item added successfully"}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def delete_inventory_item(db: AsyncSession, inventory_id: int):
        record = await db.get(Inventory, inventory_id)
        if not record:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        try:
            await db.delete(record)
            await db.commit()
            return {"message": "Inventory item deleted successfully"}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_inventory_item(db: AsyncSession, inventory: InventorySchema):
        record = await db.get(Inventory, inventory.sku)
        if not record:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        try:
            for key, value in inventory.model_dump().items():
                setattr(record, key, value)
            await db.commit()
            await db.refresh(record)
            return {"message": "Inventory item updated successfully"}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_inventory_item(db: AsyncSession, inventory_id: int):
        record = await db.get(Inventory, inventory_id)
        if not record:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        return record