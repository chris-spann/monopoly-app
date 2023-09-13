from typing import Any

import requests
from constants import GameSpaceType, PropertyGroup, PropertyStatus
from pydantic import BaseModel, ConfigDict
from schemas.deed import PropertyDeed


class GameSpaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    value: int
    type: GameSpaceType
    group: PropertyGroup
    status: PropertyStatus


class GameSpaceUpdate(GameSpaceBase):
    status: str
    owner_id: int | None


class GameSpace(GameSpaceBase):
    id: int | None
    owner_id: int | None
    deed: PropertyDeed | None = None

    def get_property_rent(self):
        if self.deed is None:
            return 0
        match self.status:
            case PropertyStatus.VACANT:
                rent = 0
            case PropertyStatus.OWNED:
                rent = self.deed.rent
                prop_group = requests.get(
                    f"http://localhost:8000/gamespaces/group/{self.group.value}"
                ).json()
                if all(p.get("owner_id") == self.owner_id for p in prop_group):
                    rent = self.deed.rent_group
            case PropertyStatus.OWNED_1_HOUSE:
                rent = self.deed.rent_1_house
            case PropertyStatus.OWNED_2_HOUSES:
                rent = self.deed.rent_2_houses
            case PropertyStatus.OWNED_3_HOUSES:
                rent = self.deed.rent_3_houses
            case PropertyStatus.OWNED_4_HOUSES:
                rent = self.deed.rent_4_houses
            case PropertyStatus.OWNED_HOTEL:
                rent = self.deed.rent_hotel
            case _:
                rent = 0
        return rent


class GameSpaceGame(GameSpace):
    owner: Any = None
    # deed: PropertyDeed | None = None
