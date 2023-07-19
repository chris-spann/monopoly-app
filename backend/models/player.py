from models.base import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import mapped_column, relationship


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    cash = mapped_column(Integer)
    position = Column(Integer)
    in_jail = Column(Boolean)
    roll_1 = Column(Boolean, default=False)
    roll_2 = Column(Boolean, default=False)
    roll_3 = Column(Boolean, default=False)
    jail_count = Column(Integer, default=0)

    properties = relationship("GameSpace", back_populates="owner")
    # gooj_cards = relationship("Card", back_populates="owner")
