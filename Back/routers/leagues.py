from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.leagues import LeagueSchema
from services.leagues import LeagueService

router = APIRouter(prefix="/leagues")


@router.get("/{league_id}", response_model=LeagueSchema)
async def get_league(
        league_id: str, session: Session = Depends(create_session)
) -> LeagueSchema:
    return LeagueService(session).get_league(league_id)


@router.get("/", response_model=List[LeagueSchema])
async def get_leagues(
        session: Session = Depends(create_session)
) -> List[LeagueSchema]:
    return LeagueService(session).get_leagues()
