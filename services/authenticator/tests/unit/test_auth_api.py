import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from auth_api import app
from dependencies import get_user_repository
from repository import MockRepository

@pytest.fixture(autouse=True)
def mock_grpc():
    """
    Prevents the real gRPC calls from running during tests.
    """
    with patch('auth_api.create_user', new_callable=AsyncMock) as mock_create, \
         patch('auth_api.delete_user', new_callable=AsyncMock) as mock_delete:
        # yield keeps the 'with' block open, ensuring patches remain active 
        # for the duration of the tests execution.
        yield mock_create, mock_delete  

@pytest.fixture(autouse=True)
def override_repository():
    mock_repo = MockRepository()
    app.dependency_overrides[get_user_repository] = lambda: mock_repo
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def signed_up_user(client):
    client.post("/signup", json={"username": "alice", "password": "secret"})
    return {"username": "alice", "password": "secret"}

@pytest.fixture
def logged_in_user(client, signed_up_user):
    resp = client.post("/login", json=signed_up_user)
    token = resp.json()["access_token"]
    return {**signed_up_user, "token": token}


#  --- Tests ---
def test_signup_success(client):
    response = client.post("/signup", json={"username": "alice", "password": "secret"})
    assert response.status_code == 201
    assert response.json()["username"] == "alice"

def test_duplicated_signup_fails(client, signed_up_user):
    response = client.post("/signup", json=signed_up_user)
    assert response.status_code == 409


def test_login_success(client, signed_up_user):
    resp = client.post("/login", json=signed_up_user)
    token = resp.json()["access_token"]
    assert token is not None

def test_login_with_wrong_password(client, signed_up_user):
    response = client.post("/login", json={"username": signed_up_user["username"], "password": "wrong"})
    assert response.status_code == 401


def test_delete_account_success(client, logged_in_user):
    response = client.post(
        "/delete-account",
        headers={"Authorization": f"Bearer {logged_in_user['token']}"},
        json={"password": logged_in_user["password"]},
    )
    assert response.status_code == 200
    assert "successfully deleted" in response.json()["message"]

def test_delete_account_after_deletion_fails(client, logged_in_user):
    # First deletion
    client.post(
        "/delete-account",
        headers={"Authorization": f"Bearer {logged_in_user['token']}"},
        json={"password": logged_in_user["password"]},
    )
    # Second deletion (should fail
    response = client.post(
        "/delete-account",
        headers={"Authorization": f"Bearer {logged_in_user['token']}"},
        json={"password": logged_in_user["password"]},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "User does not exist."

def test_delete_account_with_wrong_password(client, logged_in_user):
    wrong_password = "a wrong password"

    response = client.post(
        "/delete-account",
        headers={"Authorization": f"Bearer {logged_in_user['token']}"},
        json={"password": wrong_password},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password."

def test_delete_account_with_wrong_token(client, logged_in_user):
    invalid_token = "invalid-token"

    response = client.post(
        "/delete-account",
        headers={"Authorization": f"Bearer {invalid_token}"},
        json={"password": logged_in_user["password"]},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Token is invalid or expired."

def test_delete_account_with_invalid_header(client, logged_in_user):
    response = client.post(
        "/delete-account",
        headers={"Authorization": f"{logged_in_user['token']}"},
        json={"password": logged_in_user["password"]},
    )
    assert response.status_code == 401
    assert response.json()["detail"]== "Header is not valid." 