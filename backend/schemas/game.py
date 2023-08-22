import itertools
import random
from time import sleep

import click
import requests
from constants import (
    PASS_GO_AMOUNT,
    CardType,
    GameSpaceType,
    PayType,
    PropertyStatus,
    RollResultCode,
)
from pydantic import BaseModel, ConfigDict
from schemas.card import Card
from schemas.gamespace import GameSpaceGame
from schemas.player import Player, PlayerCreate


class Game(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    spaces: list[GameSpaceGame] = []
    players: list[Player] = []
    chance_cards: list[Card] = []
    cc_cards: list[Card] = []
    jail_index: int = 0
    no_cash_players: int = 0

    def add_space(self, space: GameSpaceGame) -> None:
        self.spaces.append(space)
        if space.type == GameSpaceType.JAIL:
            self.jail_index = len(self.spaces) - 1

    def add_card(self, card: Card) -> None:
        if card.type == CardType.CHANCE:
            self.chance_cards.append(card)
        else:
            self.cc_cards.append(card)

    def add_player(self, player: PlayerCreate) -> None:
        try:
            res = requests.post(f"http://localhost:8000/players/?name={player.name}")
            self.players.append(Player(**res.json()))
        except Exception as e:
            click.echo("Error adding player:")
            click.echo(e)

    def setup_players(self):
        num_players = click.prompt("How many players?", type=int)
        for i in range(num_players):
            name = click.prompt("Enter player name", type=str)
            self.add_player(PlayerCreate(name=name))
        click.clear()
        click.confirm("Ready to play?", abort=True)
        click.clear()

    def get_gamespaces(self):
        response = requests.get("http://localhost:8000/gamespaces/").json()
        for space in response:
            self.add_space(GameSpaceGame(**space))

    def get_cards(self):
        response = requests.get("http://localhost:8000/cards/").json()
        for card in response:
            self.add_card(Card(**card))
        random.shuffle(self.cc_cards)
        random.shuffle(self.chance_cards)
        click.echo("Cards shuffled!")
        return self

    def draw_card(self, card_type: CardType) -> Card:
        return self.chance_cards[0] if card_type == CardType.CHANCE else self.cc_cards[0]

    # def jail_player(self, player: Player, visit=False) -> None:
    #     update = {"position": self.jail_index}
    #     if visit:
    #         player.go_to_jail(jail_index=self.jail_index, jail_count=0, in_jail=False)
    #     else:
    #         player.go_to_jail(self.jail_index)
    #     print(update)

    def jail_player(self, player: Player, visit=False) -> None:
        update = {"position": self.jail_index}
        player.position = self.jail_index
        if visit:
            player.in_jail = False
            player.jail_count = 0
            update["in_jail"] = False
            update["jail_count"] = 0
            # player.go_to_jail(jail_index=self.jail_index, jail_count=0, in_jail=False)
        else:
            player.in_jail = True
            player.jail_count = 3
            update["in_jail"] = True
            update["jail_count"] = 3
            # player.go_to_jail(self.jail_index)

        requests.patch(f"http://localhost:8000/player/{player.id}", json=update)

    def get_utility_rent(
        self, space: GameSpaceGame, owner_id: int, roll_result: int
    ) -> requests.Response:
        response = requests.get(
            "http://localhost:8000/gamespaces/utility-rent/{space.id}/owner/{owner_id}/roll/{roll_result}"
        )
        click.echo(f"get_utility_rent response: {response.json()}")

        return response

    def handle_rent_payment(self, payer: Player, payee: Player, rent: int):
        if click.confirm(
            f"{payee.name}, Want to charge {payer.name} ${rent} rent?",
            abort=True,
        ):
            payer.pay(rent, PayType.RENT)
            payee.cash += rent
        else:
            return

    def move_player(self, player: Player, roll_result: int) -> None:
        # if player passes or lands on GO, add PASS_GO_AMOUNT to player's cash
        if player.position + roll_result >= len(self.spaces):
            player.cash += PASS_GO_AMOUNT
            click.echo(f"Passed go, added ${PASS_GO_AMOUNT}")
        player.position = (player.position + roll_result) % len(self.spaces)
        # update player position/cash in db
        click.echo(f"Updating player_id: {player.id}")
        requests.patch(
            f"http://localhost:8000/player/{player.id}",
            json={"position": player.position, "cash": player.cash},
        )

    def post_move_action(  # noqa: C901
        self, new_space: GameSpaceGame, player: Player, roll_result: int
    ) -> None:
        if new_space.type == GameSpaceType.GO_TO_JAIL:
            click.echo("Going to jail...")
            self.jail_player(player)
        if new_space.type in [GameSpaceType.DRAW_CHANCE, GameSpaceType.DRAW_CHEST]:
            if new_space.type == GameSpaceType.DRAW_CHANCE:
                card = self.chance_cards.pop(0)
            else:
                card = self.cc_cards.pop(0)
            # if card is not a get out of jail card, return it to the end of the deck
            if not card.is_gooj:
                self.add_card(card)
            player.handle_draw_card(card)
        if new_space.type == GameSpaceType.TAX:
            player.pay(new_space.value, PayType.TAX)
        if new_space.type == GameSpaceType.TAX_INCOME:
            player.pay_income_tax()
        # TODO: if property is owned, determine the rent amount and pay it
        if (
            new_space.type in [GameSpaceType.PROPERTY]
            and new_space.status == PropertyStatus.OWNED
            and new_space.owner != player
        ):
            rent = new_space.get_property_rent()
            click.echo(f"Rent is ${rent} for {new_space.name}, owned by {new_space.owner.name}.")
            self.handle_rent_payment(player, new_space.owner, rent)
        if (
            new_space.type in [GameSpaceType.UTILITY, GameSpaceType.RAILROAD]
            and new_space.status == PropertyStatus.OWNED
            and new_space.owner != player
        ):
            owner = requests.get(f"http://localhost:8000/player/name/{new_space.owner.name}").json()
            click.echo(f"Owner: {owner}")
            rent = self.get_utility_rent(
                space=new_space, owner_id=owner["id"], roll_result=roll_result
            )
            rent = rent.json()
            click.echo(f"Rent is ${rent} for {new_space.name}, owned by {new_space.owner.name}.")
            self.handle_rent_payment(player, new_space.owner, rent)
        if (
            new_space.type
            in [GameSpaceType.PROPERTY, GameSpaceType.UTILITY, GameSpaceType.RAILROAD]
            and new_space.status == PropertyStatus.VACANT
        ) and click.confirm(
            f"{new_space.type.capitalize()} is vacant. Purchase for ${new_space.value}?"
        ):
            if player.cash >= new_space.value:
                new_space.owner = player
                new_space.status = PropertyStatus.OWNED
                player.cash -= new_space.value
                requests.post(
                    f"http://localhost:8000/player/{player.id}/add-property/{new_space.id}"
                )
                click.echo(f"{player.name} purchased {new_space.name} for ${new_space.value}.")
            else:
                click.echo("Sorry, not enough cash.")
        sleep(1)

    def play(self) -> None:
        self.no_cash_players = 0
        list_buff = itertools.cycle(self.players)
        for p in list_buff:
            response = requests.get(f"http://localhost:8000/player/{p.id}").json()
            player = Player(**response)
            click.echo(f"player: {player}")
            if player.cash == 0:
                self.no_cash_players += 1
                click.echo(f"player: {player.name} is out of cash")
                if self.no_cash_players == len(self.players):
                    click.echo("game over, no players with cash")
                    break
                continue
            self.player_turn(player)
            click.echo("----------")

    def player_turn(self, player: Player):
        click.echo(f"{player.name}'s turn:")
        sleep(0.5)
        roll_result = player.roll()
        # roll result == 98 when 3 consecutive doubles, go to jail
        if roll_result == RollResultCode.THIRD_DOUBLE:
            click.echo("3rd consecutive double, go to jail, fool!")
            self.jail_player(player)
            return
        if roll_result == RollResultCode.JAIL_DOUBLE:
            click.echo("Rolled a double while in jail, now just visiting.")
            self.jail_player(player, visit=True)
            return
        click.echo(f"Roll result: {roll_result}")
        self.move_player(player, roll_result)
        new_space = self.spaces[player.position]
        click.echo(f"{player.name}'s resulting position: {new_space.name}\n")
        self.post_move_action(new_space, player, roll_result)
        return
