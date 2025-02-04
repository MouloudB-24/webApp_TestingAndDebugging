
import json
from unittest.mock import patch

import pytest

from server import save_clubs, save_competitions, process_booking, BookingError, assign_competition_status, \
    is_email_invalid


def test_save_clubs_valid_data():
    """
    Check that data is saved correctly.
    """
    clubs = [{'name': 'club 1', 'email': 'club1@gmail.com', 'points': '10'}]
    save_clubs(clubs, 'test_clubs.json')

    with open('test_clubs.json', 'r') as f:
        result = json.load(f)

    assert result == {'clubs': [{'name': 'club 1', 'email': 'club1@gmail.com', 'points': '10'}]}


def test_save_competitions_valid_data():
    """
    Check that data is saved correctly.
    """
    competition = [{'name': 'competition1', 'date': '2020-10-22 13:30:00' , 'numberOfPlaces': '2'}]

    save_competitions(competition, 'test_competitions.json')

    with open('test_competitions.json', 'r') as f:
        result = json.load(f)

    assert result == {'competitions': [{'name': 'competition1', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '2'}]}




def test_is_email_invalid():
    """
    Test the invalidity of a club email
    """
    mock_clubs = [{"name": "club A", 'email': 'clubA@gmail.com', 'points': '15'},
             {"name": "club A", 'email': 'clubB@gmail.com', 'points': '15'}]

    with patch('server.clubs', mock_clubs):
        with pytest.raises(BookingError, match="Sorry! This email isn't not found."):
            is_email_invalid('invalid@gmail.com')


def test_assign_competition_status():
    """
    Check that the competition status has been assigned.
    """
    competitions =[{'name': 'competition A', 'date': "2020-03-27 10:00:00", 'numberOfPlaces': '13'},
                   {'name': 'competition B', 'date': "2050-03-27 10:00:00", 'numberOfPlaces': '30'}]

    result = assign_competition_status(competitions)

    expected = [{'name': 'competition A', 'date': "2020-03-27 10:00:00", 'numberOfPlaces': '13', 'status': 'close'},
                    {'name': 'competition B', 'date': "2050-03-27 10:00:00", 'numberOfPlaces': '30', 'status': 'open'}]

    assert expected == result

    assert competitions == expected

def test_process_booking_valid():
    """
    Check that the updating of the places and points is correct.
    """
    competition = {'name': 'competition A', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '20'}
    club = {"name": "club A", 'email': 'clubA@gmail.com', 'points': '15' }

    places_required = 5

    process_booking(competition, club, places_required)

    assert competition['numberOfPlaces'] == '15', 'Le nombre de places doit être réduit correctement.'
    assert club['points'] == '10', 'Le nombre de points doit être réduit correctement.'


def test_process_booking_exced_12_places_limit():
    """
    Check the limit of 12 places per competition is respected.
    """
    competition = {'name': 'competition A', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '30'}
    club = {"name": "club A", 'email': 'clubA@gmail.com', 'points': '20'}

    with pytest.raises(BookingError, match='Max 12 places per competition 🙂. You have 12 places left.'):
        process_booking(competition, club, places_required = 13)

def test_process_booking_invalid_places():
    competition = {'name': 'competition A', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '30'}
    club = {"name": "club A", 'email': 'clubA@gmail.com', 'points': '20'}

    with pytest.raises(BookingError, match='Invalid number of places requested.'):
        process_booking(competition, club,   places_required = -1)

def test_process_booking_insufficient_points():
    competition = {'name': 'competition A', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '30'}
    club = {"name": "club A", 'email': 'clubA@gmail.com', 'points': '10'}

    with pytest.raises(BookingError, match="You don't have enough points..."):
        process_booking(competition, club,   places_required = 12)

def test_process_booking_insufficient_places():
    competition = {'name': 'competition A', 'date': '2020-10-22 13:30:00', 'numberOfPlaces': '10'}
    club = {"name": "club A", 'email': 'clubA@gmail.com', 'points': '12'}

    with pytest.raises(BookingError, match="Not enough places in the competition..."):
        process_booking(competition, club,   places_required = 12)
