from repositories.base import BaseRepository
from models.quiz import Quiz, UpdateQuiz, CreateQuiz, Question, QuestionUpdate, QuestionCreate
import datetime
from typing import List, Optional
from db.quiz import quizzes, questions


class QuizRepository(BaseRepository):

    async def create_quiz(self, company_id: int, quiz: CreateQuiz) -> Quiz:
        quiz = Quiz(
            id=0,
            company_id=company_id,
            create_date=datetime.datetime.utcnow(),
            update_date=datetime.datetime.utcnow(),
            title=quiz.title,
            description=quiz.description,
            duration=quiz.duration,
            questions=quiz.questions
        )
        values = {**quiz.dict()}
        values.pop("id", None)
        query = quizzes.insert().values(**values)
        quizzes.id = await self.database.execute(query=query)
        return quiz

    async def get_all_company_quizzes(self, company_id: int, limit: int = 100, skip: int = 0) -> List[Quiz]:
        query = quizzes.select().limit(limit).offset(skip).where(quizzes.c.company_id == company_id)
        data = await self.database.fetch_all(query=query)
        return [Quiz(**item) for item in data]

    async def delete_company_quiz(self, quiz_id: int, company_id: int):
        query = quizzes.delete().where(quizzes.c.id == quiz_id,
                                       quizzes.c.company_id == company_id)
        return await self.database.execute(query=query)

    async def update_quiz(self, quiz_id: int, company_id: int, update: UpdateQuiz) -> Quiz:
        quiz = Quiz(
            id=quiz_id,
            company_id=company_id,
            create_date=datetime.datetime.utcnow(),
            update_date=datetime.datetime.utcnow(),
            title=update.title,
            description=update.description,
            duration=update.duration,
            questions=update.questions
        )
        values = {**quiz.dict()}
        values.pop("create_date", None)
        values.pop("id", None)
        values.pop("company_id", None)
        query = quizzes.update().where(quizzes.c.id == quiz_id).values(**values)
        await self.database.execute(query=query)
        return quiz

    async def create_question(self, quiz_id: int, question: QuestionCreate) -> Question:
        question = Question(
            id=0,
            quiz_id=quiz_id,
            question=question.question,
            option_1=question.option_1,
            option_2=question.option_2,
            option_3=question.option_3,
            option_4=question.option_4,
            answer=question.answer
        )
        values = {**question.dict()}
        values.pop("id", None)
        query = questions.insert().values(**values)
        questions.id = await self.database.execute(query=query)
        return question

    async def get_all_quiz_question(self, quiz_id: int, limit: int = 100, skip: int = 0) -> List[Question]:
        query = questions.select().limit(limit).offset(skip).where(questions.c.quiz_id == quiz_id)
        data = await self.database.fetch_all(query=query)
        return [Question(**item) for item in data]

    async def delete_quiz_question(self, quiz_id: int, question_id: int):
        query = questions.delete().where(questions.c.id == quiz_id,
                                         questions.c.id == question_id)
        return await self.database.execute(query=query)

    async def update_question(self, question_id: int, quiz_id: int, question: QuestionUpdate) -> QuestionUpdate:
        question = QuestionUpdate(
            id=question_id,
            quiz_id=quiz_id,
            question=question.question,
            option_1=question.option_1,
            option_2=question.option_2,
            option_3=question.option_3,
            option_4=question.option_4,
            answer=question.answer
        )
        values = {**question.dict()}
        values.pop("id", None)
        values.pop("quiz_id", None)
        query = questions.update().where(questions.c.id == question_id).values(**values)
        await self.database.execute(query=query)
        return question
