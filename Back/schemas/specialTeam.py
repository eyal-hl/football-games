from pydantic import BaseModel
from datetime import date
from typing import Optional


class SpecialTeamSchema(BaseModel):
    special_id: str
    team_id: str
    year: int