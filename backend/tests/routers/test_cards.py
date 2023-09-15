import os

from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware
from main import app

load_dotenv(".env")

DBSessionMiddleware(app=app, db_url=os.environ["DATABASE_URL"])


class TestCards:
    def test_get_cards(self, test_client):
        # with db():
        #     # response = test_client.get("/cards/")

        #     response = test_client.get("/cards/")
        #     assert response.status_code == 200
        #     assert len(response.json()) == 32
        pass
