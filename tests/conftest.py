"""
Pytest configuration and shared fixtures for FastAPI tests.

This module provides fixtures for:
- TestClient instance for API testing
- State management (reset in-memory activities data)
- Sample test data (emails, activity names)
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities state for resetting between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Strategic board game club",
        "schedule": "Tuesdays 3-5pm",
        "max_participants": 20,
        "participants": []
    },
    "Programming Club": {
        "description": "Learn to code and build projects",
        "schedule": "Mondays 4-6pm",
        "max_participants": 25,
        "participants": []
    },
    "Gym Class": {
        "description": "Physical fitness and exercise",
        "schedule": "Daily 7-8am",
        "max_participants": 30,
        "participants": []
    },
    "Basketball Team": {
        "description": "Competitive basketball team",
        "schedule": "Wednesdays and Fridays 5-7pm",
        "max_participants": 15,
        "participants": []
    },
    "Tennis Club": {
        "description": "Tennis practice and matches",
        "schedule": "Thursdays 4-6pm",
        "max_participants": 20,
        "participants": []
    },
    "Art Studio": {
        "description": "Creative arts and painting",
        "schedule": "Tuesdays and Thursdays 3-5pm",
        "max_participants": 15,
        "participants": []
    },
    "Music Band": {
        "description": "School band and music practice",
        "schedule": "Mondays and Wednesdays 4-6pm",
        "max_participants": 30,
        "participants": []
    },
    "Debate Team": {
        "description": "Competitive debate and public speaking",
        "schedule": "Fridays 3-5pm",
        "max_participants": 20,
        "participants": []
    },
    "Science Club": {
        "description": "Science experiments and projects",
        "schedule": "Wednesdays 3-5pm",
        "max_participants": 25,
        "participants": []
    }
}


@pytest.fixture
def client():
    """
    Provide a FastAPI TestClient instance for testing API endpoints.
    
    Returns:
        TestClient: FastAPI test client for making HTTP requests
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset the in-memory activities dictionary to its original state after each test.
    
    This fixture runs automatically for every test (autouse=True) to ensure
    test isolation and prevent state pollution between tests.
    
    Yields after test execution to perform cleanup.
    """
    # Setup: Tests run here (yield gives control to the test)
    yield
    
    # Teardown: Reset activities to original state after each test
    activities.clear()
    for activity_name, activity_data in ORIGINAL_ACTIVITIES.items():
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": []  # Always start with empty participants list
        }


@pytest.fixture
def sample_emails():
    """
    Provide a list of sample email addresses for testing signup/unregister operations.
    
    Returns:
        list[str]: List of test email addresses
    """
    return [
        "student1@school.edu",
        "student2@school.edu",
        "student3@school.edu",
        "test@example.com",
        "alice@school.edu",
        "bob@school.edu"
    ]


@pytest.fixture
def activity_names():
    """
    Provide a list of valid activity names for parametrized tests.
    
    Returns:
        list[str]: List of all activity names in the system
    """
    return list(ORIGINAL_ACTIVITIES.keys())


@pytest.fixture
def filled_activity(client):
    """
    Create an activity that is at maximum capacity for testing full activity scenarios.
    
    This fixture fills the Chess Club to its maximum capacity (20 participants).
    
    Args:
        client: FastAPI TestClient fixture
    
    Returns:
        dict: Activity name and max participants info
    """
    activity_name = "Chess Club"
    max_participants = ORIGINAL_ACTIVITIES[activity_name]["max_participants"]
    
    # Fill the activity to maximum capacity
    for i in range(max_participants):
        email = f"student{i}@school.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    return {
        "name": activity_name,
        "max_participants": max_participants
    }
