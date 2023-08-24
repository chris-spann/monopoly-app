from constants import GameSpaceType
from models.base import Base
from models.deed import Deed
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class GameSpace(Base):
    __tablename__ = "gamespaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    value: Mapped[int] = mapped_column(Integer)
    type: Mapped["GameSpaceType"] = mapped_column(String(50))
    group: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))

    owner = relationship("Player", back_populates="properties")
    deed: Mapped["Deed"] = relationship()
