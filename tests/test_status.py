import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_mongodb(mocker):
    mocker.patch('app.api.status.collection.find_one', return_value=None)


def test_get_status_pending(mock_mongodb):
    with patch('app.api.status.collection.find_one', return_value={
        "uid": "1234567890abcdef",
        "country": "Canada",
        "season": "winter",
        "status": "pending",
        "recommendations": []
    }):
        response = client.get("/status/1234567890abcdef")
        assert response.status_code == 200
        assert response.json() == {
            "uid": "1234567890abcdef",
            "status": "pending",
            "message": "The recommendations are not yet available. Please try again later."
        }


def test_get_status_completed(mock_mongodb):
    with patch('app.api.status.collection.find_one', return_value={
        "uid": "1234567890abcdef",
        "country": "Canada",
        "season": "winter",
        "status": "completed",
        "recommendations": ["Go skiing in Whistler.", "Experience the Northern Lights in Yukon.", "Visit the Quebec Winter Carnival."]
    }):
        response = client.get("/status/1234567890abcdef")
        assert response.status_code == 200
        assert response.json() == {
            "uid": "1234567890abcdef",
            "country": "Canada",
            "season": "winter",
            "status": "completed",
            "recommendations": ["Go skiing in Whistler.", "Experience the Northern Lights in Yukon.", "Visit the Quebec Winter Carnival."]
        }


def test_get_status_not_found(mock_mongodb):
    with patch('app.api.status.collection.find_one', return_value=None):
        response = client.get("/status/unknown")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "UID not found"
        }
