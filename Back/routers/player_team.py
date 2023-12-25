from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.player_team import PlayerTeamSchema, PlayerTeamHumanSchema
from services.player_team import PlayerTeamService

router = APIRouter(prefix="/player_teams")


@router.get("/", response_model=PlayerTeamSchema)
async def get_player(
        player_id: int, session: Session = Depends(create_session)
) -> PlayerTeamSchema:
    return PlayerTeamService(session).get_playerTeam(player_id)


@router.get("/search", response_model=List[PlayerTeamSchema])
async def search_players(
        name: str = '', nationality: str = '', year: str = '%', player_number: str = '%', age_at_club: str = '%',
        position: str = '%', team: str = '',
        session: Session = Depends(create_session)

) -> List[PlayerTeamSchema]:
    return PlayerTeamService(session).search_playerTeams(name=name, nationality=nationality, year=year, player_number=player_number,
                                                         age_at_club=age_at_club, position=position,
                                                         team=team)
