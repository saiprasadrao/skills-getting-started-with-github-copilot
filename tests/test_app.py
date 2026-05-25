import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activity_data

BASE_ACTIVITIES = copy.deepcopy(activity_data)

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    activity_data.clear()
    activity_data.update(copy.deepcopy(BASE_ACTIVITIES))
    yield


def test_root_redirects_to_index():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_list():
    # Arrange
    expected_activities = BASE_ACTIVITIES

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_activities


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    expected_message = {"message": f"Signed up {email} for {activity_name}"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_message
    assert email in activity_data[activity_name]["participants"]


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_removes_participant():
    # Arrange
    activity_name = "Programming Class"
    email = "unsubscribe@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    expected_message = {"message": f"Unregistered {email} from {activity_name}"}

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_message
    assert email not in activity_data[activity_name]["participants"]


def test_unregister_when_not_signed_up_returns_400():
    # Arrange
    activity_name = "Gym Class"
    email = "notjoined@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
