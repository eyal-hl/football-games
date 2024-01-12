from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from backend.session import create_session
from schemas.players import PlayersSlimSchema
from schemas.player_team import PlayerTeamSchema
from schemas.teams import ConnectionSchema
from typing import List
from services.games.connect_players import connectedPlayersService

router = APIRouter(prefix="/connect_players")


@router.get("/path", response_model=List[PlayersSlimSchema])
async def get_path(team1='', team2='', nationality='', league1='', league2='',
                          session: Session = Depends(create_session)):
    return connectedPlayersService(session).get_path(team1=team1, team2=team2, nationality=nationality, league1=league1,
                                            league2=league2)


@router.get("/connection_details", response_model=List[ConnectionSchema])
async def get_connection_details(player1: int = 0, player2:int = 0,
                         session: Session = Depends(create_session)):
    return connectedPlayersService(session).get_connection_details(player1=player1, player2=player2)
