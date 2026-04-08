from fastapi import APIRouter, FastAPI, Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from typing import Annotated




router = APIRouter(prefix="/users", tags=["Users"])


# schemas
class User(BaseModel):
    username: str
    email: str




@router.post("/", summary="Create a new user", status_code=201)
def add_user(user: User):
    print(user)
    return {
        "msg": "User added successufuly"
    }

@router.get("/{user_id}", summary="Get a user by ID", status_code=200)
def get_user(user_id: int):
    user = None

    if not user:
        msg = f"User not found (id: {user_id})"
        raise HTTPException(detail=msg, status_code=status.HTTP_404_NOT_FOUND)

    return {
        "msg": "User retrieved successfully"
    }

@router.patch("/{user_id}", summary="Edit a user by ID", status_code=200)
def update_user(user_id: int, user: User):
    user = None

    if not user:
        msg = f"User not found (id: {user_id})"
        raise HTTPException(detail=msg, status_code=status.HTTP_404_NOT_FOUND)

    return {
        "msg": "User updated successfully"
    }

@router.delete("/{user_id}", summary="Delete a user by ID", status_code=204)
def delete_user(user_id: int):
    user = None

    if not user:
        msg = f"User not found (id: {user_id})"
        raise HTTPException(detail=msg, status_code=status.HTTP_404_NOT_FOUND)

    return None