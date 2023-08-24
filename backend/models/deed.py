from models.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Deed(Base):
    __tablename__ = "deeds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    deed_type: Mapped[str] = mapped_column(String)
    rent: Mapped[int] = mapped_column(Integer)
    rent_group: Mapped[int] = mapped_column(Integer)
    rent_1_house: Mapped[int] = mapped_column(Integer)
    rent_2_houses: Mapped[int] = mapped_column(Integer)
    rent_3_houses: Mapped[int] = mapped_column(Integer)
    rent_4_houses: Mapped[int] = mapped_column(Integer)
    rent_hotel: Mapped[int] = mapped_column(Integer)
    house_cost: Mapped[int] = mapped_column(Integer)
    hotel_cost: Mapped[int] = mapped_column(Integer)
    gamespace_id: Mapped[int] = mapped_column(Integer, ForeignKey("gamespaces.id"))
