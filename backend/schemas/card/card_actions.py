from time import sleep

import click


def mock_action(action_code: str, player_id: int):
    sleep(1)
    click.secho(
        message=f"Completed card action: {action_code} for player_id: {player_id}\n", fg="magenta"
    )


actions = {
    "MOCK": mock_action,
    "ADD-010": mock_action,
    "ADD-020": mock_action,
    "ADD-045": mock_action,
    "ADD-050": mock_action,
    "ADD-X50": mock_action,
    "ADD-100": mock_action,
    "ADD-150": mock_action,
    "ADD-200": mock_action,
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
    "PAY-015": mock_action,
    "PAY-050": mock_action,
    "PAY-100": mock_action,
    "PAY-150": mock_action,
    "PAY-025-100": mock_action,
    "PAY-040-115": mock_action,
    "PAY-X50": mock_action,
}
