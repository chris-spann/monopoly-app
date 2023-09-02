import pytest
from constants import PropertyStatus


class TestGameSpace:
    @pytest.mark.parametrize(
        ("gamespace", "status", "expected"),
        [
            ("mock_gamespace_no_deed", PropertyStatus.VACANT, 0),
            ("mock_gamespace", PropertyStatus.OWNED, 10),
            ("mock_gamespace", PropertyStatus.VACANT, 0),
            ("mock_gamespace", PropertyStatus.OWNED_1_HOUSE, 20),
            ("mock_gamespace", PropertyStatus.OWNED_2_HOUSES, 30),
            ("mock_gamespace", PropertyStatus.OWNED_3_HOUSES, 40),
            ("mock_gamespace", PropertyStatus.OWNED_4_HOUSES, 50),
            ("mock_gamespace", PropertyStatus.OWNED_HOTEL, 60),
            ("mock_gamespace", "", 0),
        ],
    )
    def test_get_property_rent(self, gamespace, status, expected, request):
        gamespace = request.getfixturevalue(gamespace)
        gamespace.status = status
        assert gamespace.get_property_rent() == expected
