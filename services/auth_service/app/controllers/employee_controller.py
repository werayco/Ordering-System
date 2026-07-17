from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.schemas import (AccessTokenResponse,ChangePasswordRequest,LoginRequest,RefreshRequest,RegisterRequest,TokenResponse,UserResponse)
from app.db.crud import UserCrud
from app.models.employee import Employees
from app.schemas import RegisterEmployee, Roles, RegisterAdmin
from app.utils import (get_user_from_refresh_token,hash_password,issue_access_token,issue_refresh_token,verify_password)

class EmployeeController:
    @staticmethod
    async def register_admin(payload: RegisterAdmin, db: AsyncSession):
        result = await db.execute(
            select(func.count()).select_from(Employees).where(Employees.role == Roles.ADMIN.value)
        )
        admin_count = result.scalar_one()

        if admin_count >= 1:
            raise HTTPException(status_code=409, detail="An admin already exists")

        try:
            data = payload.model_dump()
            data["role"] = Roles.ADMIN.value
            data["password"] = hash_password(data["password"])

            add_admin = Employees(**data)
            db.add(add_admin)
            await db.commit()
            await db.refresh(add_admin)
            return {"message": "Admin registered successfully", "id": str(add_admin.id)}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def register_employee(payload: RegisterEmployee, db: AsyncSession):
        try:
            data = payload.model_dump()
            data["role"] = Roles.VIEWER.value
            data["password"] = hash_password(data["password"])

            add_employee = Employees(**data)
            db.add(add_employee)
            await db.commit()
            await db.refresh(add_employee)
            return {"message": "Employee registered successfully", "id": str(add_employee.id)}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_employee(db: AsyncSession, username:str):
        result = await db.execute(select(Employees).where(Employees.username==username))
        return result.scalar_one_or_none()

    @staticmethod
    async def change_password(db: AsyncSession, username:str, new_password: str):
        result = await db.execute(select(Employees).where(Employees.username==username))
        if not result.scalars().first():
            return {"response": "user not found", "status": "failed"}
        
        passwordHash = hash_password(new_password)
        user = result.scalars().first()
        user.password = passwordHash
        await db.commit()
        return {"response": "password changed successfully", "status": "success"}

    @staticmethod
    async def login(db: AsyncSession, username: str, password: str):
        user = await EmployeeController.get_employee(db, username)
        if not user or not verify_password(password, user.password):
            return {"response": "invalid username or password", "status": "failed"}
        
        return TokenResponse(
            access_token=issue_access_token(user),
            refresh_token=issue_refresh_token(user),
        )