import unittest
import pytest

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestStatus(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup_kafka_producer(self, mock_mongo_client):
        self.mock_mongo_client = mock_mongo_client
        self.mock_collection = MagicMock()
        self.mock_mongo_client.return_value.get_database.return_value.get_collection.return_value = self.mock_collection
        from app.main import app
        self.client = TestClient(app)

    def test_get_status_pending(self):
        # Simulate task pending
        self.mock_collection.find_one.return_value = {
            "uid": "123456",
            "status": "pending",
            "country": "Japan",
            "season": "spring",
            "recommendations": []
        }

        response = self.client.get("/status/123456")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "uid": "123456",
            "status": "pending",
            "message": "The recommendations are not yet available. Please try again later."
        })

    def test_get_status_completed(self):
        self.mock_collection.find_one.return_value = {
            "uid": "123456",
            "status": "completed",
            "country": "Japan",
            "season": "spring",
            "recommendations": [
                "Visit the cherry blossoms",
                "Attend a traditional tea ceremony",
                "Explore the temples in Kyoto"
            ]
        }

        response = self.client.get("/status/123456")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "uid": "123456",
            "status": "completed",
            "country": "Japan",
            "season": "spring",
            "recommendations": [
                "Visit the cherry blossoms",
                "Attend a traditional tea ceremony",
                "Explore the temples in Kyoto"
            ]
        })

    def test_get_status_internal_error(self):
        self.mock_collection.find_one.side_effect = Exception("MongoDB error")

        response = self.client.get("/status/123456")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Internal Server Error"})

