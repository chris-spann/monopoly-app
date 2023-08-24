from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from models.deed import Deed

router = APIRouter()


def get_deed(deed_id):
    deed = db.session.query(Deed).filter(Deed.id == deed_id).first()
    if not deed:
        deed = None
    return deed


@router.get("/deed/{deed_id}")
def get_property_deed(deed_id: int):
    db_entry = get_deed(deed_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Deed not found")
    return db_entry
