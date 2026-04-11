from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from app.core.security import authenticate_user
from app.schemes.user import User, UserAdd, UserUpdate

from typing import Annotated, Any, Dict, List

import app.database.db_user as db




router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    path="/",
    response_model=List[User],
    summary="Get all users",
    status_code=200
)
def get_users(
    data: Dict[str, Any] = Depends(authenticate_user)
):
    return db.get_users()


@router.post(
    path="/",
    summary="Create a new user",
    status_code=201
)
def add_user(
    user: UserAdd,
    data: Dict[str, Any] = Depends(authenticate_user)
):
    try:
        db.add_user(user.username, user.password, user.email)

        return {
            "detail": "User added successfully"
        }
    except Exception:
        msg = "An error has occurred"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get a user by ID",
    status_code=200
)
def get_user(user_id: int, data: Dict[str, Any] = Depends(authenticate_user)):
    user = db.get_user_by_id(user_id)
    if not user:
        msg = "User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

    return user


@router.patch(
    path="/{user_id}",
    summary="Edit a user by ID",
    status_code=200
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    data: Dict[str, Any] = Depends(authenticate_user)
):
    user = db.get_user_by_id(user_id)
    if not user:
        msg = "User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

    try:
        db.update_user_by_id(user["user_id"], user_data.email)

        return {
            "detail": "User updated successfully"
        }
    except Exception:
        msg = "An error has occurred"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )


@router.delete(
    path="/{user_id}",
    summary="Delete a user by ID",
    status_code=204
)
def delete_user(
    user_id: int,
    data: Dict[str, Any] = Depends(authenticate_user)
):
    user = db.get_user_by_id(user_id)
    if not user:
        msg = "User not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

    try:
        db.delete_user_by_id(user["user_id"])
    except Exception:
        msg = "An error has occurred"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )