from datetime import datetime, timedelta, timezone
from uuid import UUID
import bcrypt
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.models.user import User
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
import secrets
import hashlib
from app.models import User, Employee
import redis


async def get_redis_client():
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )
    return redis_client


ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

bearer_scheme = HTTPBearer()

async def check_user_exists(username: str, db: AsyncSession):
    normalized_username = username.strip().lower()
    print(f"checking if user exists with username: {normalized_username}")
    result = await db.execute(select(User).where(User.username == normalized_username))
    data = result.scalar_one_or_none()
    user_exists = data is not None
    print(f"user exists: {user_exists}")
    return data, user_exists

async def get_receiever_id_by_username(username: str, db: AsyncSession):
    normalized_username = username.strip().lower()
    result = await db.execute(select(User).where(User.username == normalized_username))
    user = result.scalar_one_or_none()
    return user.id if user else None

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

def _build_token(user: User, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "iat": now,
        "exp": now + expires_delta,
        "type": token_type,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


async def issue_access_token(user: User) -> str:
    return _build_token(user, "access", timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

async def issue_refresh_token() -> str:
    return secrets.token_urlsafe(64)

async def get_tokens(user):
    access = await issue_access_token(user)
    refresh = await issue_refresh_token()
    redis_client = await get_redis_client()
    await redis_client.set(f"refresh:{user.id}", hash_token(refresh), ex=REFRESH_TOKEN_EXPIRE_DAYS * 86400)
    return {"access_token": access, "refresh_token": refresh}

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')    
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

async def cache_refresh_tokens(user_id: str,refresh_token: str):
    key = f"refresh:{user_id}"
    stored_hash = await get_redis_client().get(key)

    if not stored_hash:
        raise Exception("Refresh token has expired")

    if stored_hash != hash_token(refresh_token):
        raise Exception("Invalid refresh token")

    new_access_token = await issue_access_token(user_id)
    new_refresh_token = await issue_refresh_token()

    await get_redis_client().set(
        key,
        hash_token(new_refresh_token),
        ex=REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
    }