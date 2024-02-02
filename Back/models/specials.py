from sqlalchemy.orm import Mapped, mapped_column
from models.base import SQLModel


class SpecialsModel(SQLModel):
    __tablename__ = "specials"

    special_id: Mapped[str] = mapped_column("special_id", primary_key=True)
    name: Mapped[str] = mapped_column("name")
    ref: Mapped[str] = mapped_column("ref")
    img_ref: Mapped[str] = mapped_column("img_ref")
    type: Mapped[str] = mapped_column("type")
