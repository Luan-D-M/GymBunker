import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from auth_api import app
from dependencies import get_user_repository, get_jwt_util, get_public_key
from repository import MockRepository
from jwt_utils import JWTUtil

TEST_PRIVATE_KEY =  b"-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAwhvqCC+37A+UXgcvDl+7nbVjDI3QErdZBkI1VypVBMkKKWHM\nNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO/3+gRs/MWG27gdRNtf57uLk1+lQI\n6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pTBvirlsdX+jXrbOEaQphn0OdQo0WD\noOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeMzlD1aDDS478PDZdckPjT96ICzqe4\nO1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZbkhB70aTBuWDGLDR0iLenzyQecmD\n4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJwFwIDAQABAoIBAFCVFBA39yvJv/dV\nFiTqe1HahnckvFe4w/2EKO65xTfKWiyZzBOotBLrQbLH1/FJ5+H/82WVboQlMATQ\nSsH3olMRYbFj/NpNG8WnJGfEcQpb4Vu93UGGZP3z/1B+Jq/78E15Gf5KfFm91PeQ\nY5crJpLDU0CyGwTls4ms3aD98kNXuxhCGVbje5lCARizNKfm/+2qsnTYfKnAzN+n\nnm0WCjcHmvGYO8kGHWbFWMWvIlkoZ5YubSX2raNeg+YdMJUHz2ej1ocfW0A8/tmL\nwtFoBSuBe1Z2ykhX4t6mRHp0airhyc+MO0bIlW61vU/cPGPos16PoS7/V08S7ZED\nX64rkyECgYEA4iqeJZqny/PjOcYRuVOHBU9nEbsr2VJIf34/I9hta/mRq8hPxOdD\n/7ES/ZTZynTMnOdKht19Fi73Sf28NYE83y5WjGJV/JNj5uq2mLR7t2R0ZV8uK8tU\n4RR6b2bHBbhVLXZ9gqWtu9bWtsxWOkG1bs0iONgD3k5oZCXp+IWuklECgYEA27bA\n7UW+iBeB/2z4x1p/0wY+whBOtIUiZy6YCAOv/HtqppsUJM+W9GeaiMpPHlwDUWxr\n4xr6GbJSHrspkMtkX5bL9e7+9zBguqG5SiQVIzuues9Jio3ZHG1N2aNrr87+wMiB\nxX6Cyi0x1asmsmIBO7MdP/tSNB2ebr8qM6/6mecCgYBA82ZJfFm1+8uEuvo6E9/R\nyZTbBbq5BaVmX9Y4MB50hM6t26/050mi87J1err1Jofgg5fmlVMn/MLtz92uK/hU\nS9V1KYRyLc3h8gQQZLym1UWMG0KCNzmgDiZ/Oa/sV5y2mrG+xF/ZcwBkrNgSkO5O\n7MBoPLkXrcLTCARiZ9nTkQKBgQCsaBGnnkzOObQWnIny1L7s9j+UxHseCEJguR0v\nXMVh1+5uYc5CvGp1yj5nDGldJ1KrN+rIwMh0FYt+9dq99fwDTi8qAqoridi9Wl4t\nIXc8uH5HfBT3FivBtLucBjJgOIuK90ttj8JNp30tbynkXCcfk4NmS23L21oRCQyy\nlmqNDQKBgQDRvzEB26isJBr7/fwS0QbuIlgzEZ9T3ZkrGTFQNfUJZWcUllYI0ptv\ny7ShHOqyvjsC3LPrKGyEjeufaM5J8EFrqwtx6UB/tkGJ2bmd1YwOWFHvfHgHCZLP\n34ZNURCvxRV9ZojS1zmDRBJrSo7+/K0t28hXbiaTOjJA18XAyyWmGg==\n-----END RSA PRIVATE KEY-----\n"
TEST_PUBLIC_KEY = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwhvqCC+37A+UXgcvDl+7\nnbVjDI3QErdZBkI1VypVBMkKKWHMNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO\n/3+gRs/MWG27gdRNtf57uLk1+lQI6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pT\nBvirlsdX+jXrbOEaQphn0OdQo0WDoOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeM\nzlD1aDDS478PDZdckPjT96ICzqe4O1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZ\nbkhB70aTBuWDGLDR0iLenzyQecmD4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJw\nFwIDAQAB\n-----END PUBLIC KEY-----\n"

@pytest.fixture(autouse=True)
def override_key_pair():
    def mock_get_jwt_util():
        return JWTUtil(TEST_PRIVATE_KEY, "RS256")
    def mock_get_public_key():
        return TEST_PUBLIC_KEY

    app.dependency_overrides[get_jwt_util] = mock_get_jwt_util
    app.dependency_overrides[get_public_key] = mock_get_public_key

@pytest.fixture(autouse=True)
def override_repository():
    mock_repo = MockRepository()
    app.dependency_overrides[get_user_repository] = lambda: mock_repo
    yield
    app.dependency_overrides.clear()

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