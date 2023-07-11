from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from models.deed import Deed
from models.gamespace import GameSpace
from schemas.deed import PropertyDeed as PropertyDeedSchema
from schemas.gamespace import GameSpace as GameSpaceSchema
from schemas.gamespace import GameSpaceUpdate

router = APIRouter()


def get_space(gamespace_id: int):
    return db.session.query(GameSpace).filter(GameSpace.id == gamespace_id).first()


def get_deed(gamespace_id: int):
    return db.session.query(Deed).filter(Deed.id == gamespace_id).first()


@router.get("/gamespaces/")
def get_gamespaces():
    return db.session.query(GameSpace).all()


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
