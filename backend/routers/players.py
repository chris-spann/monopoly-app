from typing import Any

from constants import GameSpaceType, PropertyStatus
from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from models.player import Player
from routers.gamespaces import get_space
from schemas.player import Player as PlayerSchema
from schemas.player import PlayerCreate

router = APIRouter()


def get_game_player(player_id: int):
    return db.session.query(Player).filter(Player.id == player_id).first()


def get_player_by_name(name: str):
    return db.session.query(Player).filter(Player.name == name).first()


def create_game_player(player):
    p = PlayerCreate(name=player)
    db_item = Player(**p.model_dump())
    db.session.add(db_item)
    db.session.commit()
    db.session.refresh(db_item)
    return db_item


@router.get("/player/{player_id}", response_model=PlayerSchema)
def get_player(player_id: int):
    db_entry = get_game_player(player_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_entry


@router.get("/player/name/{name}", response_model=PlayerSchema)
def get_player_name(name: str):
    db_entry = get_player_by_name(name)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_entry


@router.get("/players/")
def get_players():
    return db.session.query(Player).all()


@router.patch("/player/{player_id}")
def update_player(player_id, player_update: dict[str, Any]):
    db_entry = get_game_player(player_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Player not found")
    for key, value in player_update.items():
        setattr(db_entry, key, value)
    db.session.commit()
    db.session.refresh(db_entry)
    return db_entry


@router.post("/player/{player_id}/add-property/{property_id}")
def add_property(player_id, property_id):
    db_entry = get_game_player(player_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Player not found")
    space = get_space(property_id)
    if space and space.type in [
        GameSpaceType.PROPERTY,
        GameSpaceType.UTILITY,
        GameSpaceType.RAILROAD,
    ]:
        space.status = PropertyStatus.OWNED
        db_entry.properties.append(space)
        db_entry.cash -= space.value
        db.session.commit()
        db.session.refresh(db_entry)
        return db_entry
    raise HTTPException(status_code=400, detail="Error adding property to player")


@router.post("/player/{player_id}/add-cash/{amount}")
def add_cash(player_id: int, amount: int):
    db_entry = get_game_player(player_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Player not found")
    db_entry.cash += amount
    db.session.commit()
    db.session.refresh(db_entry)
    return db_entry


@router.post("/player/{player_id}/deduct-cash/{amount}")
def deduct_cash(player_id: int, amount: int):
    db_entry = get_game_player(player_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Player not found")
    db_entry.cash -= amount
    db.session.commit()
    db.session.refresh(db_entry)
    return db_entry


@router.post("/players/")
def create_player(name: str):
    db_entry = get_player_by_name(name)
    if db_entry:
        raise HTTPException(status_code=400, detail="Player already saved")
    create_game_player(name)
    return get_player_by_name(name)
