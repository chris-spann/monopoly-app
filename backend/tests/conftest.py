import pytest
from constants import CardType, GameSpaceType, PropertyStatus
from fastapi.testclient import TestClient
from main import app
from schemas.card import Card
from schemas.deed import PropertyDeed
from schemas.gamespace import GameSpace
from schemas.player import Player


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)


@pytest.fixture()
def mock_player():
    return Player(id=1, name="test", cash=1500, position=0, in_jail=False, jail_count=0)


@pytest.fixture()
def mock_jailed_player():
    return Player(id=1, name="test", cash=1500, position=0, in_jail=True, jail_count=2)


@pytest.fixture()
def mock_chance_card():
    return Card(
        title="Advance to Go (Collect $200)",
        type=CardType.CHANCE,
        is_gooj=False,
        action_code="MOCK",
    )


@pytest.fixture()
def mock_cc_card():
    return Card(
        title="Advance to Go (Collect $200)",
        type=CardType.COMMUNITY_CHEST,
        is_gooj=False,
        action_code="MOCK",
    )


@pytest.fixture()
def mock_gooj_card():
    return Card(
        title="Get Out of Jail Free",
        type=CardType.COMMUNITY_CHEST,
        is_gooj=True,
        action_code="MOCK",
    )


@pytest.fixture()
def mock_gamespace_no_deed():
    return GameSpace(
        id=None,
        owner_id=None,
        name="test",
        value=200,
        type=GameSpaceType.PROPERTY,  # type: ignore
        group=None,
        status=PropertyStatus.VACANT,  # type: ignore
        deed=None,
    )


@pytest.fixture()
def mock_gamespace():
    return GameSpace(
        id=None,
        owner_id=None,
        name="test",
        value=200,
        type=GameSpaceType.PROPERTY,  # type: ignore
        group=None,
        status=PropertyStatus.VACANT,  # type: ignore
        deed=PropertyDeed(
            id=1,
            rent_group=1,
            deed_type=GameSpaceType.PROPERTY,
            rent=10,
            rent_1_house=20,
            rent_2_houses=30,
            rent_3_houses=40,
            rent_4_houses=50,
            rent_hotel=60,
            house_cost=50,
            hotel_cost=50,
        ),
    )


@pytest.fixture()
def mock_card():
    return Card(title="test", type="test", action_code="MOCK", is_gooj=False)
