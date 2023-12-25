from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.players import PlayerSchema
from services.players import PlayerService

router = APIRouter(prefix="/players")


@router.get("/", response_model=PlayerSchema)
async def get_player(
        player_id: int, session: Session = Depends(create_session)
) -> PlayerSchema:
    return PlayerService(session).get_player(player_id)


@router.get("/all", response_model=List[PlayerSchema])
async def get_players(
        session: Session = Depends(create_session)
) -> List[PlayerSchema]:
    return PlayerService(session).get_players()


@router.get("/search", response_model=List[PlayerSchema])
async def search_players(
        name: str, session: Session = Depends(create_session)
) -> List[PlayerSchema]:
    return PlayerService(session).search_players(name)
