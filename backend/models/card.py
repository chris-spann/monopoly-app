from models.base import Base
from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(50))
    is_gooj: Mapped[bool] = mapped_column(Boolean, default=False)
