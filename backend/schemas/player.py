from random import randint

import click
import requests
from constants import PayType, RollResultCode
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
    id: int

    def __str__(self) -> str:
        p_str = f"Cash: ${self.cash}"
        self.properties.sort(key=lambda x: x.id if x.id is not None else 0)
        if len(self.properties) > 0:
            p_str += ", Properties(group): "
            p_str += f"[{', '.join(f'{prop.name}({prop.group})' for prop in self.properties)}]"
        return p_str

    def roll_db_handler(self, is_double: bool, jail_count: int):
        self.roll_1 = self.roll_2
        self.roll_2 = self.roll_3
        self.roll_3 = is_double

        requests.patch(
            f"http://localhost:8000/player/{self.id}",
            json={
                "roll_1": self.roll_1,
                "roll_2": self.roll_2,
                "roll_3": self.roll_3,
                "jail_count": jail_count,
            },
        )

    def roll_die(self) -> tuple[int, int]:
        return randint(1, 6), randint(1, 6)

    def roll(self) -> int:
        is_double = False
        if self.roll_3:
            click.secho(
                message=f"Consecutive Doubles: "
                f"{[self.roll_1, self.roll_2, self.roll_3].count(True)}"
            )
        if self.jail_count > 0:
            click.secho(message=f"Jail Turns Remaining: {self.jail_count}")
        die_1, die_2 = self.roll_die()
        click.secho(message=f"\n{self.name} rolled a {die_1} and a {die_2}!", fg="blue")
        if die_1 == die_2:
            is_double = True
            if self.in_jail:
                self.roll_db_handler(is_double, self.jail_count)
                return RollResultCode.JAIL_DOUBLE
            if all([self.roll_2, self.roll_3, is_double]):
                self.roll_db_handler(is_double, self.jail_count)
                return RollResultCode.THIRD_DOUBLE
        elif self.in_jail and self.jail_count > 0:
            self.jail_count -= 1
            self.roll_db_handler(is_double, self.jail_count)
            return 0
        self.roll_db_handler(is_double, self.jail_count)
        return die_1 + die_2

    def pay(self, amount: int, reason: PayType) -> int:
        if amount >= self.cash:
            self.cash = 0
        else:
            self.cash -= amount
        click.secho(message=f"{self.name} paid ${amount} for {reason.capitalize()}\n", fg="red")
        requests.patch(f"http://localhost:8000/player/{self.id}", json={"cash": self.cash})
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
            click.secho(message="Drew a get out of jail free card!", fg="bright_green")
            return
            # TODO: call update player endpoint
            # player.add_gooj_card(card)
        click.secho(message="The card says:")
        click.secho(message=card.title, fg="magenta")
        card.action(self.id)


class PlayerCreate(PlayerBase):
    name: str
