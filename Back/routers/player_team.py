from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.player_team import PlayerTeamSchema, CombinedPlayerTeamSchema
from services.player_team import PlayerTeamService

router = APIRouter(prefix="/player_teams")


@router.get("/advanced_search", response_model=List[CombinedPlayerTeamSchema])
async def search_players(
        name: str = '', nationality: str = '', year: str = '', player_number: str = '', age_at_club: str = '',
        position: str = '', team: str = '', team_id: str = '', league: str = '', league_id: str = '',
        session: Session = Depends(create_session)
) -> List[CombinedPlayerTeamSchema]:
    return PlayerTeamService(session).search_playerTeams(name=name, nationality=nationality, year=year,
                                                         player_number=player_number,
                                                         age_at_club=age_at_club, position=position,
                                                         team=team, team_id=team_id, league=league, league_id=league_id)


@router.get("/{player_id}", response_model=List[PlayerTeamSchema])
async def get_player(
        player_id: int, session: Session = Depends(create_session)
) -> List[PlayerTeamSchema]:
    return PlayerTeamService(session).get_playerTeam(player_id)
