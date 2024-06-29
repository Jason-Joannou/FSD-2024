import requests
import pytest
from unittest.mock import patch
import pandas as pd

BASE_URL = "http://127.0.0.1:8080"

@pytest.fixture(scope="module")
def new_user_data():
    return {
        "username": "NewUserTest",
        "email": "newusertest@example.com",
        "password": "NewUserPass1"
    }

@pytest.fixture(scope="module")
def existing_user_data():
    return {
        "username": "ExistingUser",
        "email": "existinguser@example.com",
        "password": "ExistingPassword"
    }

def test_query_coin_endpoint():
    response = requests.get(f"{BASE_URL}/query_coin?coin_names=Bitcoin")

    assert response.status_code == 200
    assert response.json().get("transaction_state") == 200

def test_daily_price_change_endpoint():
    response = requests.get(f"{BASE_URL}/daily_price_change?coin_names=Bitcoin&coin_names=Cardano")

    assert response.status_code == 200
    assert response.json().get("transaction_state") == 200

def test_daily_price_range_endpoint():
    response = requests.get(f"{BASE_URL}/daily_price_range?coin_names=Bitcoin&coin_names=Cardano")

    assert response.status_code == 200
    assert response.json().get("transaction_state") == 200

def test_moving_average_endpoint():
    response = requests.get(f"{BASE_URL}/moving_averages?coin_names=Bitcoin&coin_names=Cardano")

    assert response.status_code == 200
    assert response.json().get("transaction_state") == 200

    response = requests.get(f"{BASE_URL}/moving_averages?coin_names=Bitcoin&coin_names=Cardano&window=10")

    assert response.status_code == 200
    assert response.json().get("transaction_state") == 200

def test_correlation_matrix_endpoint():
    pass

def test_coin_reporting_endpoint():
    # response = requests.get(f"{BASE_URL}/coin_reporting?coin_name=Aave&graph_type=boxplot")
    pass
     

def test_coin_proportion_endpoint():
    response = requests.get(f"{BASE_URL}/coin_proportion")

    assert response.status_code == 200
    assert response.json().get("transaction_state") == 200
    



@patch("requests.post")
def test_register_user(mock_post, new_user_data):
    # Mock the response for successful registration
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"message": "User registered successfully"}

    response = requests.post(f"{BASE_URL}/register", json=new_user_data)
    
    assert response.status_code == 200
    assert response.json().get("message") == "User registered successfully"

@patch("requests.post")
def test_register_existing_user(mock_post, existing_user_data):
    # Mock the response for registration failure (user already exists)
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"detail": "Username already exists"}

    response = requests.post(f"{BASE_URL}/register", json=existing_user_data)
    assert response.status_code == 400
    assert response.json().get("detail") == "Username already exists"

@patch("requests.post")
def test_register_existing_email(mock_post, new_user_data):
    # Mock the response for registration failure (email already exists)
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"detail": "Email already exists"}

    response = requests.post(f"{BASE_URL}/register", json=new_user_data)
    assert response.status_code == 400
    assert response.json().get("detail") == "Email already exists"

@patch("requests.post")
def test_login_user(mock_post, existing_user_data):
    # Mock the response for successful login
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"message": "Login successful"}

    response = requests.post(f"{BASE_URL}/login", json={
        "username": existing_user_data["username"],
        "password": existing_user_data["password"]
    })
    
    assert response.status_code == 200
    assert response.json().get("message") == "Login successful"

@patch("requests.post")
def test_login_invalid_user(mock_post):
    # Mock the response for login failure (invalid username or password)
    mock_post.return_value.status_code = 401
    mock_post.return_value.json.return_value = {"detail": "Invalid username or password"}

    response = requests.post(f"{BASE_URL}/login", json={
        "username": "InvalidUser",
        "password": "InvalidPassword"
    })
    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid username or password"

if __name__ == "__main__":
    pytest.main()
