from typing import List

from db.base import set_redis
from models.quiz import Quiz, UpdateQuiz, CreateQuiz, Question, QuestionCreate, QuestionUpdate, Answers, PublicAnswers
from models.user import PublicUser
from repositories.company import CompanyRepository
from repositories.quiz import QuizRepository
from fastapi import APIRouter, Depends, HTTPException, status
from endpoints.depends import get_quiz_repository, get_current_user, get_company_repository

router = APIRouter()


@router.get("/", response_model=List[Quiz])
async def show_all_companies_quiz(
        company_id: int,
        limit: int = 100,
        skip: int = 0,
        quizz: QuizRepository = Depends(get_quiz_repository)) -> List[Quiz]:
    return await quizz.get_all_company_quizzes(limit=limit, skip=skip, company_id=company_id)


@router.post("/", response_model=CreateQuiz)
async def create_quiz(
        quiz: CreateQuiz,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> Quiz:
    company = await comp.get_by_id_company(id=quiz.company_id)
    admin = await comp.get_company_admin(company_id=quiz.company_id, user_id=int(current_user.id))
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    if company.user_id != int(current_user.id):
        if admin:
            return await quizz.create_quiz(company_id=quiz.company_id, quiz=quiz)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    return await quizz.create_quiz(company_id=quiz.company_id, quiz=quiz)


@router.put("/", response_model=Quiz)
async def update_quiz(
        company_id: int,
        quiz_id: int,
        quiz: UpdateQuiz,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> Quiz:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company.user_id != int(current_user.id):
        if admin:
            return await quizz.update_quiz(company_id=company_id, quiz_id=quiz_id, update=quiz)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    return await quizz.update_quiz(company_id=company_id, quiz_id=quiz_id, update=quiz)


@router.delete("/")
async def delete_quiz(
        company_id: int,
        quiz_id: int,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> HTTPException:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company.user_id != int(current_user.id):
        if admin:
            await quizz.delete_company_quiz(company_id=company_id, quiz_id=quiz_id)
            return HTTPException(status_code=status.HTTP_200_OK, detail="Quiz deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    await quizz.delete_company_quiz(company_id=company_id, quiz_id=quiz_id)
    return HTTPException(status_code=status.HTTP_200_OK, detail="Quiz deleted")


@router.get("/quiz", response_model=List[Question])
async def show_all_quiz_question(
        quiz_id: int,
        limit: int = 100,
        skip: int = 0,
        quizz: QuizRepository = Depends(get_quiz_repository)) -> List[Question]:
    return await quizz.get_all_quiz_question(limit=limit, skip=skip, quiz_id=quiz_id)


@router.post("/quiz", response_model=QuestionCreate)
async def create_question(
        company_id: int,
        question: QuestionCreate,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> Question:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    if company.user_id != int(current_user.id):
        if admin:
            return await quizz.create_question(quiz_id=question.quiz_id, question=question)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    return await quizz.create_question(quiz_id=question.quiz_id, question=question)


@router.put("/quiz", response_model=QuestionUpdate)
async def update_question(
        company_id: int,
        quiz_id: int,
        question_id: int,
        question: QuestionUpdate,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> QuestionUpdate:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company.user_id != int(current_user.id):
        if admin:
            return await quizz.update_question(question_id=question_id, quiz_id=quiz_id, question=question)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    return await quizz.update_question(question_id=question_id, quiz_id=quiz_id, question=question)


@router.delete("/quiz")
async def delete_question(
        company_id: int,
        question_id: int,
        quiz_id: int,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)) -> HTTPException:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company.user_id != int(current_user.id):
        if admin:
            await quizz.delete_quiz_question(question_id=question_id, quiz_id=quiz_id)
            return HTTPException(status_code=status.HTTP_200_OK, detail="question deleted")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    await quizz.delete_quiz_question(question_id=question_id, quiz_id=quiz_id)
    return HTTPException(status_code=status.HTTP_200_OK, detail="question deleted")


@router.post("/quiz/answer")
async def answer(
        answers: PublicAnswers,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        ) -> Answers:
    return await quizz.post_answers(user_id=int(current_user.id), answer=answers)
