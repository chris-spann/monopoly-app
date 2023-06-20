from models.base import Base
from sqlalchemy import Column, Integer, String


class Deed(Base):
    __tablename__ = "deeds"

    id = Column(Integer, primary_key=True, index=True)
    deed_type = Column(String)
    rent = Column(Integer)
    rent_group = Column(Integer)
    rent_1_house = Column(Integer)
    rent_2_houses = Column(Integer)
    rent_3_houses = Column(Integer)
    rent_4_houses = Column(Integer)
    rent_hotel = Column(Integer)
    house_cost = Column(Integer)
    hotel_cost = Column(Integer)
