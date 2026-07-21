from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (ChangePasswordRequest,LoginRequest,RegisterRequest,TokenResponse)
from app.models.customer import Customer
from app.utils import (get_tokens, hash_password,verify_password)

class AuthController:
    @staticmethod
    async def register(payload: RegisterRequest, db: AsyncSession):
        result = (await db.execute(select(Customer).where(or_(Customer.email == payload.get("email"),Customer.username == payload.get("username")))))
        if result.scalars().first():
            return {"response": "this Customer already exists", "status": "failed"}

        passwordHash = hash_password(payload.get("password"))
        Customer = Customer(email=payload.get("email"),username=payload.get("username"),name=payload.get("name"),password=passwordHash)
        db.add(Customer)

        await db.commit()
        await db.refresh(Customer)
        return {"response": "Registration successful"}

    @staticmethod
    async def login(payload: LoginRequest, db: AsyncSession, table):
        result = await db.execute(select(table).where(table.username == payload.username))
        Customer = result.scalar_one_or_none()
        if not Customer or not verify_password(payload.password, Customer.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        role = Customer.role if hasattr(Customer, "role") else "Customer"
        tokens = await get_tokens(Customer, role=role)
        return {"response": "login successful", "tokens": tokens}

    @staticmethod
    async def change_password(payload: ChangePasswordRequest,current_Customer: Customer,db: AsyncSession):
        if not verify_password(payload.old_password, current_Customer.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old password is incorrect",)
        current_Customer.password = hash_password(payload.new_password)
        await db.commit()
        return {"message": "Password changed successfully"}