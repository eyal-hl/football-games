# routers/teams.py

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.specials import SpecialSchema
from services.specials import SpecialService


router = APIRouter(prefix="/specials")


@router.get("/", response_model=List[SpecialSchema])
async def get_teams(
        session: Session = Depends(create_session)
) -> List[SpecialSchema]:
    return await SpecialService(session).get_specials()


@router.get("/{special_id}", response_model=SpecialSchema)
async def get_team(
        special_id: str, session: Session = Depends(create_session)
) -> SpecialSchema:
    return await SpecialService(session).get_special(special_id)


