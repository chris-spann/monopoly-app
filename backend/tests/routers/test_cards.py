from models import Card


class TestCards:
    def test_get_cards(self, test_client, test_session):
        # Create test data
        card1 = Card(id=1, title="Card 1", type="chance", is_gooj=False, action_code="MOCK")
        card2 = Card(id=2, title="Card 2", type="chance", is_gooj=False, action_code="MOCK")
        test_session.add_all([card1, card2])
        test_session.commit()

        # Make request to API
        with test_client:
            response = test_client.get("/cards/")

        # Verify response
        assert response.status_code == 200
        assert len(response.json()) == 2
