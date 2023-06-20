from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from models.card import Card

router = APIRouter()


def get_playing_card(gamespace_id: int):
    return db.session.query(Card).filter(Card.id == gamespace_id).first()


@router.get("/cards/")
def get_cards():
    return db.session.query(Card).all()


@router.get("/card/{card_id}")
def get_card(card_id):
    db_entry = get_playing_card(card_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_entry
