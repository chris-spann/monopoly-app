from typing import Any

from pydantic import BaseModel, ConfigDict
from schemas.constants import GameSpaceType, PropertyGroup, PropertyStatus
from schemas.deed import PropertyDeed


class GameSpaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    value: int
    type: GameSpaceType
    group: PropertyGroup | None
    status: PropertyStatus


class GameSpaceUpdate(GameSpaceBase):
    status: str
    owner_id: int | None


class GameSpace(GameSpaceBase):
    id: int | None
    owner_id: int | None
    deed: PropertyDeed | None

    def get_rent(self):
        rent = 0
        if not self.deed:
            return rent
        if self.status == PropertyStatus.VACANT:
            rent = 0
        if self.status == PropertyStatus.OWNED:
            rent = self.deed.rent
        if self.status == PropertyStatus.OWNED_1_HOUSE:
            rent = self.deed.rent_1_house
        if self.status == PropertyStatus.OWNED_2_HOUSES:
            rent = self.deed.rent_2_houses
        if self.status == PropertyStatus.OWNED_3_HOUSES:
            rent = self.deed.rent_3_houses
        if self.status == PropertyStatus.OWNED_4_HOUSES:
            rent = self.deed.rent_4_houses
        if self.status == PropertyStatus.OWNED_HOTEL:
            rent = self.deed.rent_hotel
        return rent


class GameSpaceGame(GameSpace):
    owner: Any = None
