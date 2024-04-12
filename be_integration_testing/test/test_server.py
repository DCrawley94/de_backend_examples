from fastapi.testclient import TestClient
from server import app
from db.data.index import data
from db.seed import seed
import pytest

@pytest.fixture(autouse=True)
def reset_db():
    seed(**data)


class TestGetReviewByID:
    def test_200_review_returned(self):
        client = TestClient(app)
        expected_json = {
            'review': {
                'comment': (
                    "Skate ipsum dolor sit amet, alley oop vert mute-air "
                    "Colby Carter flail 180 berm. Half-cab camel back "
                    "ollie transition ledge Wes Humpston 1080. Carve casper "
                    "switch kickturn late downhill. Hardware nosebone Rick "
                    "McCrank bluntslide bigspin steps egg plant. Slap "
                    "maxwell roll-in airwalk fast plant fastplant pivot."
                ),
                'game_title': 'Donkey Kong',
                'rating': 4,
                'review_id': 2,
                'username': 'rogersop',
            }
        }

        response = client.get("/api/reviews/2")

        assert response.status_code == 200
        assert response.json() == expected_json

    def test_404_no_review_found(self):
        client = TestClient(app)
        response = client.get("/api/reviews/99999")

        expected = {
            "detail": "No review found with id 99999"
        }

        assert response.status_code == 404
        assert response.json() == expected

    # You can do one of these two tests depending on how you want 
    #   to handle malformed IDs

    def test_422_malformed_review_id(self):
        """ Test for if you want to let pydantic do the work for you """
        client = TestClient(app)
        response = client.get("/api/reviews/not_an_id")

        assert response.status_code == 422

    def test_400_malformed_review_id(self):
        """ Test for if you want to respond with a 400 """
        client = TestClient(app)
        response = client.get("/api/reviews/not_an_id")

        assert response.status_code == 400
        assert response.json() == (
            'review_id should be an integer'
        )


class TestPostGame:
    def test_201_game_returned(self):
        client = TestClient(app)
        new_game = {
            "game_title": "Skyrim 2",
            "release_year": 2024,
            "console_name": "Playstation 2",
            "image_url": "test_url"
        }
        expected_response_body = {
            'game': {
                'game_id': 4,
                'game_title': 'Skyrim 2',
                'release_year': 2024,
                'console_name': 'Playstation 2',
                'image_url': 'test_url'
            }
        }
        response = client.post('/api/games', json=new_game)
        assert response.status_code == 201
        assert response.json() == expected_response_body

    def test_422_malformed_game(self):
        """ 
        Could also treat this as a 400 like the previous endpoint if you wish
        """
        client = TestClient(app)
        new_game = {
            "game_title": "Skyrim 2",
            "console_name": "Playstation 2",
            "image_url": "test_url"
        }
        response = client.post('/api/games', json=new_game)
        assert response.status_code == 422