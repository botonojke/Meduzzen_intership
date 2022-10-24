from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from models.user import User, UserCreate, UserRsposneId, UserUpdate
from endpoints.depends import get_user_repository

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0):
    return await users.get_all(limit=limit, skip=0)


@router.post("/", response_model=UserRsposneId)
async def create_user(
        user: UserCreate,
        users: UserRepository = Depends(get_user_repository)):
    return await users.create(u=user)


@router.put("/", response_model=User)
async def update_user(
        id: int,
        user: UserUpdate,
        users: UserRepository = Depends(get_user_repository)):
    return await users.update(id=id, u=user)
