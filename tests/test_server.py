from datetime import datetime

import pytest


def test_showSummary_competitions_status():
    competitions =[
        {'name': 'competition A', 'date': "2020-03-27 10:00:00", 'numberOfPlaces': '13'},
        {'name': 'competition B', 'date': "2050-03-27 10:00:00", 'numberOfPlaces': '30'}
    ]

    for competition in competitions:
        if isinstance(competition['date'], str):
            competition['date'] = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
            if competition['date'] > datetime.now():
                competition["status"] = "open"
            else:
                competition["status"] = "close"

    expected = [
        {
            'name': 'competition A',
            'date': datetime(2020, 3, 27, 10, 00, 00),
            'numberOfPlaces': '13',
            'status': 'close'},
        {
            'name': 'competition B',
            'date': datetime(2050, 3, 27, 10, 00, 00),
            'numberOfPlaces': '30',
            'status': 'open'
        }
    ]

    assert competitions == expected


def test_showSummary_already_datetime():
    competitions = [
            {
                'name': 'competition A',
                'date': datetime(2030, 12, 31, 12, 0, 0),
                'numberOfPlaces': '13'
            }
        ]

    for competition in competitions:
        if isinstance(competition['date'], str):
            competition['date'] = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
        if competition['date'] > datetime.now():
            competition["status"] = "open"
        else:
            competition["status"] = "close"

    expected = [
            {
                'name': 'competition A',
                'date': datetime(2030, 12, 31, 12, 0, 0),
                'numberOfPlaces': '13',
                'status': 'open'
            }
        ]

    assert competitions == expected


def test_showSummary_invalid_date():
    competitions = [
        {'name': 'competition A', 'date': "invalid date", 'numberOfPlaces': '13'}
    ]

    with pytest.raises(ValueError):
        for competition in competitions:
            if isinstance(competition['date'], str):
                competition['date'] = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")


def test_purchasePlaces_initialize_registered_club():
    competition = {'name': 'competition A', 'date': "2020-03-27 10:00:00", 'numberOfPlaces': '13'}

    if 'registered_clubs' not in competition:
        competition['registered_clubs'] = {}

    assert 'registered_clubs' in competition
    assert len(competition['registered_clubs']) == 0

def test_purchasePlaces_competition_places_update():
    competition = {"name": 'competition A', "date": "2020-03-27 10:00:00", 'numberOfPlaces': '13', "registered_clubs": {}}
    club = {"name": "club A" }

    if club['name'] not in competition['registered_clubs']:
        competition['registered_clubs'][club['name']] = 0

    placesRequired = 3
    competition_places = 13

    competition['registered_clubs'][club['name']] += placesRequired
    competition['numberOfPlaces'] = competition_places - placesRequired

    assert competition['registered_clubs'][club['name']] == 3
    assert competition['numberOfPlaces'] == 10


def test_purchasePlaces_exced_12_places_limit():
    competition = {"name": 'competition A', "date": "2020-03-27 10:00:00", 'numberOfPlaces': 10,
                   "registered_clubs": {"club A": 10}}
    club = {"name": "club A"}

    placesRequired = 5
    competition['registered_clubs'][club['name']] += placesRequired

    assert competition['registered_clubs'][club['name']] > 12





