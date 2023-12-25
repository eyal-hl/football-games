from pydantic import BaseModel
from datetime import date
from typing import Optional


class PlayerTeamSchema(BaseModel):
    player_id: int
    team_id: str
    year: int
    player_number: Optional[int]
    age_at_club: Optional[int]
    position: Optional[str]


class PlayerTeamHumanSchema(BaseModel):
    team_id: str
    name: str
    year: int
    player_number: Optional[int]
    age_at_club: Optional[int]
    position: Optional[str]
    nationality: Optional[str]
    birth_date: Optional[date]

