import os

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_sqlalchemy import DBSessionMiddleware
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import CardType, GameSpaceType, PropertyGroup, PropertyStatus
from models import Base
from routers import api_router
from schemas.card import Card
from schemas.deed import PropertyDeed
from schemas.gamespace import GameSpace
from schemas.player import Player


@pytest.fixture(scope="module")
def test_client():
    load_dotenv(".env")
    db_url = os.getenv("DATABASE_URL", "@db").replace("@db", "@localhost")
    app = FastAPI()
    app.include_router(api_router)
    app.add_middleware(DBSessionMiddleware, db_url=db_url)
    with TestClient(app) as c:
        yield c


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
        group=PropertyGroup.BLUE,  # type: ignore
        status=PropertyStatus.VACANT,  # type: ignore
        deed=None,
    )


@pytest.fixture()
def mock_gamespace():
    return GameSpace(
        id=4,
        owner_id=None,
        name="test",
        value=200,
        type=GameSpaceType.PROPERTY,  # type: ignore
        group=PropertyGroup.BLUE,  # type: ignore
        status=PropertyStatus.VACANT,  # type: ignore
        deed=PropertyDeed(
            id=1,
            rent_group=12,
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
def mocker_gamespace():
    return GameSpace(
        owner_id=1,
        id=5,
        name="test",
        value=200,
        type=GameSpaceType.PROPERTY,
        group=PropertyGroup.BLUE,
        status=PropertyStatus.OWNED,
        deed=PropertyDeed(
            id=1,
            rent_group=12,
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
def mock_gamespaces():
    return [mock_gamespace()]


@pytest.fixture()
def mock_owned_gamespace():
    return GameSpace(
        id=2,
        owner_id=1,
        name="test",
        value=200,
        type=GameSpaceType.PROPERTY,  # type: ignore
        group=PropertyGroup.BLUE,  # type: ignore
        status=PropertyStatus.OWNED,  # type: ignore
        deed=PropertyDeed(
            id=1,
            rent_group=12,
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
def mock_owned_gamespace_group():
    g = GameSpace(
        id=2,
        owner_id=1,
        name="test",
        value=200,
        type=GameSpaceType.PROPERTY,  # type: ignore
        group=PropertyGroup.BLUE,  # type: ignore
        status=PropertyStatus.OWNED,  # type: ignore
        deed=PropertyDeed(
            id=1,
            rent_group=12,
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
    g.is_property_group_owned = True
    return g


@pytest.fixture()
def mock_card():
    return Card(title="test", type="test", action_code="MOCK", is_gooj=False)


# Define a PostgreSQL test database fixture
@pytest.fixture(scope="module")
def mock_db():
    a = factories.postgresql("monopoly_db")
    a.init()
    return a


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/monopoly_db")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def test_session(test_engine):
    session = sessionmaker(bind=test_engine)
    session = session()
    yield session
    session.rollback()
    session.close()
