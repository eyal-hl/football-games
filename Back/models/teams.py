from sqlalchemy.orm import Mapped, mapped_column
from models.base import SQLModel


class TeamModel(SQLModel):
    __tablename__ = "teams"

    name: Mapped[str] = mapped_column("name", unique=True)
    league_id: Mapped[str] = mapped_column("league_id")
    ref: Mapped[str] = mapped_column("ref")
    team_id: Mapped[str] = mapped_column("team_id", primary_key=True, unique=True)
    img_ref: Mapped[str] = mapped_column("img_ref")