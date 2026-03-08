import pytest


class TestUnregisterSuccess:
    """Tests for successful unregister scenarios."""
    
    def test_unregister_existing_participant(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        email = "alice@test.edu"  # Already signed up
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email not in participants
    
    def test_unregister_decrements_participant_list(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        email = "alice@test.edu"
        initial_count = 1
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert - verify count decreased
        activities_response = client.get("/activities")
        new_count = len(activities_response.json()[activity_name]["participants"])
        assert new_count == initial_count - 1


class TestUnregisterNotFound:
    """Tests for unregister errors."""
    
    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@test.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_non_participant_returns_400(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        email = "notregistered@test.edu"  # Not signed up
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Not registered for this activity"
    
    def test_unregister_non_participant_does_not_remove(self, client, reset_activities):
        # Arrange
        activity_name = "Test Club"
        email = "notregistered@test.edu"
        initial_participants = ["alice@test.edu"]
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert - participant list unchanged
        activities_response = client.get("/activities")
        final_participants = activities_response.json()[activity_name]["participants"]
        assert final_participants == initial_participants
