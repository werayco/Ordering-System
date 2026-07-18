from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import *
from app.db.session import get_db
from app.models.user import User
from app.utils import (get_current_user_dep, get_tokens)
from app.controllers.employee_controller import EmployeeController
from services.auth_service.app.controllers.users_auth_controller import AuthController
from services.auth_service.app.schemas import *

router = APIRouter(prefix="/api/v1/employee", tags=["auth"])

@router.post("/create-admin", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterAdmin, db: AsyncSession = Depends(get_db)):
    return await EmployeeController.register_admin(payload, db)

@router.post("/create-employee", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterEmployee, db: AsyncSession = Depends(get_db)):
    return await EmployeeController.register_employee(payload, db)

@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthController.login(payload, db)

@router.post("/refresh")
async def refresh(current_user: User = Depends(get_current_user_dep(User))):
    access_token, refresh_token = await get_tokens(current_user)
    return AccessTokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me")
async def me(current_user: User = Depends(get_current_user_dep(User))):
    return current_user

@router.post("/change-password")
async def change_password(payload: ChangePasswordRequest,current_user = Depends(get_current_user_dep(User)),db: AsyncSession = Depends(get_db),):
    return await AuthController.change_password(payload, current_user, db)