import time

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from backend.session import create_session
from schemas.players import PlayersSlimSchema
from schemas.player_team import PlayerTeamSchema
from schemas.teams import ConnectionSchema
from typing import List
from services.games.connect_players import connectedPlayersService
import asyncio

router = APIRouter(prefix="/connect_players")


@router.get("/path", response_model=List[PlayersSlimSchema])
async def get_path(player1: int, player2: int, players_to_ignore: str = '', teams_to_ignore: str = '',
                   session: Session = Depends(create_session)):
    players_to_ignore = ([int(player) for player in players_to_ignore.split(',')] if players_to_ignore else [])
    teams_to_ignore = teams_to_ignore.split(',') if teams_to_ignore else []
    return await asyncio.create_task(connectedPlayersService(session).get_path(player1=player1, player2=player2,
                                                     players_to_ignore=players_to_ignore,
                                                     teams_to_ignore=teams_to_ignore))


@router.get("/connection_details", response_model=List[ConnectionSchema])
async def get_connection_details(player1: int = 0, player2: int = 0,
                                 session: Session = Depends(create_session)):
    return await connectedPlayersService(session).get_connection_details(player1=player1, player2=player2)

