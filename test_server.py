import pytest
from server import app,loadClubs,loadCompetitions

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



