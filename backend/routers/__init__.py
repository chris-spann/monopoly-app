from fastapi import APIRouter
from routers import cards, deeds, gamespaces, players, root

api_router = APIRouter()

# api_router.include_router(authors.router, tags=["authors"])
# api_router.include_router(books.router, tags=["books"])
api_router.include_router(cards.router, tags=["cards"])
api_router.include_router(deeds.router, tags=["deeds"])
api_router.include_router(gamespaces.router, tags=["gamespaces"])
api_router.include_router(players.router, tags=["players"])
api_router.include_router(root.router, tags=["root"])
