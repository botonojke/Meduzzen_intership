from typing import List
from models.company import Company, Owner, Invite, Request, UpdateCompanyUser, AccessInvite
from models.user import PublicUser
from repositories.company import CompanyRepository
from fastapi import APIRouter, Depends, HTTPException, status
from endpoints.depends import get_company_repository, get_current_user

router = APIRouter()


@router.get("/", response_model=List[Company])
async def show_all_companies(
        limit: int = 100,
        skip: int = 0,
        comp: CompanyRepository = Depends(get_company_repository)) -> List[Company]:
    return await comp.all_company(limit=limit, skip=skip)


@router.post("/", response_model=Company)
async def create_company(
        owner: Owner,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> Company:
    return await comp.create_company(user_id=int(current_user.id), owner=owner)


@router.put("/", response_model=Company)
async def update_company(
        id: int,
        owner: Owner,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> Company:
    company = await comp.get_by_id_company(id=id)
    if company is None or company.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    return await comp.update_company(id=id, user_id=int(current_user.id), owner=owner)


@router.delete("/")
async def delete_company(
        id: int,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> dict:
    company = await comp.get_by_id_company(id=id)
    if company is None or company.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    await comp.delete_company(id=id)
    return {'status': True}


@router.post("/company/invite", response_model=dict)
async def invite_user(
        invite: Invite,
        company_id: int,
        user_id: int,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> dict:
    company = await comp.get_by_id_company(id=company_id)
    if company is None or company.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    await comp.invite_user(user_id=user_id, company_id=company.id, invite=invite)
    return {'status': 'User invited to the company'}


@router.post("/company/request", response_model=dict)
async def request_for_company(
        request: Request,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> dict:
    company = await comp.get_by_id_company(id=request.company_id)
    print(type(current_user.id))
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found")
    elif company.user_id == int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You can't send request to your company")
    await comp.request(user_id=int(current_user.id), company_id=request.company_id, request=request)
    return {'status': 'Request send to company'}

@router.delete("/company/user")
async def delete_user(
        user_id: int,
        company_id: int,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> dict:
    # user = await comp.get_user_from_company(user_id=user_id, company_id=company_id)
    company = await comp.get_by_id_company(id=company_id)
    if company is None or company.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    await comp.delete_user(user_id=user_id, company_id=company_id)
    return {'status': True}

@router.put("/company/user_update", response_model=UpdateCompanyUser)
async def update_company_user(
        user_id: int,
        company_id: int,
        company_user: UpdateCompanyUser,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> UpdateCompanyUser:
    company = await comp.get_by_id_company(id=company_id)
    if company is None or company.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    return await comp.update_user(company_id=company_id, user_id=user_id, company_user=company_user)


@router.put("/company/access_invite", response_model=AccessInvite)
async def access_invite(
        user_id: int,
        company_id: int,
        company_user: AccessInvite,
        comp: CompanyRepository = Depends(get_company_repository),
        current_user: PublicUser = Depends(get_current_user)) -> AccessInvite:
    company = await comp.get_by_id_company(id=company_id)
    if company is None or user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found")
    if not company_user.decision:
        return await comp.delete_user(user_id=user_id, company_id=company_id)
    return await comp.access_invite(company_id=company_id, user_id=user_id, company_user=company_user)
