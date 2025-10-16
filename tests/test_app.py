import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]


def test_signup_for_activity_duplicate():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]


def test_unregister_from_activity_not_registered():
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
