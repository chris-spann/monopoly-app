from models.base import Base
from sqlalchemy import Boolean, Column, Integer, String, Text


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    type = Column(String(50))
    is_gooj = Column(Boolean, default=False)
