from fastapi import Depends, HTTPException, status

from core.security import JWTBearer, decode_access_toke
from models.user import User
from repositories.users import UserRepository
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer()),
) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Creddential are not valid")
    payload = decode_access_toke(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get('sub')
    if email is None:
        raise cred_exception
    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user
