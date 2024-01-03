from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from backend.session import create_session

router = APIRouter(prefix="/grid")


@router.get("/all_answers", response_model=str)
async def get_all_answers(session: Session = Depends(create_session)):
    return "hmmm"

@router.get("/is_currect", response_model=bool)
async def get_is_currect():
    return "hmmm"