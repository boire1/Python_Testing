import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def saveClubs():
    with open('clubs.json', 'w') as f:
        json.dump({"clubs": clubs}, f)


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def saveCompetitions():
    with open('competitions.json', 'w') as f:
        json.dump({"competitions": competitions}, f)



app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club_list = [club for club in clubs if club['email'] == request.form['email']]
    if not club_list:  # if the list is empty
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    club = club_list[0]
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
    

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    
    # Check if competition date is in the past
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    if competition_date < datetime.now():
        flash('You cannot book places for past competitions.')
        return render_template('welcome.html',club=club, competitions=competitions)
    
    # Check if the club is trying to book more than 12 places
    if placesRequired > 12:
        flash('You cannot book more than 12 places in one competition.')
        return render_template('welcome.html', club=club, competitions=competitions)

    
    # Check if the club has enough points
    if int(club['points']) < placesRequired:
        flash('You do not have enough points to book these places.')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Check if there are enough available places in the competition
    if int(competition['numberOfPlaces']) < placesRequired:
        flash('There are not enough places available in this competition.')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Deduct the points and update the number of available places in the competition
    club['points'] = str(int(club['points']) - placesRequired)
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
    
    # Save the updated club data to the JSON file
    saveClubs()
    saveCompetitions()
    
                
    #competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)