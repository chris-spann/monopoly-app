# unit tests for deeds router


from constants import GameSpaceType
from models import Deed, GameSpace


class TestDeedsRouter:
    def test_get_deeds(self, test_client, test_session):
        # res = requests.get("http://localhost:8000/deed/1")

        gamespace = GameSpace(
            id=2,
            name="test",
            value=2,
            type=GameSpaceType.PROPERTY,
            group="blue",
            status="vacant",
        )
        deed = Deed(
            id=1,
            gamespace_id=2,
            rent_group=12,
            deed_type=GameSpaceType.PROPERTY,
            rent=10,
            rent_1_house=20,
            rent_2_houses=30,
            rent_3_houses=40,
            rent_4_houses=50,
            rent_hotel=60,
            house_cost=50,
            hotel_cost=50,
        )
        test_session.add_all([deed, gamespace])
        test_session.commit()
        res = test_client.get("/deed/1")
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("id") == 1
        assert res_json.get("rent") == 10
        # pass

    # unit test for get_property_deed
    # def test_get_property_deed(self):
    #     res = requests.get("http://localhost:8000/deed/1")
    #     res_json = res.json()
    #     assert res.status_code == 200
    #     assert res_json.get("id") == 1
    #     assert res_json.get("rent") == 2

    # def test_read_main(self, test_client):
    #     response = test_client.get("/")
    #     assert response.status_code == 200
    #     assert response.json() == {"message": "Hello World"}

    # def test_get_deeds_2(self):
    #     res = requests.get("http://localhost:8000/deed/3")
    #     assert res.status_code == 200
    #     assert res.json() == {
    #         "deed_type": "property",
    #         "gamespace_id": 3,
    #         "hotel_cost": 50,
    #         "house_cost": 50,
    #         "id": 3,
    #         "rent": 4,
    #         "rent_1_house": 20,
    #         "rent_2_houses": 60,
    #         "rent_3_houses": 180,
    #         "rent_4_houses": 320,
    #         "rent_group": 8,
    #         "rent_hotel": 450,
    #     }
