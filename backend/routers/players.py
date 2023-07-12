from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from models.player import Player
from schemas.player import Player as PlayerSchema
from schemas.player import PlayerCreate, PlayerUpdate

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


@router.get("/players/")
def get_players():
    return db.session.query(Player).all()


@router.patch("/player/{player_id}")
def update_player(player_id, player: PlayerUpdate):
    db_entry = get_game_player(player_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Player not found")
    update_data = player.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_entry, key, value)
    db.session.commit()
    db.session.refresh(db_entry)
    return db_entry


@router.post("/players/")
def create_player(name: str):
    db_entry = get_player_by_name(name)
    if db_entry:
        raise HTTPException(status_code=400, detail="Player already saved")
    return create_game_player(name)
