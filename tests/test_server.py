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


