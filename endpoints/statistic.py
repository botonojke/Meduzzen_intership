import datetime
from typing import List


from models.quiz import Quiz, UpdateQuiz, CreateQuiz, Question, QuestionCreate, QuestionUpdate, Answers, PublicAnswers
from models.statistic import UserStatistic, AvgRate, LastQuizTest, UserLastTest, LastUserQuizTest
from models.user import PublicUser, User
from repositories.company import CompanyRepository
from repositories.statistic import StatisticRepository
from fastapi import APIRouter, Depends, HTTPException, status
from endpoints.depends import get_quiz_repository, get_current_user, get_company_repository, get_stat_repository, \
    get_user_repository
from repositories.users import UserRepository

router = APIRouter()


@router.get("/", response_model=List[UserStatistic])
async def get_all_company_users_rate(
        company_id: int,
        limit: int = 100,
        skip: int = 0,
        stat: StatisticRepository = Depends(get_stat_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> List[UserStatistic]:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company.user_id != int(current_user.id):
        if admin:
            return await stat.get_all_users_rate(limit=limit, skip=skip, company_id=company_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    return await stat.get_all_users_rate(limit=limit, skip=skip, company_id=company_id)


@router.get("/user_rate", response_model=List[UserStatistic])
async def get_one_company_user_rate(
        company_id: int,
        user_id: int,
        stat: StatisticRepository = Depends(get_stat_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> List[UserStatistic]:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company.user_id != int(current_user.id):
        if admin:
            return await stat.get_one_user_rate(company_id=company_id, user_id=user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    return await stat.get_one_user_rate(company_id=company_id, user_id=user_id)


@router.get("/user_avg_rate", response_model=AvgRate)
async def get_one_company_user_rate(
        user_id: int,
        stat: StatisticRepository = Depends(get_stat_repository)) -> AvgRate:
    return await stat.get_avg_rate(user_id=user_id)


@router.get("/user_avg_quiz_rate", response_model=List[LastQuizTest])
async def get_avg_quiz_rate(
        user_id: int,
        stat: StatisticRepository = Depends(get_stat_repository),
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)) -> List[LastQuizTest]:
    old_user = await users.get_by_id(id=user_id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found user')
    return await stat.get_avg_quiz_rate(user_id=user_id)


@router.get("/users_last_test")
async def get_company_users_last_test(
        company_id: int,
        limit: int = 100,
        skip: int = 0,
        stat: StatisticRepository = Depends(get_stat_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> dict[str, datetime]:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company.user_id != int(current_user.id):
        if admin:
            return await stat.get_last_test(limit=limit, skip=skip, company_id=company_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    return await stat.get_last_test(limit=limit, skip=skip, company_id=company_id)


@router.get("/user_last_test")
async def get_user_last_tests(
        user_id: int,
        stat: StatisticRepository = Depends(get_stat_repository),
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)) -> dict[str, datetime]:
    old_user = await users.get_by_id(id=user_id)
    if old_user is None or old_user.email != current_user.email:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found user')
    return await stat.user_last_test(user_id=user_id)
