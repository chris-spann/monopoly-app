from fastapi import APIRouter
from fastapi_sqlalchemy import db
from models.book import Book as BookModel
from schemas.book import Book as BookSchema

router = APIRouter()


@router.get("/books/")
def get_books():
    return db.session.query(BookModel.all())


@router.post("/add-book/", response_model=BookSchema)
def add_book(book: BookSchema) -> BookModel:
    db_book = BookModel(**book.dict())
    db.session.add(db_book)
    db.session.commit()
    return db_book
