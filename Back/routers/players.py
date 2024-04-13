from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.players import PlayerSchema, PlayersSlimSchema
from services.players import PlayerService

router = APIRouter(prefix="/players")


@router.get("/search", response_model=List[PlayersSlimSchema])
async def search_players(
        name: str = '', search_from_middle: bool = False, session: Session = Depends(create_session)
) -> List[PlayersSlimSchema]:
    return await PlayerService(session).search_players(name=name, search_from_middle=search_from_middle)


@router.get("/nationalities", response_model=List[str])
async def get_nationalities(
        session: Session = Depends(create_session)
) -> List[str]:
    return await PlayerService(session).get_nationalities()


@router.get("/{player_id}", response_model=PlayersSlimSchema)
async def get_player(
        player_id: int, session: Session = Depends(create_session)
) -> PlayersSlimSchema:
    return await PlayerService(session).get_player(player_id)


@router.get("/", response_model=List[PlayersSlimSchema])
async def get_players(
        session: Session = Depends(create_session)
) -> List[PlayersSlimSchema]:
    return await PlayerService(session).get_players()

@router.get("/league/{league_id}/{year}", response_model=List[PlayersSlimSchema])
async def get_players_by_league(
        league_id: str, year: int, session: Session = Depends(create_session)
) -> List[PlayersSlimSchema]:
    return await PlayerService(session).get_players_by_league(league_id, year)


@router.get("/team/{team_id}/{year}", response_model=List[PlayersSlimSchema])
async def get_players_by_team(
        team_id: str, year: int, session: Session = Depends(create_session)
) -> List[PlayersSlimSchema]:
    return await PlayerService(session).get_players_by_team(team_id, year)