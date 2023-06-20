from pydantic import BaseModel
from schemas.card import Card
from schemas.gamespace import GameSpace


class PlayerBase(BaseModel):
    name: str
    position: int = 0
    cash: int = 1500
    in_jail: bool = False
    jail_count: int = 0
    properties: list[GameSpace] = []
    roll_1: bool = False
    roll_2: bool = False
    roll_3: bool = False


class Player(PlayerBase):
    id: int | None

    class Config:
        orm_mode = True


class PlayerCreate(PlayerBase):
    name: str


class PlayerUpdate(Player):
    name: str | None
    position: int | None
    cash: int | None
    in_jail: bool | None
    jail_count: int | None
    roll_1: bool | None
    roll_2: bool | None
    roll_3: bool | None
    gooj_cards: list[Card] | None
