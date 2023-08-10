from random import randint

import click
from constants import CardType, PayType, RollResultCode
from pydantic import BaseModel, ConfigDict
from schemas.card import Card
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
                return RollResultCode.JAIL_DOUBLE
            if all(self.prev_double):
                return RollResultCode.THIRD_DOUBLE
        else:
            self.prev_double.append(False)
            if self.in_jail and self.jail_count > 0:
                self.jail_count -= 1
                return 0
        return roll_1 + roll_2

    def pay(self, amount: int, reason: PayType) -> None:
        if amount >= self.cash:
            self.cash = 0
        else:
            self.cash -= amount
        click.echo(f"{self.name} paid ${amount} for {reason}")

    def pay_income_tax(self) -> None:
        click.echo(
            f"You must pay either $200 or 10% of your total cash. (current cash: ${self.cash})"
        )
        click.echo("Enter 1 to pay $200 or 2 to pay 10%")
        if click.prompt("Enter 1 or 2", type=int) == 1:
            self.pay(200, PayType.INCOME_TAX)
        else:
            self.pay(self.cash // 10, PayType.INCOME_TAX)

    def go_to_jail(self, jail_index: int, jail_count=3, in_jail=True):
        self.in_jail = in_jail
        self.jail_count = jail_count
        self.position = jail_index

    def handle_draw_card(self, card: Card):
        if card.is_gooj:
            click.echo("Drew a get out of jail free card!")
            return
            # TODO: call update player endpoint
            # player.add_gooj_card(card)

        if card.type == CardType.CHANCE:
            click.echo("Drew a chance card!")
            click.echo(card.title)
        if card.type == CardType.COMMUNITY_CHEST:
            click.echo("Drew a community chest card!")
            click.echo(card.title)


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
