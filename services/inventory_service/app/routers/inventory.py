from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.controllers.inventory_controller import InventoryCRUD

router = APIRouter(prefix="/inventory",tags=["inventory"])

@router.post("/add")
async def add_inventory_item(db: AsyncSession = Depends(get_db)):
    return {"message": "Inventory item added successfully"}

@router.post("/delete")
async def delete_inventory_item(db: AsyncSession = Depends(get_db)):
    return {"message": "Inventory item deleted successfully"}

@router.post("/update")
async def update_inventory_item(db: AsyncSession = Depends(get_db)):
    return {"message": "Inventory item updated successfully"}

@router.post("/get")
async def get_inventory_item(db: AsyncSession = Depends(get_db)):
    return {"message": "Inventory item retrieved successfully"}