from pydantic import BaseModel
from enum import Enum

class InventorySchema(BaseModel):
    name: str
    description: str | None
    price: float
    sku: str
    quantity: int

class InventoryDeleteSchema(BaseModel):
    sku: str


class Roles(Enum):
    ADMIN = "admin"
    INVENTORY_MANAGER = "inventory_manager"
    VIEWER = "viewer"

FIELD_PERMISSIONS = {
    Roles.ADMIN: {"*"},
    Roles.INVENTORY_MANAGER: {"quantity", "price", "sku", "name", "category"},
    Roles.VIEWER: {}
}
