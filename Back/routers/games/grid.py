from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from backend.session import create_session
from services.games.grid import GridService
from schemas.players import PlayersSlimSchema
from typing import List
from const import POSSIBLE_GRID_TYPES

router = APIRouter(prefix="/grid")


@router.get("/all_answers", response_model=List[PlayersSlimSchema])
async def get_all_answers(type1:str, value1:str, type2:str, value2:str,
                          session: Session = Depends(create_session)):
    if type1 not in POSSIBLE_GRID_TYPES or type2 not in POSSIBLE_GRID_TYPES:
        raise HTTPException(status_code=400, detail="Type not found")
    if type1 == type2 == "nationality":
        raise HTTPException(status_code=400, detail="Player cant have 2 nationalities")

        return []
    return await GridService(session).all_answers(type1=type1, value1=value1, type2=type2, value2=value2)


@router.get("/is_currect", response_model=bool)
async def get_is_currect(player_id: int,type1:str, value1:str, type2:str, value2:str,
                         session: Session = Depends(create_session)):
    if player_id is None:
        raise HTTPException(status_code=400, detail="No player_id")
    a = await GridService(session).all_answers(type1=type1, value1=value1, type2=type2, value2=value2)
    return player_id in list(map(lambda player: player.__dict__['player_id'], a))
