from constants import GameSpaceType
from models.base import Base
from models.deed import Deed
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class GameSpace(Base):
    __tablename__ = "gamespaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    value = Column(Integer)
    type: Mapped[GameSpaceType] = mapped_column(String(50))
    group = Column(String, nullable=True)
    status = mapped_column(String(50))
    owner_id = Column(Integer, ForeignKey("players.id"))

    owner = relationship("Player", back_populates="properties")
    deed: Mapped["Deed"] = relationship()
