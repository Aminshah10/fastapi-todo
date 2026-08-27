from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, InvalidSignatureError
from sqlalchemy.orm import Session

from app.core.config import setting
from app.core.database import get_db
from app.users.models import UserModel

DB_DEPENDENCY = Depends(get_db)

security = HTTPBearer()
SECURITY_DEPENDENCY = Depends(security)


def get_authenticated_user(
    db: Session = DB_DEPENDENCY,
    credentials: HTTPAuthorizationCredentials = SECURITY_DEPENDENCY,
):

    token = credentials.credentials
    try:
        decoded_token = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed, user_id not found in token",
            )
        if decoded_token.get("exp") < datetime.utcnow().timestamp():  # noqa: DTZ003
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed, token has expired",
            )
        if decoded_token.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed, invalid token type",
            )
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed, user not found",
            )
        return user_obj

    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed, Invalid token signature",
        )
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed, decode failed",
        )

def generate_access_token(user_id: int, expires_in: int = 3600) -> str:
    now = datetime.utcnow()  # noqa: DTZ003
    payload = {
        "type": "access",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    token = jwt.encode(payload, setting.JWT_SECRET_KEY, algorithm="HS256")
    return token

def generate_refresh_token(user_id: int, expires_in: int = 604800) -> str:
    now = datetime.utcnow()  # noqa: DTZ003
    payload = {
        "type": "refresh",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    token = jwt.encode(payload, setting.JWT_SECRET_KEY, algorithm="HS256")
    return token