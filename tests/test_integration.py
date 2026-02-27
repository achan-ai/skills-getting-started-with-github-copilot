"""
Integration tests for FastAPI High School Activity Management API.

Tests all endpoints with success and error scenarios:
- GET /activities - List all activities
- POST /activities/{activity_name}/signup - Sign up for an activity
- DELETE /activities/{activity_name}/participants - Unregister from an activity
- GET / - Root redirect

Tests also verify proper state management and URL encoding.
"""

import pytest
from urllib.parse import quote


@pytest.mark.integration
class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_all_activities_success(self, client):
        """Test that GET /activities returns all 9 activities with correct structure."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify correct number of activities
        assert len(data) == 9
        
        # Verify all activities have required fields
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in data.items():
            assert required_fields.issubset(set(activity_data.keys()))
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_includes_expected_activities(self, client, activity_names):
        """Test that all expected activities are present in the response."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name in activity_names:
            assert activity_name in data
    
    def test_get_activities_initial_participants_empty(self, client):
        """Test that all activities start with empty participants list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert activity_data["participants"] == []


@pytest.mark.integration
class TestActivitySignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_success(self, client, sample_emails):
        """Test successful signup to an activity."""
        email = sample_emails[0]
        activity_name = "Chess Club"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        assert response.json() == {
            "message": f"Signed up {email} for {activity_name}"
        }
        
        # Verify the participant was actually added
        get_response = client.get("/activities")
        activities_data = get_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_with_url_encoded_activity_name(self, client, sample_emails):
        """Test signup with URL-encoded activity name (spaces in name)."""
        email = sample_emails[0]
        activity_name = "Programming Club"  # Has space in name
        encoded_name = quote(activity_name)
        
        response = client.post(
            f"/activities/{encoded_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        
        # Verify participant was added
        get_response = client.get("/activities")
        activities_data = get_response.json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_signup_multiple_students_same_activity(self, client, sample_emails):
        """Test multiple students can sign up for the same activity."""
        activity_name = "Basketball Team"
        
        # Sign up three different students
        for email in sample_emails[:3]:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all three are in participants list
        get_response = client.get("/activities")
        activities_data = get_response.json()
        participants = activities_data[activity_name]["participants"]
        
        assert len(participants) == 3
        for email in sample_emails[:3]:
            assert email in participants
    
    def test_signup_activity_not_found(self, client, sample_emails):
        """Test signup to non-existent activity returns 404."""
        email = sample_emails[0]
        invalid_activity = "Nonexistent Club"
        
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_already_registered(self, client, sample_emails):
        """Test signing up when already registered returns 400."""
        email = sample_emails[0]
        activity_name = "Tennis Club"
        
        # First signup - should succeed
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup with same email - should fail
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"].lower()
    
    def test_signup_activity_full(self, client, filled_activity):
        """Test signup to a full activity returns 400."""
        activity_name = filled_activity["name"]
        new_email = "latestudent@school.edu"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        assert response.status_code == 400
        assert "is full" in response.json()["detail"].lower()
    
    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Club",
        "Art Studio"
    ])
    def test_signup_different_activities_parametrized(self, client, sample_emails, activity_name):
        """Test signup works for different activities (parametrized test)."""
        email = sample_emails[0]
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        assert activity_name in response.json()["message"]


@pytest.mark.integration
class TestActivityUnregister:
    """Tests for DELETE /activities/{activity_name}/participants endpoint."""
    
    def test_unregister_success(self, client, sample_emails):
        """Test successful unregistration from an activity."""
        email = sample_emails[0]
        activity_name = "Music Band"
        
        # First, sign up
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Then, unregister
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        assert response.status_code == 200
        assert response.json() == {
            "message": f"Unregistered {email} from {activity_name}"
        }
        
        # Verify the participant was actually removed
        get_response = client.get("/activities")
        activities_data = get_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_unregister_with_url_encoded_activity_name(self, client, sample_emails):
        """Test unregister with URL-encoded activity name."""
        email = sample_emails[0]
        activity_name = "Science Club"
        encoded_name = quote(activity_name)
        
        # Sign up first
        client.post(f"/activities/{encoded_name}/signup", params={"email": email})
        
        # Unregister with encoded name
        response = client.delete(
            f"/activities/{encoded_name}/participants",
            params={"email": email}
        )
        
        assert response.status_code == 200
        
        # Verify removed
        get_response = client.get("/activities")
        activities_data = get_response.json()
        assert email not in activities_data[activity_name]["participants"]
    
    def test_unregister_activity_not_found(self, client, sample_emails):
        """Test unregister from non-existent activity returns 404."""
        email = sample_emails[0]
        invalid_activity = "Fake Club"
        
        response = client.delete(
            f"/activities/{invalid_activity}/participants",
            params={"email": email}
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_participant_not_found(self, client, sample_emails):
        """Test unregister when not registered returns 404."""
        email = sample_emails[0]
        activity_name = "Debate Team"
        
        # Try to unregister without signing up first
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        assert response.status_code == 404
        assert "participant not found" in response.json()["detail"].lower()
    
    def test_unregister_removes_correct_participant(self, client, sample_emails):
        """Test that unregistering removes only the specified participant."""
        activity_name = "Gym Class"
        
        # Sign up multiple students
        for email in sample_emails[:3]:
            client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Unregister only the middle one
        email_to_remove = sample_emails[1]
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_remove}
        )
        
        assert response.status_code == 200
        
        # Verify only the correct participant was removed
        get_response = client.get("/activities")
        activities_data = get_response.json()
        participants = activities_data[activity_name]["participants"]
        
        assert email_to_remove not in participants
        assert sample_emails[0] in participants
        assert sample_emails[2] in participants
        assert len(participants) == 2


@pytest.mark.integration
class TestRootEndpoint:
    """Tests for GET / root endpoint."""
    
    def test_root_redirect(self, client):
        """Test that root endpoint returns appropriate response."""
        response = client.get("/", follow_redirects=False)
        
        # FastAPI redirect responses typically return 307 or 200
        assert response.status_code in [200, 307]


@pytest.mark.integration
class TestStateManagement:
    """Tests for verifying state management and test isolation."""
    
    def test_signup_and_unregister_sequence(self, client, sample_emails):
        """Test complete workflow: signup -> verify -> unregister -> verify."""
        email = sample_emails[0]
        activity_name = "Art Studio"
        
        # Step 1: Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Step 2: Verify signup
        get_response1 = client.get("/activities")
        assert email in get_response1.json()[activity_name]["participants"]
        
        # Step 3: Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Step 4: Verify unregistration
        get_response2 = client.get("/activities")
        assert email not in get_response2.json()[activity_name]["participants"]
    
    def test_state_isolation_between_tests(self, client, sample_emails):
        """Test that state is clean at the start of each test (reset_activities fixture)."""
        # This test should always start with empty participants
        # even if previous tests added participants (thanks to reset_activities fixture)
        response = client.get("/activities")
        activities_data = response.json()
        
        for activity_name, activity_data in activities_data.items():
            assert activity_data["participants"] == [], \
                f"Activity {activity_name} should start with empty participants"
    
    def test_multiple_operations_on_same_activity(self, client, sample_emails):
        """Test multiple different operations on the same activity in sequence."""
        activity_name = "Chess Club"
        
        # Add first participant
        client.post(f"/activities/{activity_name}/signup", params={"email": sample_emails[0]})
        
        # Add second participant
        client.post(f"/activities/{activity_name}/signup", params={"email": sample_emails[1]})
        
        # Check both are registered
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        assert len(participants) == 2
        assert sample_emails[0] in participants
        assert sample_emails[1] in participants
        
        # Remove first participant
        client.delete(f"/activities/{activity_name}/participants", params={"email": sample_emails[0]})
        
        # Check only second remains
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        assert len(participants) == 1
        assert sample_emails[0] not in participants
        assert sample_emails[1] in participants
        
        # Add third participant
        client.post(f"/activities/{activity_name}/signup", params={"email": sample_emails[2]})
        
        # Check we now have second and third
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        assert len(participants) == 2
        assert sample_emails[1] in participants
        assert sample_emails[2] in participants
