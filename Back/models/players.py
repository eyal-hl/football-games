from sqlalchemy.orm import Mapped, mapped_column
from models.base import SQLModel
from datetime import date


class PlayerModel(SQLModel):
    __tablename__ = "players"

    player_id: Mapped[int] = mapped_column("player_id", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    ref: Mapped[str] = mapped_column("ref")
    img_ref: Mapped[str] = mapped_column("img_ref")
    nationality: Mapped[str] = mapped_column("nationality")
    birth_date: Mapped[date] = mapped_column("birth_date")
    name_unaccented: Mapped[str] = mapped_column("name_unaccented")
