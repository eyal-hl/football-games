# routers/teams.py

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.teams import TeamSchema
from services.teams import TeamService

router = APIRouter(prefix="/teams")


@router.get("/", response_model=List[TeamSchema])
async def get_teams(
        session: Session = Depends(create_session)
) -> List[TeamSchema]:
    return TeamService(session).get_teams()


@router.get("/{team_id}", response_model=TeamSchema)
async def get_team(
        team_id: str, session: Session = Depends(create_session)
) -> TeamSchema:
    return TeamService(session).get_team(team_id)


@router.get("/league/{league_id}", response_model=List[TeamSchema])
async def get_teams_by_league(
        league_id: str, session: Session = Depends(create_session)
) -> List[TeamSchema]:
    return TeamService(session).get_teams_by_league(league_id)
