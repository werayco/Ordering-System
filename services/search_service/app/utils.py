import json
from uuid import UUID
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

def deserialize_from_json(data):
    try:
        return json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(f"Data deserialization error: {e}")

bearer_scheme = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    credentials_exception = HTTPException(status_code=401, detail="Invalid or expired token")
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "access":
            raise credentials_exception
        UUID(payload["sub"])
    except (JWTError, ValueError, KeyError):
        raise credentials_exception

    return payload