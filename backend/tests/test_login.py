import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, User, bcrypt

from flask import json

@pytest.fixture
def client():
    """Creates a test client for Flask."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user with a hashed password
            hashed_password = bcrypt.generate_password_hash("testpass").decode("utf-8")
            test_user = User(username="testuser", password=hashed_password)
            db.session.add(test_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_login_success(client):
    """Test successful login with correct credentials."""
    response = client.post(
        "/login",
        data=json.dumps({"username": "testuser", "password": "testpass"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert "token" in response.json  # Ensure token is returned

def test_login_failure(client):
    """Test login failure with incorrect credentials."""
    response = client.post(
        "/login",
        data=json.dumps({"username": "wronguser", "password": "wrongpass"}),
        content_type="application/json",
    )
    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Invalid username or password"
