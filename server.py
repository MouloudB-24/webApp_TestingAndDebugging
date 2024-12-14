import json
import pdb

from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def save_clubs(clubs):
    try:
        data = {'clubs': clubs}

        with open('clubs.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"Error saving clubs: {e}")


def save_competitions(competitions):
    try:
        for competition in competitions:
            if 'date' in competition and isinstance(competition['date'], datetime):
                competition['date'] = str(competition['date'])

        data = {'competitions': competitions}

        with open('competitions.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"Error saving competitions: {e}")

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    # Retrieve all emails
    emails = [club['email'] for club in clubs]

    if request.method == 'POST':
        email = request.form['email']

        # Check if the email is presente in the JSON database
        if email not in emails:
            error_email = "Sorry! This email isn't not found."
            return render_template('email.html', error_email=error_email)
        club = [club for club in clubs if club['email'] == email][0]
    else:
        club = clubs[0]

    for competition in competitions:
        if isinstance(competition['date'], str):
            competition['date'] = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
            if competition['date'] > datetime.now():
                competition["status"] = "open"
            else:
                competition["status"] = "close"
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    club_points = int(club['points'])
    competition_places = int(competition['numberOfPlaces'])

    # Validate the number of place to purchase
    if club_points < placesRequired:
        error_message = "You don't have enough points to purchase the requested places 🙂"
        return render_template('error.html', error_message=error_message)

    if competition_places < placesRequired:
        error_message = "Not enough places in the competition to meet request 🙂"
        return render_template('error.html', error_message=error_message)

    # Initializes the list of registered clubs
    if 'registered_clubs' not in competition:
        competition['registered_clubs'] = {}

    # count the number of places purchased per club
    if club['name'] not in competition['registered_clubs']:
        competition['registered_clubs'][club['name']] = 0

    competition['registered_clubs'][club['name']] += placesRequired

    # Limit the number of reservations to 12 places
    if competition['registered_clubs'][club['name']] > 12:
        error_message = "You're not allowed to reserve more than 12 places per competition."
        return render_template('error.html', error_message=error_message)

    # Update club and competition points after booking
    club['points'] = club_points - placesRequired
    competition['numberOfPlaces'] = competition_places - placesRequired

    flash(f'Great 👍! You have booked {placesRequired} places.')

    # Update data in JSON
    save_clubs(clubs)
    save_competitions(competitions)

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))