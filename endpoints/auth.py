from fastapi import APIRouter, Depends, HTTPException, status, Response

from core.security import verify_password, create_access_token, token_auth_scheme, VerifyToken
from endpoints.depends import get_user_repository
from models.token import Token, Login
from repositories.users import UserRepository

router = APIRouter()

@router.post('/', response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return Token(
        access_token=create_access_token({'sub': user.email}),
        token_type="Bearer"
    )

@router.post('/me')
async def auth0(response: Response, token: str = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    return result
