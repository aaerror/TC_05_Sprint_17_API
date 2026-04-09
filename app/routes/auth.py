from datetime import datetime, timedelta, timezone

from app.database import db_user, db_token

from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, JWTError
from typing import Annotated, Any, Dict, Optional

from pydantic import BaseModel
import secrets




router = APIRouter(prefix="/auth", tags=["Authorization"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = "TRWAGMYFPDXBNJZSQVHLCKE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_SECONDS = 3600
REFRESH_TOKEN_EXPIRY_DAYS = 30


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshToken(BaseModel):
    refresh_token: str


def create_access_token(
    data: Dict[str, Any],
    expiry: Optional[timedelta] = None
) -> str:
    """Create a short-lived access token for API authentication"""
    to_encode = data.copy()                        # Don't modify original data

    now = datetime.now(timezone.utc)
    # Calculate expiration time
    expire = now + (
        expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS)
    )

    # Add standard JWT claims
    to_encode.update({
        "sub": str(data["user_id"]),
        "exp": int(expire.timestamp()),            # Expiration time
        "iat": int(now.timestamp()),               # Issued at time
        "type": "access",                          # Token type for validation
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
        issued_at=int(now.timestamp()),
        expires_at=int(expire.timestamp()),
        token=token,
        token_type="access_token"
    )

    return token

def create_refresh_token(
    data: Dict[str, Any],
    expire_time: Optional[timedelta] = None
) -> str:
    # """Create a longer-lived refresh token for obtaining new access tokens"""
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    # Refresh tokens have longer expiry
    expire = now + (
        expire_time or timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
    )

    to_encode.update({
        "sub": str(data["user_id"]),
        "exp": int(expire.timestamp()),            # Expiration time
        "iat": int(now.timestamp()),               # Issued at time
        "type": "refresh",                         # Token type for validation
        "jti": secrets.token_urlsafe(16)           # Unique ID for revocation
    })

    token = jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    db_token.save_token(
        jti=to_encode["jti"],
        user_id=data["user_id"],
        issued_at=int(now.timestamp()),
        expires_at=int(expire.timestamp()),
        token=token,
        token_type="refresh_token"
    )

    return token

def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token, raising ValueError on failure"""
    try:
        # This also verifies signature and expiration
        return jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def decode_tokens(token: Annotated[str, Depends(oauth2)]) -> Dict[str, Any]:
    """Decode and validate a JWT token, raising ValueError on failure"""
    try:
        # This also verifies signature and expiration
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail=f"Invalid token")


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Generate a new access token"
)
def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = db_user.get_user(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    is_valid = db_user.is_valid_password(
        int(user["user_id"]),
        form_data.password
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # - Generate an access_token
    access_token = create_access_token({
        "user_id": str(user["user_id"]),
        "username": user["username"]
    })

    # - Generate an refresh_token
    refresh_token = create_refresh_token({
        "user_id": str(user["user_id"]),
        "username": user["username"]
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post(
    "/refresh",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Generate a new access token after the previous one expires")
def refresh_token(
    request: RefreshToken
):
    data = decode_token(request.refresh_token)
    response = db_token.get_token_by_jti(data["jti"]) 
    print(response)

    return {
        "access_token": "Test",
        "refresh_token": "Test",
        "token_type": "bearer"
    }