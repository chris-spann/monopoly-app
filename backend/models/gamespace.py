from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import GameSpaceType, PropertyGroup
from models.base import Base
from models.deed import Deed


class GameSpace(Base):
    __tablename__ = "gamespaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    value: Mapped[int] = mapped_column(Integer)
    type: Mapped["GameSpaceType"] = mapped_column(String(50))
    group: Mapped["PropertyGroup"] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable=True)

    owner = relationship("Player", back_populates="properties")
    deed: Mapped["Deed"] = relationship()
