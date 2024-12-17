import json
import pdb
from datetime import datetime
from pathlib import Path
import sys
import logging
from platform import system

from flask import Flask, render_template, request, redirect, flash, url_for


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

def load_clubs(file_path='clubs.json'):
    path = Path(file_path)

    try:
        if not path.exists():
            path.write_text(json.dumps({'clubs': []}, indent=4), encoding='utf-8')

        with open(file_path, 'r') as c:
             return json.load(c)['clubs']

    except json.JSONDecodeError:
        logging.error(f"The {file_path} is corrupted!")
        raise SystemExit()
    except PermissionError:
        logging.error(f"You do not have access to file {file_path}")
        raise SystemExit()
    except Exception as e:
        logging.error(f"An unexpected error is occurred: {e}")
        raise SystemExit()


def load_competitions(file_path='competitions.json'):
    path = Path(file_path)

    try:
        if not path.exists():
            path.write_text(json.dumps({'competitions': []}, indent=4), encoding='utf-8')

        with open(file_path, 'r') as comps:
             return json.load(comps)['competitions']

    except json.JSONDecodeError:
        logging.error(f"Error: The {file_path} is corrupted!")
        raise SystemExit()
    except PermissionError:
        logging.error(f"You do not have access to file {file_path}")
        raise SystemExit()
    except Exception as e:
        logging.error(f"An unexpected error is occurred: {e}")
        raise SystemExit()


def save_clubs(clubs, file_path='clubs.json'):
    try:
        data = {'clubs': clubs}

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"Error saving clubs: {e}")


def save_competitions(competitions, file_path='competitions.json'):
    try:
        data = {'competitions': competitions}

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"Error saving competitions: {e}")

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()

@app.route('/')
def index():
    return render_template('index.html')


def assign_competition_status(competitions):
    for competition in competitions:
        if datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S") > datetime.now():
            competition["status"] = "open"
        else:
            competition["status"] = "close"
    return competitions

def is_email_invalid(email):
    # Retrieve all emails
    emails = [club['email'] for club in clubs] if clubs else []
    if email not in emails:
        raise BookingError("Sorry! This email isn't not found.")


@app.route('/showSummary', methods=['GET', 'POST'])
def show_summary():
    try:

        if request.method == 'POST':
            # Check if the email is presente in the JSON database
            email = request.form['email']
            is_email_invalid(email)

            club = [club for club in clubs if club['email'] == email][0]
        else:
            club = clubs[0]
        assign_competition_status(competitions)
        return render_template('welcome.html', club=club, competitions=competitions)

    except BookingError as e:
        return render_template('email.html', error_message=e)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]

    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


class BookingError(Exception):
    pass


def process_booking(competition, club, places_required):
    """
    Processes the logic booking for competitions places.
    :param competition: The competition selected by the user.
    :param club: The club requesting the booking.
    :return: updated_club, updated_competition OR raises booking_error
    """
    try:
        places_required = int(places_required)
        club_points = int(club['points'])
        competition_places = int(competition['numberOfPlaces'])

        # Validate the number of place to purchase
        if places_required <= 0:
            raise BookingError("Invalid number of places requested 😡")

        if club_points < places_required:
            raise BookingError("You don't have enough points to purchase the requested places 🙂")
        if competition_places < places_required:
            raise BookingError("Not enough places in the competition to meet request 🙂")

        # Initializes the list of registered clubs
        if 'registered_clubs' not in competition:
            competition['registered_clubs'] = {}

        # Count the number of places purchased per club And limit the number of reservations to 12 places
        if club['name'] not in competition['registered_clubs']:
            competition['registered_clubs'][club['name']] = 0
        count = competition['registered_clubs'][club['name']] + places_required
        if count  > 12:
            raise BookingError(f"Max 12 places per competition 🙂. "
                               f"You have {12-(competition['registered_clubs'][club['name']])} places left.")
        competition['registered_clubs'][club['name']] = count

        # Update club and competition points after booking
        club['points'] = club_points - places_required
        competition['numberOfPlaces'] = competition_places - places_required

        return competition, club

    except ValueError:
        raise BookingError('The number format provided is invalid 😡')


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    try:
        # Find competition and club
        competition = next(c for c in competitions if c['name'] == request.form['competition'])
        club = next(c for c in clubs if c['name'] == request.form['club'])

        # Start booking
        competition, club = process_booking(competition, club, request.form['places'])

        # Update data in JSON
        save_clubs(clubs)
        save_competitions(competitions)

        # Display the booking confirmation message
        flash(f"Great 👍! You have booked {request.form['places']} places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    except BookingError as e:
        return render_template('error.html', error_message=e)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))