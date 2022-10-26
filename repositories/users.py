import datetime
from typing import List, Optional

from sqlalchemy import insert

from db.users import users
from models.user import User, UserCreate, UserRsposneId, UserUpdate
from core.security import hash_password
from repositories.base import BaseRepository


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        data = await self.database.fetch_all(query=query)
        return [User(**item) for item in data]

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
            hashed_password=hash_password(u.password2),
            is_active=u.is_active,
            is_admin=False,
            create_date=datetime.datetime.utcnow(),
            update_date=datetime.datetime.utcnow(),
        )
        return UserRsposneId(id=await self.database.execute(user))

    async def update(self, id: int, u: UserUpdate) -> UserRsposneId:
        now = datetime.datetime.utcnow()
        updated_data = u.dict(skip_defaults=True)
        updated_data['update_date'] = now
        if updated_data.get('password'):
            updated_data['hashed_password'] = hash_password(updated_data['password'])
            updated_data.pop('password', None)
            updated_data.pop('password2', None)
        u = users.update().values(updated_data).where(users.c.id == id)

        await self.database.execute(u)
        return UserRsposneId(id=id)


    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
