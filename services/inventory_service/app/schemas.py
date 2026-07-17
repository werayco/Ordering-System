from pydantic import BaseModel

class InventorySchema(BaseModel):
    name: str
    description: str | None
    price: float
    sku: str
    quantity: int

class InventoryDeleteSchema(BaseModel):
    sku: str