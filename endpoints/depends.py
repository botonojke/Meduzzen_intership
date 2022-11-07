from fastapi import Depends, HTTPException, status

from core.security import JWTBearer, decode_access_token
from models.user import User
from models.company import Company
from repositories.users import UserRepository
from repositories.company import CompanyRepository
from repositories.quiz import QuizRepository
from db.base import database


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_company_repository() -> CompanyRepository:
    return CompanyRepository(database)

def get_quiz_repository() -> QuizRepository:
    return QuizRepository(database)

async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer())) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Creddential are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception

    email: str = payload.get('sub')
    if email is None:
        raise cred_exception
    if email.find("@") == -1:
        email: str = payload.get('email')
    user = await users.get_by_email(email=email)
    if user is None:
        try:
            user = await users.create_user_auth0(email=email)
            return user
        except:
            raise cred_exception
    return user
