from time import sleep

import click
import requests


def mock_action(action_code: str, player_id: int):
    sleep(1)
    click.secho(
        message=f"Completed card action: {action_code} for player_id: {player_id}\n", fg="magenta"
    )


def adj_funds(action_code: str, player_id: int):
    inst, update = action_code.split("-")[0], int(action_code.split("-")[1])
    op = "add-cash"
    if inst == "PAY":
        op = "deduct-cash"
    requests.post(f"http://localhost:8000/player/{player_id}/{op}/{update}")
    sleep(1)
    click.secho(
        message=f"Completed card action: {action_code} for player_id: {player_id}\n", fg="magenta"
    )


# get list of players and loop thru them except provided player_id
def adj_funds_batch(action_code: str, player_id):
    res = requests.get("http://localhost:8000/players/").json()
    for player in res:
        if player["id"] != player_id:
            action_code = action_code.replace("X", "0")
            adj_funds(action_code, player["id"])


def find_space(name: str):
    res = requests.get("http://localhost:8000/gamespaces/").json()
    for space in res:
        if space["name"] == name:
            return space["id"]
    return None


def move_player(action_code: str, player_id: int):
    pass


actions = {
    "MOCK": mock_action,
    "ADD-010": adj_funds,
    "ADD-020": adj_funds,
    "ADD-045": adj_funds,
    "ADD-050": adj_funds,
    "ADD-X50": adj_funds_batch,
    "ADD-100": adj_funds,
    "ADD-150": adj_funds,
    "ADD-200": adj_funds,
    "ADV-BRD": mock_action,
    "ADV-GO": mock_action,
    "ADV-ILL": mock_action,
    "ADV-RR": mock_action,
    "ADV-STC": mock_action,
    "ADV-UT": mock_action,
    "BAC-003": mock_action,
    "GO-JAIL": mock_action,
    "GO-RERD": mock_action,
    "GOOJF": mock_action,
    "PAY-015": adj_funds,
    "PAY-050": adj_funds,
    "PAY-100": adj_funds,
    "PAY-150": adj_funds,
    "PAY-025-100": mock_action,
    "PAY-040-115": mock_action,
    "PAY-X50": adj_funds_batch,
}
