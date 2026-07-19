from pydantic import BaseModel
from enum import Enum
from typing import Union

class InventorySchema(BaseModel):
    name: Union[str,None]
    description: Union[str,None]
    price: Union[float,None]
    sku: Union[str,None]
    quantity: Union[int, None]

class InventorySchemaList(BaseModel):
    __root__: list[InventorySchema]

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
