import datetime
from typing import List, Optional
from db.users import users
from models.user import User, UserCreate, UserRsposneId, UserUpdate
from core.security import hash_password
from repositories.base import BaseRepository


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        data = await self.database.fetch_all(query=query)
        return [User(*item) for item in data]


    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserCreate) -> UserRsposneId:
        user = users.insert().values(
            name=u.name,
            email=u.email,
            password=hash_password(u.password2),
            password2=u.password2,
            is_active=u.is_active,
            is_admin=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        return UserRsposneId(id=await self.database.execute(user))

    async def update(self, id: int, u: UserUpdate) -> User:
        user = User(
            id=id,
            name=u.name,
            hashed_password=hash_password(u.password2),
            is_active=u.is_active,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
