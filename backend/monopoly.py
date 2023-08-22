import click
from schemas.game import Game


def setup_game() -> Game:
    click.clear()
    print("One moment...")
    game = Game()
    game.setup_players()
    game.get_gamespaces()
    game.get_cards()
    return game


if __name__ == "__main__":
    game = setup_game()
    game.play()
