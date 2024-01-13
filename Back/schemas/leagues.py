from pydantic import BaseModel


class LeagueSchema(BaseModel):
    league_id: str
    name: str
    img_ref: str
