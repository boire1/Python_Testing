import pytest
from server import app,loadClubs,loadCompetitions,competitions,clubs

@pytest.fixture(autouse=True)
def reset_data():
    global clubs, competitions
    clubs = loadClubs()
    competitions = loadCompetitions()



def test_loadClubs():
    # Appel de la fonction
    clubs = loadClubs()

    # S'assurer que la fonction retourne une liste 
    assert isinstance(clubs, list), "Expected a list"

    # S'assurer  que la liste n'est pas vide 
    assert len(clubs) > 0, "Expected non-empty list"

    # Testez si chaque élément de la liste est un dictionnaire contenant une clé "name" et une clé "email"
    for club in clubs:
        assert "name" in club, f"Expected 'name' in club, got {club}"
        assert "email" in club, f"Expected 'email' in club, got {club}"
        

def test_loadCompetitions():
    #  Function call
    competitions = loadCompetitions()

    # Ensure that the function returns a list
    assert isinstance(competitions, list), "Expected a list"

    # Ensure that the list is not empty
    assert len(competitions) > 0, "Expected non-empty list"

    # Test if each element of the list is a dictionary containing the essential keys
    for competition in competitions:
        assert "name" in competition, f"Expected 'name' in competition, got {competition}"
        assert "date" in competition, f"Expected 'date' in competition, got {competition}"
        assert "numberOfPlaces" in competition, f"Expected 'numberOfPlaces' in competition, got {competition}"


import pytest
from server import app, loadClubs
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_showSummary_correct_email(client):
    # Simulate a connection with a valid email
    club_email = loadClubs()[0]['email']  # Utilisez le premier e-mail de club pour le test
    response = client.post('/showSummary', data={'email': club_email})
    assert response.status_code == 200
    assert club_email in response.data.decode('utf-8')

def test_showSummary_incorrect_email(client):
    # Use the first club email for the test 'test_showSummary_incorrect_email '
    wrong_email = "wrong@example.com"
    response = client.post('/showSummary', data={'email': wrong_email})
    assert response.status_code == 302
    assert "Location" in response.headers
    assert url_for('index') in response.headers["Location"]

def test_book_valid_club_and_competition(client):
    #  name of a valid club and competition from clubs.json data
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    
    response = client.get(f'/book/{club_name}/{competition_name}')
    
    assert response.status_code == 200
    # check that certain key elements are present on the page :
    assert b'Booking for' in response.data

    assert bytes(competition_name, 'utf-8') in response.data
    assert bytes(club_name, 'utf-8') in response.data
    
    
def test_book_invalid_club(client):
    club_name = "Non Existent Club"
    competition_name = "Spring Festival"
    
    response = client.get(f'/book/{club_name}/{competition_name}')
    
    assert b"Something went wrong-please try again" in response.data
    

def test_book_invalid_competition(client):
    club_name = "Simply Lift"
    competition_name = "Non Existent Competition"
    
    response = client.get(f'/book/{club_name}/{competition_name}')
    
    assert b"Something went wrong-please try again" in response.data  
      
# ---------------------------------PurchasePlaces--------------------------------------------------------------------

def test_successful_purchase(client):
    club_name = "Simply Lift"  
    competition_name = "Spring Festival"  
    number_of_places = 5
    
    initial_places = [comp for comp in competitions if comp['name'] == competition_name][0]['numberOfPlaces']
    initial_points = [club for club in clubs if club['name'] == club_name][0]['points']

    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': number_of_places
    })

    assert b'Great-booking complete!' in response.data

    updated_places = [comp for comp in competitions if comp['name'] == competition_name][0]['numberOfPlaces']
    updated_points = [club for club in clubs if club['name'] == club_name][0]['points']

    assert int(updated_places) == int(initial_places) - number_of_places
    assert int(updated_points) == int(initial_points) - number_of_places
#             _____________________________________________________________________

def test_exceed_max_purchase_limit(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    number_of_places = 13  # Plus que la limite maximale

    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': number_of_places
    })

    assert b'You cannot book more than 12 places in one competition.' in response.data
    
#             _____________________________________________________________________
    
def test_exceed_points_available(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"
    number_of_places = 10  # set it to more than the club's points but not superior to 12

    response = client.post('/purchasePlaces', data={
        'club': club_name,
        'competition': competition_name,
        'places': number_of_places
    })

    assert b'You do not have enough points to book these places.' in response.data
    
#-----------------------------------------------Index------------------------------------------------------------------------

def test_index_page(client):
    response = client.get('/')
    
    # Check that the status code is 200
    assert response.status_code == 200
    
    # Check that the title is present
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    
    # Check the presence of the form
    assert b'<form action="showSummary" method="post">' in response.data
    assert b'<input type="email" name="email"' in response.data
    assert b'<button type="submit">Enter</button>' in response.data