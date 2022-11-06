import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr



class Company(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    is_active: bool = True
    create_date: datetime.datetime
    update_date: datetime.datetime


class Owner(BaseModel):
    title: str
    description: str
    is_active: bool = True


class Invite(BaseModel):
    user_id: int
    company_id: int
    invite: bool = True


class Request(BaseModel):
    user_id: int
    company_id: int
    request: bool = True


class CompanyUser(BaseModel):
    user_id: int
    company_id: int
    invite: bool
    is_admin: bool
    decision: bool
    request: bool


class UpdateCompanyUser(BaseModel):
    user_id: int
    company_id: int
    is_admin: bool = True
    decision: bool = True


class AccessInvite(BaseModel):
    user_id: int
    company_id: int
    decision: bool = True

