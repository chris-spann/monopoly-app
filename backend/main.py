import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from routers import api_router

load_dotenv(".env")


def create_app():
    app = FastAPI()
    app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
    app.include_router(api_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
