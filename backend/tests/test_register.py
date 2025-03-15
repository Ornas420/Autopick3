import pytest
import sys
import os

# Add backend directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, User, bcrypt  # Now it should work
from flask import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def client():
    """Creates a test client for Flask and sets up a test database."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_success(client):
    """Test user registration with valid credentials."""
    response = client.post(
        "/register",
        data=json.dumps({"username": "newuser", "password": "newpass"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json["message"] == "User registered successfully"

    # Verify user exists in the database
    with app.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None
        assert bcrypt.check_password_hash(user.password, "newpass")  # Check hashed password

def test_register_existing_user(client):
    """Test registration failure when the username already exists."""
    # First, register a user
    client.post(
        "/register",
        data=json.dumps({"username": "existinguser", "password": "password123"}),
        content_type="application/json",
    )

    # Attempt to register again with the same username
    response = client.post(
        "/register",
        data=json.dumps({"username": "existinguser", "password": "password123"}),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Username already exists"


