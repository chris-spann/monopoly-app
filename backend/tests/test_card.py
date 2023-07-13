class TestCard:
    def test_card_repr(self, mock_card):
        assert repr(mock_card) == "title: test, type: test"
