import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Your Flask API URL

@pytest.fixture
def test_user():
    """Fixture to create test user credentials."""
    return {"username": "testuser2", "password": "testpass"}

def test_logout_flow(test_user):
    """Test login, logout, and token invalidation."""


    requests.post(f"{BASE_URL}/register", json=test_user)


    login_response = requests.post(f"{BASE_URL}/login", json=test_user)
    assert login_response.status_code == 200
    token = login_response.json().get("token")
    assert token is not None


    headers = {"Authorization": f"Bearer {token}"}
    home_response = requests.get(f"{BASE_URL}/home", headers=headers)
    assert home_response.status_code == 200  # ✅ Access should be granted


    logout_response = requests.post(f"{BASE_URL}/logout", headers=headers)
    assert logout_response.status_code == 200  # ✅ Logout should be successful


    invalid_home_response = requests.get(f"{BASE_URL}/home", headers=headers)
    assert invalid_home_response.status_code == 401  # ❌ Should be Unauthorized

    print("✅ Logout test passed! Token invalidation works as expected.")

