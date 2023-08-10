from constants import PropertyGroup
from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from models.gamespace import GameSpace
from routers.deeds import get_deed
from schemas.deed import PropertyDeed as PropertyDeedSchema
from schemas.gamespace import GameSpace as GameSpaceSchema
from schemas.gamespace import GameSpaceUpdate

router = APIRouter()


def get_spaces():
    return db.session.query(GameSpace).order_by(GameSpace.id).all()


def get_space(gamespace_id):
    return (
        db.session.query(GameSpace)
        .filter(GameSpace.id == gamespace_id)
        .order_by(GameSpace.id)
        .first()
    )


@router.get("/gamespaces/")
def get_gamespaces():
    spaces = get_spaces()
    for space in spaces:
        space.deed = get_deed(space.id)
    return spaces


@router.get("/gamespaces/group/{group}")
def get_gamespaces_by_group(group: PropertyGroup):
    return db.session.query(GameSpace).filter(GameSpace.group == group).all()


@router.get("/gamespace/{gampesace_id}", response_model=GameSpaceSchema)
def get_gamespace(gamespace_id):
    db_entry = get_space(gamespace_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Gamespace not found")
    return db_entry


@router.patch("/gamespace/{gamespace_id}")
def update_gamespace(gamespace_id, gamespace: GameSpaceUpdate):
    db_entry = get_space(gamespace_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Gamespace not found")
    update_data = gamespace.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_entry, key, value)
    db.session.commit()
    db.session.refresh(db_entry)
    return db_entry


@router.get("/gamespace/{gamespace_id}/deed", response_model=PropertyDeedSchema)
def get_gamespace_deed(gamespace_id):
    db_entry = get_deed(gamespace_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Deed not found")
    return db_entry
