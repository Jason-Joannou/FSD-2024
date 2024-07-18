from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UsernameUpdate(BaseModel):
    old_username: str
    new_username: str

class EmailUpdate(BaseModel):
    username: str
    new_email: str

class PasswordUpdate(BaseModel):
    username: str
    current_password: str
    new_password: str
    confirm_password: str

