import unittest
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestRecommendations(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup_kafka_producer(self, mock_kafka_producer, mock_mongo_client):
        self.mock_kafka_producer = mock_kafka_producer

        self.mock_mongo_client = mock_mongo_client
        self.mock_collection = MagicMock()
        self.mock_mongo_client.return_value.get_database.return_value.get_collection.return_value = self.mock_collection
        from app.main import app
        self.client = TestClient(app)

    def test_get_recommendations_invalid_season(self):
        from app.main import app
        client = TestClient(app)

        response = client.get("/recommendations/?country=Japan&season=invalid")

        self.assertEqual(response.status_code, 422)

    def test_get_recommendations_mongo_failure(self):
        self.mock_collection.insert_one.side_effect = Exception("MongoDB error")

        response = self.client.get("/recommendations/?country=Paris&season=spring")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Internal Server Error")
