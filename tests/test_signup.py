import pytest


class TestSignupSuccess:
    """Tests for successful signup scenarios."""
    
    def test_signup_new_student_to_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        email = "newstudent@test.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email in participants
    
    def test_signup_increments_participant_list(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        initial_count = 1  # alice@test.edu already signed up
        new_email = "david@test.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert - verify count increased
        activities_response = client.get("/activities")
        new_count = len(activities_response.json()[activity_name]["participants"])
        assert new_count == initial_count + 1


class TestSignupDuplicateErrors:
    """Tests for duplicate signup prevention."""
    
    def test_signup_duplicate_email_returns_400(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        email = "alice@test.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Already signed up for this activity"
    
    def test_duplicate_signup_does_not_add_participant(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        email = "alice@test.edu"
        initial_participants = ["alice@test.edu"]
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert - participant list unchanged
        activities_response = client.get("/activities")
        final_participants = activities_response.json()[activity_name]["participants"]
        assert final_participants == initial_participants


class TestSignupActivityNotFound:
    """Tests for signup to non-existent activity."""
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@test.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestSignupCapacityLimitError:
    """Tests for signup with capacity limit."""
    
    def test_signup_at_capacity_returns_400(self, client, reset_activities):
        # Arrange
        activity_name = "Full Activity"  # Has 2 participants, max 2
        email = "newstudent@test.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is at maximum capacity"
    
    def test_capacity_limit_prevents_signup(self, client, reset_activities):
        # Arrange
        activity_name = "Full Activity"
        email = "newstudent@test.edu"
        initial_participant_count = 2
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert - participant count should not increase
        activities_response = client.get("/activities")
        final_count = len(activities_response.json()[activity_name]["participants"])
        assert final_count == initial_participant_count
