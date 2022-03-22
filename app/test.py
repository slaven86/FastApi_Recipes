import json
from fastapi.testclient import TestClient
from .main import app



client = TestClient(app)



def test_create_user():
    data = {"first_name": "ivan", "last_name": "ivanovic", "email": "ivan@ivan.com", "username": "ivan123", "password": "ivan123"}
    response = client.post('/users', json.dumps(data))
    assert response.status_code == 201
    assert response.json() == {"msg": "New user created!"}
    


def test_create_recipe():

    data = {"name": "Cheese cake",
            "description": "Maslac iseći na kockice, dodati plazmu i šećer u prahu, pa rukom sjediniti i formirati koricu u okruglom kalupu za torte. Umutiti slatku pavlaku, u drugoj posudi kašikom sjediniti Ella sir i šećer u prahu, zatim sve spojiti i mutiti mikserom, želatin rastopiti po uputstvu sa kesice i dodati u fil, muteći mikserom da se sve lepo sjedini, sipati preko korice.Voće, šećer i vodu staviti na šporet da provri, kuvati 5 minuta, skloniti za ringle, i onda dodati želatin u vrelu masu da se rastopi. Ostaviti da se prohladi, pa sipati preko fila."
             }
    token = ''
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post('/recipes', json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json() == {"msg": "New recipe created!"}


def test_get_single_recipe():
    token = ''
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get('/recipes/37', headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Palacinke"



def test_get_all_recipes():
    response = client.get('/recipes')
    assert response.status_code == 200



def test_delete_recipe():
    token = ''
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete('/recipes/2', headers=headers)
    assert response.status_code == 200
    assert response.json() == {"msg": "Recipe has been deleted!"}


def test_get_top_ingredients():
    response = client.get('/top-ingredients')
    assert response.status_code == 200







