import itertools
import random
from time import sleep

import click
import requests
from constants import (
    OWNABLE_SPACES,
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
        click.secho(message="Cards shuffled!", fg="magenta")
        return self

    def draw_card(self, card_type: CardType) -> Card:
        return self.chance_cards[0] if card_type == CardType.CHANCE else self.cc_cards[0]

    def jail_player(self, player: Player, visit=False) -> None:
        update = {"position": self.jail_index}
        player.position = self.jail_index
        if visit:
            player.in_jail = False
            player.jail_count = 0
            update["in_jail"] = False
            update["jail_count"] = 0
        else:
            player.in_jail = True
            player.jail_count = 3
            update["in_jail"] = True
            update["jail_count"] = 3
        requests.patch(f"http://localhost:8000/player/{player.id}", json=update)

    def get_utility_rent(
        self, space: GameSpaceGame, owner_id: int, roll_result: int
    ) -> requests.Response:
        return requests.get(
            f"http://localhost:8000/gamespaces/utility-rent/{space.id}/owner/{owner_id}/roll/{roll_result}"
        )

    def handle_rent_payment(self, payer: Player, payee: Player, rent: int):
        if click.confirm(
            click.style(
                text=f"{payee.name}, Want to charge {payer.name} ${rent} rent?", fg="yellow"
            ),
        ):
            new_payer_bal = payer.pay(rent, PayType.RENT)
            new_payee_cash = payee.cash + rent
            requests.patch(f"http://localhost:8000/player/{payer.id}", json={"cash": new_payer_bal})
            requests.patch(
                f"http://localhost:8000/player/{payee.id}", json={"cash": new_payee_cash}
            )
        else:
            click.echo("No rent paid.\n")
            return

    def move_player(self, player: Player, roll_result: int) -> Player:
        if player.position + roll_result >= len(self.spaces):
            player.cash += PASS_GO_AMOUNT
            click.secho(message=f"Passed go, added ${PASS_GO_AMOUNT}", fg="green", bold=True)
        player.position = (player.position + roll_result) % len(self.spaces)
        requests.patch(
            f"http://localhost:8000/player/{player.id}",
            json={"position": player.position, "cash": player.cash},
        )
        response = requests.get(f"http://localhost:8000/player/{player.id}").json()
        return Player(**response)

    def post_move_ownable(self, new_space: GameSpaceGame, player: Player, roll_result: int) -> None:
        if (
            new_space.type in [GameSpaceType.PROPERTY]
            and new_space.status == PropertyStatus.OWNED
            and new_space.owner.name != player.name
        ):
            rent = new_space.get_property_rent()
            click.echo(f"Rent is ${rent} for {new_space.name}, owned by {new_space.owner.name}.")
            self.handle_rent_payment(player, new_space.owner, rent)
        if (
            new_space.type in [GameSpaceType.UTILITY, GameSpaceType.RAILROAD]
            and new_space.status == PropertyStatus.OWNED
            and new_space.owner.name != player.name
        ):
            owner = requests.get(f"http://localhost:8000/player/name/{new_space.owner.name}").json()
            click.echo(f"Owner: {owner.get('name')}")
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
        ):
            if click.confirm(
                click.style(
                    text=f"{new_space.type.capitalize()} is vacant. "
                    f"Purchase for ${new_space.value}?",
                    fg="yellow",
                )
            ):
                if player.cash >= new_space.value:
                    new_space.owner = player
                    new_space.status = PropertyStatus.OWNED
                    # player.cash -= new_space.value
                    requests.post(
                        f"http://localhost:8000/player/{player.id}/add-property/{new_space.id}"
                    )
                    click.secho(
                        message=f"{player.name} purchased {new_space.name} "
                        f"for ${new_space.value}.\n",
                        fg="red",
                    )
                else:
                    click.echo("Sorry, not enough cash.")
            else:
                click.echo("No purchase made.\n")

    def post_move_action(self, new_space: GameSpaceGame, player: Player, roll_result: int) -> None:
        if new_space.type in OWNABLE_SPACES:
            self.post_move_ownable(new_space, player, roll_result)
        if new_space.type == GameSpaceType.GO_TO_JAIL:
            click.secho("Going to jail...", fg="red", bold=True)
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
        sleep(1)

    def play(self) -> None:
        self.no_cash_players = 0
        list_buff = itertools.cycle(self.players)
        for p in list_buff:
            response = requests.get(f"http://localhost:8000/player/{p.id}").json()
            player = Player(**response)
            if player.cash == 0:
                click.echo(f"Player: {player.name} is out of cash")
                if all(self.player.cash == 0 for self.player in self.players):
                    click.echo("Game over, no players remaining with cash")
                    break
                continue
            self.player_turn(player)
            click.echo("----------")

    def roll_sequence(self, player: Player) -> None:
        roll_result = player.roll()
        # roll result == 98 when 3 consecutive doubles, go to jail
        if roll_result == RollResultCode.THIRD_DOUBLE:
            click.secho(message="3rd consecutive double, go to jail, fool!\n", fg="red", bold=True)
            self.jail_player(player)
            return
        if roll_result == RollResultCode.JAIL_DOUBLE:
            click.secho(
                message="Rolled a double while in jail, now just visiting.\n", fg="red", bold=True
            )
            self.jail_player(player, visit=True)
            return
        click.secho(message=f"Roll result: {roll_result}\n", fg="blue")
        updated_player = self.move_player(player, roll_result)
        new_space = self.spaces[player.position]
        new_space_str = f"{updated_player.name} landed on: {new_space.name}\n"
        if new_space.type == GameSpaceType.PROPERTY:
            new_space_str = (
                f"{updated_player.name} landed on: {new_space.name} ({new_space.group.value})\n"
            )
        click.echo(new_space_str)
        self.post_move_action(new_space, updated_player, roll_result)
        return

    def player_turn(self, player: Player):
        click.secho(message=f"{player.name}'s turn:", underline=True)
        click.secho(message=player, fg="green", bold=True)
        sleep(0.5)
        props_for_building = set()
        for prop in player.properties:
            # only properties can be built upon (not railroads or utilities)
            if prop.type == GameSpaceType.PROPERTY:
                prop_group = requests.get(
                    f"http://localhost:8000/gamespaces/group/{prop.group.value}"
                ).json()
                if all(p.get("owner_id") == player.id for p in prop_group):
                    for p in prop_group:
                        props_for_building.add((p.get("name"), p.get("id")))
        if len(props_for_building) > 0:
            roll = False
            while roll is False:
                res = click.prompt(
                    text="What would you like to do?\nEnter [R] to roll, [B] to build something",
                    type=click.Choice(["R", "B"], case_sensitive=False),
                    show_choices=False,
                )
                if res == "R":
                    # break out of this loop and roll
                    roll = True
                    self.roll_sequence(player)
                if res == "B":
                    roll = True
                    click.echo(
                        f"You may build on these properties: {[p[0] for p in props_for_building]}\n"
                    )
        else:
            self.roll_sequence(player)
