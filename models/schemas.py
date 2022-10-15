import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator, constr


class User(BaseModel):
    id: Optional[str]
    username: str
    email: EmailStr
    password: str
    about_user: Optional[str] = None
    register_date: datetime.datetime
    update_date: datetime.datetime
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class SignInUser(BaseModel):
    username: str
    password: str


class SignUpUser(BaseModel):
    username: str
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str
    about_user: Optional[str] = None

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


class UpdateUser(BaseModel):
    username: Optional[str]
    password: Optional[constr(min_length=3)]
    about_user: Optional[str]
    is_active: Optional[bool]

    class Config:
        orm_mode = True


