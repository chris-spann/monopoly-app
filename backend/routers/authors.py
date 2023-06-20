from fastapi import APIRouter
from fastapi_sqlalchemy import db
from models.author import Author as AuthorModel
from schemas.author import Author as AuthorSchema

router = APIRouter()


@router.get("/authors/")
def get_authors():
    return db.session.query(AuthorModel).all()


@router.post("/add-author/", response_model=AuthorSchema)
def add_author(author: AuthorSchema) -> AuthorModel:
    db_author = AuthorModel(**author.dict())
    db.session.add(db_author)
    db.session.commit()
    return db_author
