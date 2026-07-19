from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (RefreshRequest,ChangePasswordRequest,LoginRequest,RegisterRequest,TokenResponse,UserResponse)
from app.db.session import get_db
from app.models.user import User
from app.utils import (get_current_user_dep,cache_refresh_tokens)
from services.auth_service.app.controllers.users_auth_controller import AuthController

user_router = APIRouter(prefix="/api/v1/auth/user", tags=["auth"])

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.register(payload, db)

@user_router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.login(payload, db, table=User)

@user_router.post("/refresh")
async def refresh(refresh_token:RefreshRequest, current_user: User = Depends(get_current_user_dep(User))):
    tokens = await cache_refresh_tokens(current_user.id,refresh_token,"user")
    return tokens

@user_router.get("/me")
async def me(current_user: User = Depends(get_current_user_dep(User))):
    return current_user

@user_router.post("/change-password")
async def change_password(payload: ChangePasswordRequest,current_user: User = Depends(get_current_user_dep(User)),db: AsyncSession = Depends(get_db),):
    return await AuthController.change_password(payload, current_user, db)