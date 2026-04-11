from app.core.security import generate_token, decode_token
from app.database import db_user, db_token
from app.schemes.auth import AccessToken, RefreshToken, Token
from app.shared.token_type import TokenType

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Annotated





router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post(
    path="/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Generate a new token"
)
def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = db_user.get_user_by_username(form_data.username)
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

    # Generate an access_token
    access_token = generate_token(
        data={"user_id": str(user["user_id"])},
        token_type=TokenType.ACCESS_TOKEN
    )

    # Generate an refresh_token
    refresh_token = generate_token(
        data={"user_id": str(user["user_id"])},
        token_type=TokenType.REFRESH_TOKEN
    )

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post(
    path="/refresh",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    summary="Generate a new access token after the previous one expires")
def create_access_token(
    request: RefreshToken
):
    data = decode_token(request.refresh_token)
    response = db_token.get_token_by_jti(data["jti"])
    if not response or response["token_type"] != TokenType.REFRESH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Generate a new access_token
    access_token = generate_token(
        data={"user_id": str(response["user_id"])},
        token_type=TokenType.ACCESS_TOKEN
    )

    return AccessToken(access_token=access_token)