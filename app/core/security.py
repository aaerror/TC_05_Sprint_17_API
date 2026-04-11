from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Annotated, Any, Dict, Optional

from app.database import db_token
from app.shared.token_type import TokenType

import secrets



oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET_KEY = "TRWAGMYFPDXBNJZSQVHLCKE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_SECONDS = 3600
REFRESH_TOKEN_EXPIRY_DAYS = 14

def generate_token(
    data: Dict[str, Any],
    token_type: TokenType = TokenType.ACCESS_TOKEN,
    expiry_time: Optional[timedelta] = None
) -> str:
    """Create a short-lived access token for API authentication"""
    to_encode = data.copy()                        # Don't modify original data

    if not expiry_time:
        if token_type == TokenType.ACCESS_TOKEN:
            expiry_time = timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS)
        elif token_type == TokenType.REFRESH_TOKEN:
            expiry_time = timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
        else:
            raise ValueError("Invalid token type")

    # Calculate expiration time
    now = datetime.now(timezone.utc)
    expire = now + expiry_time

    # Add standard JWT claims
    to_encode.update({
        "sub": str(data["user_id"]),
        "exp": float(expire.timestamp()),          # Expiration time
        "iat": float(now.timestamp()),             # Issued at time
        "type": token_type,                        # Token type for validation
        "jti": secrets.token_urlsafe(16)           # Unique ID for revocation
    })

    # Sign and return the JWT
    token = jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    db_token.save_token(
        jti=to_encode["jti"],
        user_id=data["user_id"],
        issued_at=float(now.timestamp()),
        expires_at=float(expire.timestamp()),
        token=token,
        token_type=token_type
    )

    return token


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token, raising ValueError on failure"""
    try:
        # This also verifies signature and expiration
        return jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def authenticate_user(token: Annotated[str, Depends(oauth2)]) -> Dict[str, Any]:
    try:
        data = decode_token(token)

        token_type = data.get("type")
        if not data or token_type != TokenType.ACCESS_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token"
            )

        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )