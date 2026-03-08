import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture that provides a TestClient for making requests to the app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture that resets activities to a known test state before each test.
    Clears real data and replaces with minimal test data.
    """
    # Store original state
    original_activities = dict(activities)
    
    # Clear and set up test activities
    activities.clear()
    activities.update({
        "Test Club": {
            "description": "A test activity",
            "schedule": "Mondays, 3:00 PM - 4:00 PM",
            "max_participants": 2,
            "participants": ["alice@test.edu"]
        },
        "Full Activity": {
            "description": "An activity at capacity",
            "schedule": "Tuesdays, 3:00 PM - 4:00 PM",
            "max_participants": 2,
            "participants": ["bob@test.edu", "charlie@test.edu"]
        }
    })
    
    yield
    
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)
