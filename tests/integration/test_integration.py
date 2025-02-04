from unittest.mock import patch

import pytest

from server import app, load_clubs, load_competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_data():
    """Mock les données des clubs et compétitions directement en mémoire"""
    clubs = [{"name": "Test Club", "email": "test@club.com", "points": "20"}]
    competitions = [{"name": "Test Competition", "date": "2030-12-31 23:59:59", "numberOfPlaces": "25"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions), \
            patch("server.save_clubs"), patch("server.save_competitions"):
        yield clubs, competitions




def test_integration(client, mock_data):
    clubs, competitions = mock_data

    # Connection test with valid email
    response = client.post("/showSummary", data={"email": "test@club.com"})
    assert response.status_code == 200
    assert b"Welcome" in response.data

    # Reserve 5 places
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Test Competition", "club": "Test Club", "places": "5"},
    )
    assert response.status_code == 200
    assert b"You have booked" in response.data

    # Checks the update
    assert clubs[0]["points"] == "15"  # 20 - 5 = 15
    assert competitions[0]["numberOfPlaces"] == "20"  # 25 - 5 = 20

    # Attempt to reserve 50 places
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Test Competition", "club": "Test Club", "places": "50"},
    )
    assert response.status_code == 200
    assert b"You don&#39;t have enough points" in response.data  # Message d'erreur attendu

    # Disconnect
    response = client.get("/logout")
    assert response.status_code == 302