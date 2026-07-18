from select import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import *
from app.schemas import InventorySchema
from app.kafka.producer import kafka_manager
from app.models.product import Inventory

class InventoryCRUD:
    @staticmethod
    async def add_inventory_item(db: AsyncSession, inventory: InventorySchema):
        try:
            record = Inventory(**inventory.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            kafka_manager.produce(topic="inventory", key="inventory.created", value=inventory.model_dump())
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
            kafka_manager.produce(topic="inventory", key="inventory.deleted", value=inventory.model_dump())
            return {"message": "Inventory item deleted successfully"}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_inventory_item(db: AsyncSession, inventory: InventorySchema):
        record = db.execute(select(Inventory).where(Inventory.sku == inventory.sku)).scalar_one_or_none()
        if not record:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        try:
            for key, value in inventory.model_dump().items():
                setattr(record, key, value)
            await db.commit()
            await db.refresh(record)
            kafka_manager.produce(topic="inventory", key="inventory.updated", value=inventory.model_dump())
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