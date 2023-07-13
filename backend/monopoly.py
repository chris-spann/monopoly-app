from schemas.game import Game


def setup_game() -> Game:
    print("one moment...")
    game = Game()
    game.get_gamespaces()
    game.get_cards()
    game.setup_players()
    return game


if __name__ == "__main__":
    game = setup_game()
    game.play()
