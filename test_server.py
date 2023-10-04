import pytest
from server import app,loadClubs

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



