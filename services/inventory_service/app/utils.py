from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.config import settings
import redis

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


async def get_redis_client():
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )
    return redis_client

bearer_scheme = HTTPBearer()

def get_current_user_dep(table_name):
    async def _get_current_user(
        token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db),
    ):
        credentials_exception = HTTPException(status_code=401, detail="Invalid or expired token")
        try:
            payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("type") != "access":
                raise credentials_exception
            user_id = UUID(payload["sub"])
        except (JWTError, ValueError, KeyError):
            raise credentials_exception
        result = await db.execute(select(table_name).where(table_name.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
        return user
    return _get_current_user