from repositories.base import BaseRepository
from models.company import Company, Owner, Invite, Request, CompanyUser, UpdateCompanyUser, AccessInvite
import datetime
from typing import List, Optional
from db.company import companies, company_users


class CompanyRepository(BaseRepository):

    async def create_company(self, user_id: int, owner: Owner) -> Company:
        company = Company(
            id=0,
            user_id=user_id,
            create_date=datetime.datetime.utcnow(),
            update_date=datetime.datetime.utcnow(),
            title=owner.title,
            description=owner.description,
            is_active=owner.is_active,
        )
        values = {**company.dict()}
        values.pop("id", None)
        query = companies.insert().values(**values)
        company.id = await self.database.execute(query=query)
        return company

    async def update_company(self, id: int, user_id: int, owner: Owner) -> Company:
        company = Company(
            id=id,
            user_id=user_id,
            update_date=datetime.datetime.utcnow(),
            create_date=datetime.datetime.utcnow(),
            title=owner.title,
            description=owner.description,
            is_active=owner.is_active,
        )
        values = {**company.dict()}
        values.pop("create_date", None)
        values.pop("id", None)
        query = companies.update().where(companies.c.id == id).values(**values)
        await self.database.execute(query=query)
        return company

    async def all_company(self, limit: int = 100, skip: int = 0) -> List[Company]:
        query = companies.select().limit(limit).offset(skip).where(companies.c.is_active)
        data = await self.database.fetch_all(query=query)
        return [Company(**item) for item in data]

    async def delete_company(self, id: int):
        query = companies.delete().where(companies.c.id == id)
        return await self.database.execute(query=query)

    async def get_by_id_company(self, id: int) -> Optional[Company]:
        query = companies.select().where(companies.c.id == id)
        company = await self.database.fetch_one(query=query)
        if company is None:
            return None
        return Company.parse_obj(company)

    async def invite_user(self, user_id: int, company_id: int, invite: Invite):
        invite = Invite(
            company_id=company_id,
            user_id=user_id,
            invite=invite.invite,
        )
        values = {**invite.dict()}
        query = company_users.insert().values(**values)
        await self.database.execute(query=query)
        return invite

    async def request(self, user_id: int, company_id: int, request: Request):
        request = Request(
            company_id=company_id,
            user_id=user_id,
            request=request.request,
        )
        values = {**request.dict()}
        query = company_users.insert().values(**values)
        await self.database.execute(query=query)
        return request

    async def get_user_from_company(self, user_id: int, company_id: int) -> CompanyUser:
        query = company_users.select().where(
            company_users.c.user_id == user_id,
            company_users.c.company_id == company_id)
        company_user = await self.database.fetch_one(query=query)
        if company_user is None:
            return None
        return CompanyUser.parse_obj(company_user)

    async def delete_user(self, user_id: int, company_id: int):
        query = company_users.delete().where(company_users.c.user_id == user_id,
                                             company_users.c.company_id == company_id)
        return await self.database.execute(query=query)

    async def update_user(self, company_id: int, user_id: int, company_user: UpdateCompanyUser) -> UpdateCompanyUser:
        user = UpdateCompanyUser(
            company_id=company_id,
            user_id=user_id,
            invite=True,
            is_admin=company_user.is_admin,
            decision=company_user.decision,
            request=True,
        )
        values = {**user.dict()}
        query = company_users.update().where(company_users.c.user_id == user_id,
                                             company_users.c.company_id == company_id).values(**values)
        await self.database.execute(query=query)
        return user

    async def access_invite(self, company_id: int, user_id: int, company_user: AccessInvite) -> UpdateCompanyUser:
        user = UpdateCompanyUser(
            company_id=company_id,
            user_id=user_id,
            invite=True,
            is_admin=False,
            decision=company_user.decision,
            request=True,
        )
        values = {**user.dict()}
        query = company_users.update().where(company_users.c.user_id == user_id,
                                             company_users.c.company_id == company_id).values(**values)
        await self.database.execute(query=query)
        return user
