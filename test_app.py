import string
import random
import pytest
from app import app
from db import init_test_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def database():
    try:
        db = init_test_db()
        yield db
    finally:
        db.close_all()


@pytest.fixture
def random_str():
    s = 10
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=s))
    return str(ran)


@pytest.fixture
def random_str1():
    s = 10
    ran1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=s))
    return str(ran1)


@pytest.fixture
def demo_user(client, database):
    response = client.post('/users/create_user', json={"username": "test_username", "email": "test@gmail.com"})
    return response.get_json()


@pytest.fixture
def demo_account_values(client, database, demo_user, random_str):
    response = {"name": random_str, "user_id": demo_user["id"]}
    return response


@pytest.fixture
def demo_account(client, database, demo_user, random_str):
    response = client.post('/accounts/create_account', json={"name": random_str, "user_id": demo_user["id"]})
    return response.get_json()


@pytest.fixture
def demo_update(client, database):
    response = {"username": "updated_username", "email": "updated@gmail.com", "is_admin": True}
    return response


def test_create_user(client, database):
    response = client.post('/users/create_user', json={"username": "test_username", "email": "test@gmail.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "test_username"
    assert data["is_admin"] == False
    response1 = client.post('/users/create_user', json={"email": "test@gmail.com"})
    assert response1.status_code == 201
    data1 = response1.get_json()
    assert data1["username"] == "Sahan"
    assert data1["email"] == "test@gmail.com"
    # bad_scenarios
    response2 = client.post('/users/create_user', json={"username": "test_username"})
    assert response2.status_code == 400
    response3 = client.post('/users/create_user', json={"username": "test_username", "email": "testgmail.com"})
    assert response3.status_code == 400


def test_get_user(client, database, demo_user):
    response = client.get(f'/users/{demo_user["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == demo_user["id"]
    assert data["username"] == demo_user["username"]
    assert data["email"] == demo_user["email"]
    assert data["is_admin"] == demo_user["is_admin"]
    # bad_scenarios
    response1 = client.get(f'/users/{demo_user["id"]+1}')
    assert response1.status_code == 404


def test_delete_user(client, database, demo_user):
    response = client.get(f'/users/{demo_user["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == demo_user["id"]
    assert data["username"] == demo_user["username"]
    assert data["email"] == demo_user["email"]
    assert data["is_admin"] == demo_user["is_admin"]
    response1 = client.delete(f'/users/delete/{demo_user["id"]}')
    assert response1.status_code == 204
    response1 = client.get(f'/users/{demo_user["id"]}')
    assert response1.status_code == 404


def test_update_user(client, database, demo_user, demo_update):
    response = client.get(f'/users/{demo_user["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == demo_user["id"]
    assert data["username"] == demo_user["username"]
    assert data["email"] == demo_user["email"]
    assert data["is_admin"] == demo_user["is_admin"]
    response1 = client.put(f'/users/update/{demo_user["id"]}', json={"username": demo_update["username"],
                                                                     "email": demo_update["email"],
                                                                     "is_admin": demo_update["is_admin"]})
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1["username"] == demo_update["username"]
    assert data1["email"] == demo_update["email"]
    assert data1["is_admin"] == demo_update["is_admin"]
    assert data1["username"] != data["username"]
    assert data1["email"] != data["email"]
    assert data1["is_admin"] != data["is_admin"]
    # bad_scenarios
    response2 = client.put(f'/users/update/10000', json={"username": demo_update["username"],
                                                         "email": demo_update["email"],
                                                         "is_admin": demo_update["is_admin"]})
    assert response2.status_code == 404


def test_create_account(client, database, demo_account_values, random_str):
    response = client.post('/accounts/create_account', json={"name": random_str,
                                                             "user_id": demo_account_values["user_id"]})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == random_str
    assert data["user_id"] == demo_account_values["user_id"]
    # bad_scenarios
    response2 = client.post('/accounts/create_account', json={"name": "test_name"})
    assert response2.status_code == 400
    response3 = client.post('/accounts/create_account', json={"user_id": 2})
    assert response3.status_code == 400
    response4 = client.post('/accounts/create_account', json={"name": "name1", "user_id": 1})
    assert response4.status_code == 404


def test_get_account(client, database, demo_account):
    response = client.get(f'/accounts/{demo_account["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == demo_account["id"]
    assert data["name"] == demo_account["name"]
    assert data["user_id"] == demo_account["user_id"]
    # bad_scenarios
    response1 = client.get(f'/accounts/10000')
    assert response1.status_code == 404


def test_delete_account(client, database, demo_account):
    response = client.get(f'/accounts/{demo_account["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == demo_account["id"]
    assert data["name"] == demo_account["name"]
    assert data["user_id"] == demo_account["user_id"]
    response1 = client.delete(f'/accounts/delete/{demo_account["id"]}')
    assert response1.status_code == 204
    response1 = client.get(f'/accounts/{demo_account["id"]}')
    assert response1.status_code == 404


def test_update_account(client, database, demo_account_values, demo_account, random_str1):
    response = client.get(f'/accounts/{demo_account["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == demo_account["id"]
    assert data["name"] == demo_account["name"]
    assert data["user_id"] == demo_account["user_id"]
    response1 = client.put(f'/accounts/update/{demo_account["id"]}', json={"name": random_str1, "user_id": 26})
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1["name"] == random_str1
    assert data1["user_id"] == 26
    assert data1["name"] != data["name"]
    assert data1["user_id"] != data["user_id"]
    # bad_scenarios
    response2 = client.put(f'/accounts/update/1000', json={"name": random_str1,
                                                           "user_id": demo_account_values["user_id"]})
    assert response2.status_code == 404
