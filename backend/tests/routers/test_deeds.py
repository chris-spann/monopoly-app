# unit tests for deeds router
import requests


class TestDeedsRouter:
    def test_get_deeds(self):
        res = requests.get("http://localhost:8000/deed/1")
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("id") == 1
        assert res_json.get("rent") == 2

    # unit test for get_property_deed
    def test_get_property_deed(self):
        res = requests.get("http://localhost:8000/deed/1")
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("id") == 1
        assert res_json.get("rent") == 2

    def test_read_main(self, test_client):
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_get_deeds_2(self):
        res = requests.get("http://localhost:8000/deed/3")
        assert res.status_code == 200
        assert res.json() == {
            "deed_type": "property",
            "gamespace_id": 3,
            "hotel_cost": 50,
            "house_cost": 50,
            "id": 3,
            "rent": 4,
            "rent_1_house": 20,
            "rent_2_houses": 60,
            "rent_3_houses": 180,
            "rent_4_houses": 320,
            "rent_group": 8,
            "rent_hotel": 450,
        }
