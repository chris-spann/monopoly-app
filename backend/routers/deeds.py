from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from models.deed import Deed

router = APIRouter()


def get_deed(deed_id: int):
    return db.session.query(Deed).filter(Deed.id == deed_id).first()


@router.get("/deed/{deed_id}")
def get_property_deed(deed_id: int):
    db_entry = get_deed(deed_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Deed not found")
    return db_entry
