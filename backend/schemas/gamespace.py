from pydantic import BaseModel

# from app.schemas.player import Player
from schemas.deed import PropertyDeed


class GameSpaceBase(BaseModel):
    name: str
    value: int
    type: str
    group: str | None
    status: str

    # owner: Player | None = None


class GameSpaceCreate(GameSpaceBase):
    name: str
    value: int
    type: str
    group: str | None
    status: str = "vacant"
    owner_id: int | None = None


class GameSpace(GameSpaceBase):
    id: int | None
    owner_id: int | None
    deed: PropertyDeed | None  # type: ignore
    # owner: Player | None = None

    class Config:
        orm_mode = True
