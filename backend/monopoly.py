import os

from dotenv import load_dotenv
from models.gamespace import GameSpace
from schemas.game import Game
from schemas.player import Player
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(".env")
encoded = os.environ["DATABASE_URL"]
engine = create_engine(encoded, echo=False)
Session = sessionmaker(engine)


def get_spaces(session=Session):
    with Session() as session:
        spaces = session.query(GameSpace).all()
        return [(space.name, space.value) for space in spaces]


def get_players(game: Game):
    num_players = int(input("How many players?"))
    for i in range(0, num_players):
        name = input("Enter player name")
        game.add_player(Player(id=i, name=name))


if __name__ == "__main__":  # pragma: no cover
    print(get_spaces())
    game = Game()
    get_players(game)
