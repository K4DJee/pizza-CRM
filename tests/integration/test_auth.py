import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_user():
    user_data = {
        "email": "user1234@example.com",
        "password": "12345678" 
    }

    response = client.post("/api/v1/login", json=user_data)

    assert response.status_code == 200
# РЕГРЕССИОННЫЕ ТЕСТЫ

def test_register_existing_user():# run test after func test_register_user
    user_data = {
        "name": "UserTest",
        "surname": "UserTest",
        "patronymic": "UserTest",
        "age": 20,
        "email": "user123@example.com",
        "password": "12345678"
    }
    response = client.post("/api/v1/register", json=user_data)
    
    assert response.status_code == 400
    response_data = response.json()

def test_login_not_existing_user():
    user_data = {
            "email": "not@example.com",
            "password": "12345678" 
    }
    
    response = client.post("/api/v1/login", json=user_data)

    assert response.status_code == 401

# /api/v1/refresh
# /change-password-stage-1
# /change-password-stage-2
# /change-password-stage-3
# /me

# def test_change_password_1():
#     user_data = {
#         "email": "user123@example.com"
#     }

#     response = client.post("/api/v1/change-password-stage-1", json=user_data)
    
#     assert response.status_code == 200

def test_change_password_1_not_existing_user():
    user_data = {
        "email": "not@example.com"
    }

    response = client.post("/api/v1/change-password-stage-1", json=user_data)
    
    assert response.status_code == 404

# def test_change_password_2():
#     user_data = {
#         "email": "not@example.com",
#         "otp": "123456" 
#     }

#     response = client.post("/api/v1/change-password-stage-2", json=user_data)
    
#     assert response.status_code == 401

# def test_change_password_3():
#     user_data = {
#         "email": "not@example.com",
#         "new_password": "12345678" 
#     }

#     response = client.post("/api/v1/change-password-stage-3", json=user_data)
    
#     assert response.status_code == 401

def test_me(auth_tokens):
    access_token, refresh_token = auth_tokens
    user_headers= {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = client.get("/api/v1/me", headers=user_headers)
    
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)

def test_refresh_token(auth_tokens):
    access_token, refresh_token = auth_tokens
    user_headers= {
        "Authorization": f"Bearer {refresh_token}"
    }
    
    response = client.post("/api/v1/refresh", headers=user_headers)
    
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)