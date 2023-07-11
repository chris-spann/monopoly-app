from random import randint

from pydantic import BaseModel, ConfigDict
from schemas.card import Card
from schemas.constants import RollResultCodes
from schemas.gamespace import GameSpace


class PlayerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    prev_double: list[bool] = [False, False, False]

    def roll_die(self) -> tuple[int, int]:
        return randint(1, 6), randint(1, 6)

    def roll(self) -> int:
        roll_1, roll_2 = self.roll_die()
        self.prev_double.pop(0)
        if roll_1 == roll_2:
            self.prev_double.append(True)
            if self.in_jail:
                return RollResultCodes.JAIL_DOUBLE.value
            if all(self.prev_double):
                return RollResultCodes.THIRD_DOUBLE.value
        else:
            self.prev_double.append(False)
            if self.in_jail and self.jail_count > 0:
                self.jail_count -= 1
                return 0
        return roll_1 + roll_2


class PlayerCreate(PlayerBase):
    name: str


class PlayerUpdate(Player):
    position: int | None
    cash: int | None
    in_jail: bool | None
    jail_count: int | None
    roll_1: bool | None
    roll_2: bool | None
    roll_3: bool | None
    gooj_cards: list[Card] | None
