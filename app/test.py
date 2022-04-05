import json
from fastapi.testclient import TestClient
from .main import app


client = TestClient(app)



def test_create_user():
    data = {"first_name": "", "last_name": "", "email": "", "username": "", "password": ""}
    response = client.post('/users', json.dumps(data))
    assert response.status_code == 201
    assert response.json() == {"msg": "New user created!"}
    


def test_create_recipe():

    data = {"name": "",
            "description": "",
            "ingredients": ""
            }
    token = ''
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post('/recipes', json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json() == {"msg": "New recipe created!"}


def test_get_single_recipe():
    token = ''
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/recipes/1', headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Torta-Moskva"



def test_get_all_recipes():
    response = client.get('/recipes')
    assert response.status_code == 200



def test_delete_recipe():
    token = ''
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete('/recipes/1', headers=headers)
    assert response.status_code == 200
    assert response.json() == {"msg": "Recipe has been deleted!"}


def test_get_top_ingredients():
    response = client.get('/top-ingredients')
    assert response.status_code == 200


def test_get_recipe_avg_rate():
    token = ''
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/recipes/rate/avg', headers=headers)
    assert response.status_code == 200

