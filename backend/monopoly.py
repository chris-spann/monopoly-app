import time

import click
from schemas.game import Game


def setup_game() -> Game:
    click.clear()
    game = Game()
    game.setup_players()
    print("One moment...")
    time.sleep(1)
    game.get_gamespaces()
    game.get_cards()
    time.sleep(1)
    click.clear()
    return game


if __name__ == "__main__":
    game = setup_game()
    game.play()
