import datetime
from typing import Optional, Dict
from pydantic import BaseModel, conint, constr


class UserStatistic(BaseModel):
    user_id: int
    quiz_id: int
    create_date: datetime.datetime
    average_quiz_mark: float


class UserLastTest(BaseModel):
    user_id: int
    create_date: datetime.datetime


class AvgRate(BaseModel):
    user_id: int
    quiz_rate: float


class LastQuizTest(BaseModel):
    quiz_id: int
    company_id: int
    average_quiz_mark: float
    create_date: datetime.datetime


class LastUserQuizTest(BaseModel):
    quiz_id: int
    create_date: datetime.datetime