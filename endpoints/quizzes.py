from typing import List

from fastapi.responses import FileResponse

from db.base import set_redis
from models.quiz import Quiz, UpdateQuiz, CreateQuiz, Question, QuestionCreate, QuestionUpdate, Answers, PublicAnswers
from models.user import PublicUser
from repositories.company import CompanyRepository
from repositories.export_files import get_csv_from_redis, file_path, get_all_csv_file_redis
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


@router.post("/quiz/answer", response_model=Answers)
async def answer(
        answers: PublicAnswers,
        quizz: QuizRepository = Depends(get_quiz_repository),
        current_user: PublicUser = Depends(get_current_user),
        ) -> Answers:
    return await quizz.post_answers(user_id=int(current_user.id), answer=answers)


@router.get("/download_user_quiz_answers")
async def get_user_answers(
        company_id: int,
        quiz_id: int,
        current_user: PublicUser = Depends(get_current_user)
        ) -> FileResponse:
    key = f"{company_id}-{quiz_id}-{current_user.id}"
    get_csv_from_redis(key=key)
    return FileResponse(path=file_path, filename='Your answers')


@router.get("/download_company_quiz")
async def get_all_company_quiz_result_for_one_user(
        company_id: int,
        quiz_id: int,
        user_id: int,
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)
        ) -> FileResponse:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    if company.user_id != int(current_user.id):
        if admin:
            return FileResponse(path=file_path, filename=f'{company.title} answers')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    key = f"{company_id}-{quiz_id}-{user_id}"
    get_csv_from_redis(key=key)
    return FileResponse(path=file_path, filename=f'{company.title} answers')


@router.get("/download_all_company_quizzes")
async def get_all_company_quiz_result(
        company_id: int,
        current_user: PublicUser = Depends(get_current_user),
        comp: CompanyRepository = Depends(get_company_repository)
        ) -> FileResponse:
    company = await comp.get_by_id_company(id=company_id)
    admin = await comp.get_company_admin(company_id=company_id, user_id=int(current_user.id))
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company is not found or you are not owner")
    if company.user_id != int(current_user.id):
        if admin:
            return FileResponse(path=file_path, filename=f'{company.title} answers')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not company owner or admin")
    key = f"{company_id}*"
    get_all_csv_file_redis(key=key)
    return FileResponse(path=file_path, filename=f'{company.title} answers')
