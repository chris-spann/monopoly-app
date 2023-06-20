from pydantic import BaseModel


class BaseDeed(BaseModel):
    deed_type: str
    rent: int

    class Config:
        orm_mode = True


class PropertyDeed(BaseDeed):
    id: int
    deed_type = "property"
    rent_group: int
    rent_1_house: int
    rent_2_houses: int
    rent_3_houses: int
    rent_4_houses: int
    rent_hotel: int
    house_cost: int
    hotel_cost: int


class RailRoadDeed(BaseDeed):
    deed_type = "railroad"
    rent = 25
    rent_2: int = 50
    rent_3: int = 100
    rent_4: int = 200
