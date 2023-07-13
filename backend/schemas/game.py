import itertools
import random

import click
import requests
from pydantic import BaseModel, ConfigDict
from schemas.card import Card
from schemas.constants import CardType, GameSpaceType, PayType, PropertyStatus, RollResultCode
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

    def get_gamespaces(self):
        response = requests.get("http://localhost:8000/gamespaces/").json()
        for space in response:
            self.add_space(GameSpaceGame(**space))

    def add_player(self, player: PlayerCreate) -> None:
        try:
            res = requests.post(f"http://localhost:8000/players/?name={player.name}")
            self.players.append(Player(**res.json()))
        except Exception as e:
            click.echo("Error adding player:")
            click.echo(e)

    def add_players(self):
        num_players = click.prompt("How many players?", type=int)
        for i in range(num_players):
            name = click.prompt("Enter player name", type=str)
            self.add_player(PlayerCreate(name=name))
        print(self.players)

    def add_card(self, card: Card) -> None:
        if card.type == CardType.CHANCE:
            self.chance_cards.append(card)
        else:
            self.cc_cards.append(card)

    def shuffle_cards(self):
        random.shuffle(self.cc_cards)
        random.shuffle(self.chance_cards)
        click.echo("cards shuffled")
        return self

    def get_cards(self):
        response = requests.get("http://localhost:8000/cards/").json()
        for card in response:
            self.add_card(Card(**card))
        self.shuffle_cards()

    def draw_card(self, card_type: CardType) -> Card:
        return self.chance_cards[0] if card_type == CardType.CHANCE else self.cc_cards[0]

    def jail_player(self, player: Player) -> None:
        player.go_to_jail(self.jail_index)

    def jail_visit_player(self, player: Player) -> None:
        player.go_to_jail(jail_index=self.jail_index, jail_count=0, in_jail=False)

    def handle_rent_payment(self, payer: Player, payee: Player, rent: int):
        if click.confirm(
            f"{payee.name}, Want to charge {payer.name} ${rent} rent?",
            abort=True,
        ):
            payer.pay(rent, PayType.RENT)
            payee.cash += rent

    def post_move_action(self, new_space: GameSpaceGame, player: Player) -> None:
        if new_space.type == GameSpaceType.GO_TO_JAIL:
            click.echo("Going to jail...")
            self.jail_player(player)
        # TODO: implement drawing of card
        if new_space.type in [GameSpaceType.DRAW_CHANCE, GameSpaceType.DRAW_CHEST]:
            if new_space.type == GameSpaceType.DRAW_CHANCE:
                click.echo("Draw a chance card")
                card = self.chance_cards.pop(0)
            else:
                card = self.cc_cards.pop(0)
            if not card.is_gooj:
                self.add_card(card)
            player.handle_draw_card(card)
        if new_space.type == GameSpaceType.TAX:
            player.pay(new_space.value, PayType.TAX)
        if new_space.type == GameSpaceType.TAX_INCOME:
            player.pay_income_tax()
        # TODO: if property is owned, determine the rent amount and pay it
        if (
            new_space.type in [GameSpaceType.PROPERTY, GameSpaceType.RAILROAD]
            and new_space.status == PropertyStatus.OWNED
            and new_space.owner != player
        ):
            click.echo(f"property is owned by {new_space.owner}. Please pay 1 million dollars.")
            self.handle_rent_payment(player, new_space.owner, new_space.get_rent())
        if (
            new_space.type in [GameSpaceType.PROPERTY, GameSpaceType.RAILROAD]
            and new_space.status == PropertyStatus.VACANT
        ) and click.confirm(f"Property is vacant. Purchase for ${new_space.value}?"):
            if player.cash >= new_space.value:
                new_space.owner = player
                new_space.status = PropertyStatus.OWNED
                player.cash -= new_space.value
            else:
                click.echo("Sorry, not enough cash.")

    def play(self) -> None:
        self.no_cash_players = 0
        list_buff = itertools.cycle(self.players)
        for player in list_buff:
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
        click.echo(f"player: {player.name}'s turn")
        starting_space = self.spaces[player.position]
        click.echo(f"player: {player.name} started on {starting_space}")
        roll_result = player.roll()
        # roll result == 98 when 3 consecutive doubles, go to jail
        if roll_result == RollResultCode.THIRD_DOUBLE:
            click.echo("3rd consecutive double, go to jail, fool!")
            self.jail_player(player)
            return
        if roll_result == RollResultCode.JAIL_DOUBLE:
            click.echo("Rolled a double while in jail, now just visiting.")
            self.jail_visit_player(player)
            return
        click.echo(f"rolled: {roll_result}")
        # if player passes or lands on GO, add 200 to their cash
        if player.position + roll_result >= len(self.spaces):
            player.cash += 200
            click.echo("passed go, added $200")
        player.position = (player.position + roll_result) % len(self.spaces)
        new_space = self.spaces[player.position]
        click.echo(f"player: {player.name} landed on {new_space}")
        self.post_move_action(new_space, player)
        return
