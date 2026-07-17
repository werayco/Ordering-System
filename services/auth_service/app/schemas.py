from typing import Optional
from uuid import UUID
from enum import Enum
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    name: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    
class RefreshRequest(BaseModel):
    refresh_token: str

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Roles(Enum):
    ADMIN = "admin"
    INVENTORY_MANAGER = "inventory_manager"
    VIEWER = "viewer"

FIELD_PERMISSIONS = {
    Roles.ADMIN: {"*"},
    Roles.INVENTORY_MANAGER: {"quantity", "price", "sku", "name", "category"},
    Roles.VIEWER: {}
}

class RegisterEmployee(BaseModel):
    email: str
    name: str
    role: Roles = "viewer"
    password: str

class RegisterAdmin(BaseModel):
    email: str
    name: str
    password: str

class RegisterEmployee(BaseModel):
    email: str
    name: str
    role: Roles = Roles.VIEWER
    password: str
