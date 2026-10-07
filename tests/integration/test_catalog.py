from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app=app)

# catalog
# /catalog
# /catalog/new"
# /catalog/{item_id}/update
# /catalog/{item_id}

@pytest.fixture(scope="module")
def create_new_dish():
    return {
        "title": "Македонский",
        "description": "string",
        "price": 0,
        "image_url": "string",
        "is_active": True,
        "composition": [
            {
            "quantity": 350,
            "is_optional": True,
            "ingredient": {
                "id": 3
            }
            }
        ]
    }
@pytest.fixture(scope="module")
def update_dish(test_adding_new_catalog_item):
    return {
    "updated_dish":{
        "title": "Македонский23",
        "description": "string",
        "price": 0,
        "image_url": "string",
        "is_active": True,
        "composition": [
            {
            "quantity": 350,
            "is_optional": True,
            "ingredient": {
                "id": 3
            }
            }
        ]
    },
    "updated_dish_id": test_adding_new_catalog_item["id"]
}

def test_get_catalog():
    response = client.get("/api/v1/catalog")

    assert response.status_code == 200
    response_data = response.json()

@pytest.fixture(scope="module")
def test_adding_new_catalog_item(create_new_dish, auth_tokens):
    access_token, refresh_token = auth_tokens
    user_headers= {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.post("/api/v1/catalog/new", json=create_new_dish, headers=user_headers)

    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    return response_data


def test_update_catalog_item(update_dish, test_adding_new_catalog_item, auth_tokens):
    access_token, refresh_token = auth_tokens
    user_headers= {
        "Authorization": f"Bearer {access_token}"
    }
    print(test_adding_new_catalog_item)
    response = client.post(
        f"/api/v1/catalog/{test_adding_new_catalog_item["id"]}/update", 
        json=update_dish["updated_dish"], 
        headers=user_headers
    )
    
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)

def test_delete_catalog_item(test_adding_new_catalog_item, auth_tokens):
    access_token, refresh_token = auth_tokens
    user_headers= {
        "Authorization": f"Bearer {access_token}"
    }
    response = client.delete(f"/api/v1/catalog/{test_adding_new_catalog_item["id"]}", headers=user_headers)
    
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)