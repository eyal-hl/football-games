from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.session import create_session
from schemas.players import PlayerSchema, PlayersSlimSchema
from services.players import PlayerService

router = APIRouter(prefix="/players")


@router.get("/search", response_model=List[PlayersSlimSchema])
async def search_players(
        name: str = '', nationality: str = '', session: Session = Depends(create_session)
) -> List[PlayerSchema]:
    return PlayerService(session).search_players(name=name, nationality=nationality)

@router.get("/nationalities", response_model=List[str])
async def get_nationalities(
        session: Session = Depends(create_session)
) -> List[PlayerSchema]:
    return PlayerService(session).get_nationalities()

@router.get("/{player_id}", response_model=PlayerSchema)
async def get_player(
        player_id: int, session: Session = Depends(create_session)
) -> PlayerSchema:
    return PlayerService(session).get_player(player_id)


@router.get("/", response_model=List[PlayerSchema])
async def get_players(
        session: Session = Depends(create_session)
) -> List[PlayerSchema]:
    return PlayerService(session).get_players()



