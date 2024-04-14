from pydantic import BaseModel
from typing import List


class TeamSchema(BaseModel):
    name: str
    league_id: str
    ref: str
    team_id: str
    img_ref: str


class ConnectionSchema(BaseModel):
    team_name: str
    years: str


class MassConnectionSchema(BaseModel):
    player_id: int
    connections: List[ConnectionSchema]
