import datetime
from typing import Optional
from pydantic import BaseModel, conint, constr


class Quiz(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    duration: int
    questions: conint(ge=3)
    create_date: datetime.datetime
    update_date: datetime.datetime


class UpdateQuiz(BaseModel):
    title: str
    description: str
    duration: int
    questions: conint(ge=3)


class CreateQuiz(BaseModel):
    company_id: int
    title: str
    description: str
    duration: int
    questions: conint(ge=3)


class Question(BaseModel):
    id: int
    quiz_id: int
    question: constr(max_length=100)
    option_1: constr(max_length=25)
    option_2: constr(max_length=25)
    option_3: constr(max_length=25)
    option_4: constr(max_length=25)
    answer: constr(max_length=25)


class QuestionUpdate(BaseModel):
    question: constr(max_length=100)
    option_1: constr(max_length=25)
    option_2: constr(max_length=25)
    option_3: constr(max_length=25)
    option_4: constr(max_length=25)
    answer: constr(max_length=25)


class QuestionCreate(BaseModel):
    quiz_id: int
    question: constr(max_length=100)
    option_1: constr(max_length=25)
    option_2: constr(max_length=25)
    option_3: constr(max_length=25)
    option_4: constr(max_length=25)
    answer: constr(max_length=25)
