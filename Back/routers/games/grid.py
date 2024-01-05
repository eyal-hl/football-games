from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from backend.session import create_session
from services.games.grid import GridService
from schemas.players import PlayersSlimSchema
from typing import List

router = APIRouter(prefix="/grid")


@router.get("/all_answers", response_model=List[PlayersSlimSchema])
async def get_all_answers(team1='', team2='', nationality='', league1='', league2='',
                          session: Session = Depends(create_session)):
    return GridService(session).all_answers(team1=team1, team2=team2, nationality=nationality, league1=league1,
                                            league2=league2)


@router.get("/is_currect", response_model=bool)
async def get_is_currect(player_id: int, team1='', team2='', nationality='', league1='', league2='',
                         session: Session = Depends(create_session)):
    if player_id is None:
        return False
    a = GridService(session).all_answers(team1=team1, team2=team2, nationality=nationality, league1=league1,
                                         league2=league2)
    return player_id in list(map(lambda player: player.__dict__['player_id'], a))
