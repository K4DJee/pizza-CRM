import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(scope="session")
def test_user():
    """"Создание тестового пользователя"""
    return {
        "name": "Regression",
        "surname": "Test",
        "patronymic": "User",
        "age": 20,
        "email": "regression_test_user@example.com",
        "password": "SecurePassword123!"
    }

@pytest.fixture(scope="session")
def registered_user(test_user):
    response = client.post("/api/v1/register", json=test_user)

    assert response.status_code in [200, 400]
    return test_user

@pytest.fixture(scope="session")
def auth_tokens(registered_user):
    response = client.post("/api/v1/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })

    assert response.status_code == 200

    tokens = response.json()
    return tokens["AccessToken"], tokens["RefreshToken"]