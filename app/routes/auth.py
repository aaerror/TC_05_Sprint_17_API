from datetime import datetime, timedelta, timezone

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
    to_encode = data.copy()                     # Don't modify original data

    now = datetime.now(timezone.utc)
    # Calculate expiration time
    expire = now + (
        expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS)
    )

    # Add standard JWT claims
    to_encode.update({
        "exp": expire,                              # Expiration time
        "iat": now,                                 # Issued at time
        "type": "access",                           # Token type for validation
        "jti": secrets.token_urlsafe(16)            # Unique ID for revocation
    })

    # Sign and return the JWT
    return jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(
    data: Dict[str, Any],
    expire_time: Optional[timedelta] = None
) -> str:
    """Create a longer-lived refresh token for obtaining new access tokens"""
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    # Refresh tokens have longer expiry
    expire = now + (
        expire_time or timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)
    )

    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": "refresh",                    # Distinguishes from access tokens
        "jti": secrets.token_urlsafe(16)      # Unique ID for rotation tracking
    })

    return jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token: Annotated[str, Depends(oauth2)]) -> Dict[str, Any]:
    """Decode and validate a JWT token, raising ValueError on failure"""
    try:
        # This also verifies signature and expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload
    except HTTPException:
        # raise ValueError(f"Invalid token: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid or expired token")


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Generate a new access token"
)
def create_token(
    payload: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> str:
    # TODO:
    # - Check access data into db and throw error in case that pass is
    # incorrect or user doesn't exist
    # - Generate an access_token

    return {
        "access_token": "",
        "refresh_token": "",
        "token_type": "bearer"
    }

    # return create_access_token(request)

@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Generate a new access token after the previous one expires")
def refresh_token(
    request: Annotated[dict, Depends(RefreshToken)]
):
    return {
        "token": "test"
    }