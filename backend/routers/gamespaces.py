from constants import GameSpaceType, PropertyGroup
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


@router.get("/gamespaces/utility-rent/{utility_id}/owner/{owner_id}/roll/{roll_result}")
def get_utility_rent(utility_id, owner_id: int, roll_result: int):
    ct = 0
    rr_rent_dict = {1: 25, 2: 50, 3: 100, 4: 200}
    utility = db.session.query(GameSpace).filter(GameSpace.id == int(utility_id)).first()
    if utility is None or utility.type not in [GameSpaceType.UTILITY, GameSpaceType.RAILROAD]:
        raise HTTPException(status_code=404, detail="Utilit/Railroad not found")
    # if utility.owner_id. != owner_id:
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f"Utility/Railroad not owned by player, {utility.owner_id} != {owner_id}",
    #     )
    utilities = db.session.query(GameSpace).filter(GameSpace.group == utility.group).all()
    for u in utilities:
        if u.owner_id is owner_id:
            ct += 1
    if utility.type == GameSpaceType.UTILITY:
        if ct == 1:
            return roll_result * 4
        if ct == 2:
            return roll_result * 10
    if utility.type == GameSpaceType.RAILROAD:
        return rr_rent_dict[ct]
    return 0


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
