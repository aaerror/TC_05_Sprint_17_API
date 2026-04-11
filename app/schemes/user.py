from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: int
    username: str
    email: EmailStr

class UserAdd(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserUpdate(BaseModel):
    email: EmailStr