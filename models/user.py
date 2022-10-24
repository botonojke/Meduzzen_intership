import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool
    is_admin: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_active: bool = True

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v


class UserRsposneId(BaseModel):
    id: int


class UserUpdate(BaseModel):
    name: str
    password: constr(min_length=8)
    password2: str
    is_active: bool = True
    updated_at: datetime.datetime = datetime.datetime.utcnow()

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v
