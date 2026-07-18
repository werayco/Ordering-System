from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import (ChangePasswordRequest,LoginRequest,RegisterRequest,TokenResponse)
from app.models.user import User
from app.utils import (get_tokens, hash_password,issue_access_token,issue_refresh_token,verify_password)

class AuthController:
    @staticmethod
    async def register(payload: RegisterRequest, db: AsyncSession):
        result = await db.execute(select(User).where(or_(User.email == payload.get("email"),User.username == payload.get("username"))))
        if result.scalars().first():
            return {"response": "this user already exists", "status": "failed"}

        passwordHash = hash_password(payload.get("password"))
        user = User(email=payload.get("email"),username=payload.get("username"),name=payload.get("name"),password=passwordHash)
        db.add(user)

        await db.commit()
        await db.refresh(user)
        return get_tokens(user)

    @staticmethod
    async def login(payload: LoginRequest, db: AsyncSession):
        user = await db.execute(select(User).where(User.username==payload.username)).scalar_one_or_none()
        if not user or not verify_password(payload.password, user.password):
            return {"response": "invalid username or password", "status": "failed"}
        return {"response": "login successful", "tokens": get_tokens(user)}

    @staticmethod
    async def change_password(payload: ChangePasswordRequest,current_user: User,db: AsyncSession):
        if not verify_password(payload.old_password, current_user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old password is incorrect",)
        current_user.password = hash_password(payload.new_password)
        await db.commit()
        return {"message": "Password changed successfully"}