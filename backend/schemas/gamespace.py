from typing import Any

from pydantic import BaseModel, ConfigDict
from schemas.deed import PropertyDeed


class GameSpaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    value: int
    type: str
    group: str | None
    status: str


class GameSpaceUpdate(GameSpaceBase):
    status: str
    owner_id: int | None


class GameSpace(GameSpaceBase):
    id: int | None
    owner_id: int | None
    deed: PropertyDeed | None


class GameSpaceGame(GameSpaceBase):
    owner: Any = None
