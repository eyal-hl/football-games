from sqlalchemy.orm import Mapped, mapped_column
from models.base import SQLModel


class LeagueModel(SQLModel):
    __tablename__ = "leagues"

    league_id: Mapped[str] = mapped_column("league_id", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    ref: Mapped[str] = mapped_column("ref")
    img_ref: Mapped[str] = mapped_column("img_ref")
