from unittest.mock import patch

from constants import PropertyStatus


class TestGameSpace:
    def test_get_property_rent_group(self, mocker_gamespace):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = [
                {"owner_id": 1},
                {"owner_id": 1},
                {"owner_id": 1},
            ]
            assert mocker_gamespace.get_property_rent() == 12

    def test_get_property_rent(self, mocker_gamespace):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = [
                {"owner_id": 1},
                {"owner_id": 2},
                {"owner_id": 1},
            ]
            assert mocker_gamespace.get_property_rent() == 10

    def test_get_property_rent_hotel(self, mocker_gamespace):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = [
                {"owner_id": 1},
                {"owner_id": 2},
                {"owner_id": 1},
            ]
            mocker_gamespace.status = PropertyStatus.OWNED_HOTEL
            assert mocker_gamespace.get_property_rent() == 60

    def test_get_property_rent_vacant(self, mocker_gamespace):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = [
                {"owner_id": 1},
                {"owner_id": 2},
                {"owner_id": 1},
            ]
            mocker_gamespace.status = PropertyStatus.VACANT
            assert mocker_gamespace.get_property_rent() == 0

    def test_get_property_rent_no_deed(self, mocker_gamespace):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = [
                {"owner_id": 1},
                {"owner_id": 2},
                {"owner_id": 1},
            ]
            mocker_gamespace.deed = None
            assert mocker_gamespace.get_property_rent() == 0
