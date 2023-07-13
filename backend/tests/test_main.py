import requests
from schemas.constants import PropertyStatus


def test_hello_world(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_gamespaces():
    res = requests.get("http://localhost:8000/gamespaces/")
    res_json = res.json()
    assert res.status_code == 200
    assert res_json[0]["type"] == "free"
    assert res_json[0]["name"] == "GO"
    assert res_json[0]["value"] == 200
    assert res_json[0]["status"] == PropertyStatus.VACANT
