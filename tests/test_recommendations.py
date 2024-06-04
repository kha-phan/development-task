import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_kafka_producer(mocker):
    mocker.patch('app.api.recommendations.producer.send', return_value=None)


@pytest.fixture
def mock_mongodb(mocker):
    mocker.patch('app.api.recommendations.collection.insert_one', return_value=None)


@patch("uuid.uuid4", return_value="1234567890abcdef")
def test_get_recommendations(mock_uuid, mock_kafka_producer, mock_mongodb):
    response = client.get("/recommendations/?country=Canada&season=winter")
    assert response.status_code == 200
    assert response.json() == {"uid": "1234567890abcdef"}
