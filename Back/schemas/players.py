from pydantic import BaseModel
from datetime import date
from typing import Optional


class PlayerSchema(BaseModel):
    player_id: int
    name: str
    ref: str
    img_ref: str
    nationality: Optional[str]
    birth_date: Optional[date]
    name_unaccented: str


class PlayersSlimSchema(BaseModel):
    player_id: int
    name: str
    name_unaccented: str
    birth_date: Optional[date]
    img_ref: str
