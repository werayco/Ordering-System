from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import InventorySchema, InventoryUpdateSchema
from app.controllers.inventory_controller import InventoryCRUD

router = APIRouter(prefix="/inventory",tags=["inventory"])

@router.post("/add")
async def add_inventory_item(db: AsyncSession = Depends(get_db)):
    return InventoryCRUD.add_inventory_item(db)

@router.get("/get")
async def get_inventory_item(db: AsyncSession = Depends(get_db), inventory_id: int = None):
    return InventoryCRUD.get_inventory_item(db, inventory_id)

@router.put("/update")
async def update_inventory_item(db: AsyncSession = Depends(get_db), inventory: InventorySchema = None):
    return InventoryCRUD.update_inventory_item(db, inventory)

@router.delete("/delete")
async def delete_inventory_item(db: AsyncSession = Depends(get_db)):
    return InventoryCRUD.delete_inventory_item(db)