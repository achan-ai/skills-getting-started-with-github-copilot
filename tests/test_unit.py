"""
Unit tests for High School Activity Management API components.

These tests focus on isolated components and data structures
rather than full endpoint integration.
"""

import pytest
from src.app import activities


@pytest.mark.unit
class TestActivitiesDataStructure:
    """Tests for the activities data structure integrity."""
    
    def test_activities_dict_exists(self):
        """Test that activities dictionary is properly initialized."""
        assert activities is not None
        assert isinstance(activities, dict)
    
    def test_activities_has_expected_count(self):
        """Test that activities dictionary contains exactly 9 activities."""
        assert len(activities) == 9
    
    def test_all_activities_have_required_fields(self):
        """Test that each activity has all required fields."""
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), \
                f"Activity {activity_name} should be a dictionary"
            
            missing_fields = required_fields - set(activity_data.keys())
            assert not missing_fields, \
                f"Activity {activity_name} is missing fields: {missing_fields}"
    
    def test_activity_field_types(self):
        """Test that activity fields have correct data types."""
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), \
                f"{activity_name} description should be a string"
            
            assert isinstance(activity_data["schedule"], str), \
                f"{activity_name} schedule should be a string"
            
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"
            
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants should be a list"
    
    def test_max_participants_positive(self):
        """Test that all activities have positive max_participants."""
        for activity_name, activity_data in activities.items():
            assert activity_data["max_participants"] > 0, \
                f"{activity_name} max_participants should be positive"
    
    def test_description_not_empty(self):
        """Test that all activities have non-empty descriptions."""
        for activity_name, activity_data in activities.items():
            assert activity_data["description"].strip(), \
                f"{activity_name} should have a non-empty description"
    
    def test_schedule_not_empty(self):
        """Test that all activities have non-empty schedules."""
        for activity_name, activity_data in activities.items():
            assert activity_data["schedule"].strip(), \
                f"{activity_name} should have a non-empty schedule"
    
    def test_participants_list_elements_are_strings(self):
        """Test that participants list contains only strings (emails)."""
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            for participant in participants:
                assert isinstance(participant, str), \
                    f"Participant in {activity_name} should be a string"
    
    @pytest.mark.parametrize("activity_name,expected_max", [
        ("Chess Club", 20),
        ("Programming Club", 25),
        ("Gym Class", 30),
        ("Basketball Team", 15),
        ("Tennis Club", 20),
        ("Art Studio", 15),
        ("Music Band", 30),
        ("Debate Team", 20),
        ("Science Club", 25)
    ])
    def test_specific_activity_max_participants(self, activity_name, expected_max):
        """Test that specific activities have their expected max_participants values."""
        assert activities[activity_name]["max_participants"] == expected_max


@pytest.mark.unit
class TestActivityNames:
    """Tests for activity name validation and consistency."""
    
    def test_all_expected_activities_exist(self):
        """Test that all expected activities are present in the dictionary."""
        expected_activities = {
            "Chess Club",
            "Programming Club",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Debate Team",
            "Science Club"
        }
        
        actual_activities = set(activities.keys())
        assert actual_activities == expected_activities
    
    def test_activity_names_are_strings(self):
        """Test that all activity names (keys) are strings."""
        for activity_name in activities.keys():
            assert isinstance(activity_name, str)
    
    def test_activity_names_not_empty(self):
        """Test that no activity has an empty name."""
        for activity_name in activities.keys():
            assert activity_name.strip()


@pytest.mark.unit
class TestParticipantsListOperations:
    """Tests for participants list operations (simulated unit tests)."""
    
    def test_participants_list_is_mutable(self):
        """Test that participants list can be modified."""
        activity_name = "Chess Club"
        original_count = len(activities[activity_name]["participants"])
        
        # Add a test participant
        test_email = "unittest@test.com"
        activities[activity_name]["participants"].append(test_email)
        
        # Verify it was added
        assert len(activities[activity_name]["participants"]) == original_count + 1
        assert test_email in activities[activity_name]["participants"]
        
        # Clean up (reset_activities fixture will also handle this)
        activities[activity_name]["participants"].remove(test_email)
    
    def test_participants_list_supports_removal(self):
        """Test that participants can be removed from the list."""
        activity_name = "Programming Club"
        test_email = "remove@test.com"
        
        # Add a participant
        activities[activity_name]["participants"].append(test_email)
        assert test_email in activities[activity_name]["participants"]
        
        # Remove the participant
        activities[activity_name]["participants"].remove(test_email)
        assert test_email not in activities[activity_name]["participants"]
    
    def test_participants_list_allows_duplicates_check(self):
        """Test checking for duplicate participants in a list."""
        test_list = ["email1@test.com", "email2@test.com", "email1@test.com"]
        
        # Verify we can detect duplicates
        assert test_list.count("email1@test.com") == 2
        assert test_list.count("email2@test.com") == 1
        
        # Verify unique check
        unique_emails = set(test_list)
        assert len(unique_emails) == 2
