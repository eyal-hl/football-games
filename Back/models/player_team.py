from sqlalchemy.orm import Mapped, mapped_column
from models.base import SQLModel


class PlayerTeamModel(SQLModel):
    __tablename__ = "playerTeam"

    player_id: Mapped[int] = mapped_column("player_id", primary_key=True)
    team_id: Mapped[str] = mapped_column("team_id", primary_key=True)
    year: Mapped[int] = mapped_column("year", primary_key=True)
    player_number: Mapped[int] = mapped_column("player_number")
    age_at_club: Mapped[int] = mapped_column("age_at_club")
    position: Mapped[str] = mapped_column("position")
