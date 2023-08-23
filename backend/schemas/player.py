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

    def __str__(self) -> str:
        prop_repr = ", ".join(f"{prop.name}" for prop in self.properties)
        return f"Cash: ${self.cash}, Properties: [{prop_repr}]"

    def roll_die(self) -> tuple[int, int]:
        return randint(1, 6), randint(1, 6)

    def roll(self) -> int:
        die_1, die_2 = self.roll_die()
        self.prev_double.pop(0)
        if die_1 == die_2:
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
        return die_1 + die_2

    # TODO: Move pay to game module...
    # function should take in payer/payee as argument,
    # should be bank when purchasing property
    def pay(self, amount: int, reason: PayType) -> int:
        if amount >= self.cash:
            self.cash = 0
        else:
            self.cash -= amount
        click.echo(f"{self.name} paid ${amount} for {reason}")
        return self.cash

    def pay_income_tax(self) -> None:
        click.echo("You must pay either $200 or 10% of your total cash.")
        if (
            click.prompt(
                click.style(text="Enter 1 to pay $200 or 2 to pay 10%", fg="yellow"), type=int
            )
            == 1
        ):
            self.pay(200, PayType.INCOME_TAX)
        else:
            self.pay(self.cash // 10, PayType.INCOME_TAX)

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
