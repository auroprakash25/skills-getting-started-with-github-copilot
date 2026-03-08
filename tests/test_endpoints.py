import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        # Arrange - root endpoint should redirect to /static/index.html
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        # Arrange
        expected_activity_count = 2  # Test Club and Full Activity
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert "Test Club" in data
        assert "Full Activity" in data
    
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        # Arrange
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in data.items():
            assert set(activity_details.keys()) == expected_keys
    
    def test_get_activities_shows_current_participants(self, client, reset_activities):
        # Arrange
        expected_test_club_participants = ["alice@test.edu"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert data["Test Club"]["participants"] == expected_test_club_participants
