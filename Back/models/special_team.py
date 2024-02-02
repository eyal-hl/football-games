from sqlalchemy.orm import Mapped, mapped_column
from models.base import SQLModel


class SpecialTeamModel(SQLModel):
    __tablename__ = "specialTeam"

    special_id: Mapped[str] = mapped_column("special_id", primary_key=True)
    team_id: Mapped[str] = mapped_column("team_id", primary_key=True)
    year: Mapped[int] = mapped_column("year", primary_key=True)
