from models import GameSpace
from models.base import Base
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    cash: Mapped[int] = mapped_column(Integer)
    position: Mapped[int] = mapped_column(Integer)
    in_jail: Mapped[bool] = mapped_column(Boolean)
    roll_1: Mapped[bool] = mapped_column(Boolean, default=False)
    roll_2: Mapped[bool] = mapped_column(Boolean, default=False)
    roll_3: Mapped[bool] = mapped_column(Boolean, default=False)
    jail_count: Mapped[int] = mapped_column(Integer, default=0)

    properties: Mapped[list["GameSpace"]] = relationship(back_populates="owner")
    # gooj_cards = relationship("Card", back_populates="owner")
