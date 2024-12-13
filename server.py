import json
from flask import Flask,render_template,request,redirect,flash,url_for


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

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


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

    # Update club and competition points after booking
    club['points'] = club_points - placesRequired
    competition['numberOfPlaces'] = competition_places - placesRequired

    flash(f'Great 👍! You have booked {placesRequired} places.')

    # Update data in JSON
    save_clubs(clubs)
    save_competitions(competitions)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))