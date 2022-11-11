from sqlalchemy import desc

from models.statistic import UserStatistic, UserLastTest, AvgRate, LastQuizTest, LastUserQuizTest
from repositories.base import BaseRepository

import datetime
from typing import List, Optional, Dict
from db.quiz import quizzes, questions, quiz_rate, answers
from db.base import set_redis


class StatisticRepository(BaseRepository):

    async def get_all_users_rate(self, company_id: int, limit: int = 100, skip: int = 0) -> List[UserStatistic]:
        query = answers.select().limit(limit).offset(skip).where(
            answers.c.company_id == company_id)
        data = await self.database.fetch_all(query=query)
        return [UserStatistic(**item) for item in data]

    async def get_one_user_rate(self, company_id: int, user_id: int) -> List[UserStatistic]:
        query = answers.select().where(
            answers.c.company_id == company_id,
            answers.c.user_id == user_id)
        data = await self.database.fetch_all(query=query)
        return [UserStatistic(**item) for item in data]

    async def get_last_test(self, company_id: int, limit: int = 100, skip: int = 0) -> dict[str, datetime]:
        query = answers.select().limit(limit).offset(skip).where(
            answers.c.company_id == company_id).order_by(desc(answers.c.user_id), answers.c.create_date)
        data = await self.database.fetch_all(query=query)
        res = {}
        for result in data:
            user = UserLastTest(**result)
            if res.get(str(user.user_id)) is None:
                res[str(user.user_id)] = user.create_date
            if res[str(user.user_id)] < user.create_date:
                res[str(user.user_id)] = user.create_date

        return res

    async def get_avg_rate(self, user_id: int) -> AvgRate:
        query = quiz_rate.select().where(quiz_rate.c.user_id == user_id)
        data = await self.database.fetch_one(query=query)
        return AvgRate(**data)

    async def get_avg_quiz_rate(self, user_id: int) -> List[LastQuizTest]:
        query = answers.select().where(answers.c.user_id == user_id)
        data = await self.database.fetch_all(query=query)
        return [LastQuizTest(**item) for item in data]

    async def user_last_test(self, user_id: int) -> dict[str, datetime]:
        query = answers.select().where(
                answers.c.user_id == user_id)
        data = await self.database.fetch_all(query=query)
        res = {}
        for result in data:
            user = LastUserQuizTest(**result)
            if res.get(str(user.quiz_id)) is None:
                res[str(user.quiz_id)] = user.create_date
            if res.get(str(user.quiz_id)) < user.create_date:
                res[str(user.quiz_id)] = user.create_date
        return res
