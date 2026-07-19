from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (ChangePasswordRequest,LoginRequest,RegisterRequest,TokenResponse)
from app.models.user import User
from app.utils import (get_tokens, hash_password,verify_password)

class AuthController:
    @staticmethod
    async def register(payload: RegisterRequest, db: AsyncSession):
        result = (await db.execute(select(User).where(or_(User.email == payload.get("email"),User.username == payload.get("username")))))
        if result.scalars().first():
            return {"response": "this user already exists", "status": "failed"}

        passwordHash = hash_password(payload.get("password"))
        user = User(email=payload.get("email"),username=payload.get("username"),name=payload.get("name"),password=passwordHash)
        db.add(user)

        await db.commit()
        await db.refresh(user)
        return {"response": "Registration successful"}

    @staticmethod
    async def login(payload: LoginRequest, db: AsyncSession, table):
        result = await db.execute(select(table).where(table.username == payload.username))
        user = result.scalar_one_or_none()
        if not user or not verify_password(payload.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        role = user.role if hasattr(user, "role") else "user"
        tokens = await get_tokens(user, role=role)
        return {"response": "login successful", "tokens": tokens}

    @staticmethod
    async def change_password(payload: ChangePasswordRequest,current_user: User,db: AsyncSession):
        if not verify_password(payload.old_password, current_user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old password is incorrect",)
        current_user.password = hash_password(payload.new_password)
        await db.commit()
        return {"message": "Password changed successfully"}