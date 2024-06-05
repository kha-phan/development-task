import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestStatus(unittest.TestCase):
    @patch("pymongo.MongoClient")
    def test_get_status_pending(self, mock_mongo_client):
        # Mock MongoDB client
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_mongo_client.return_value = mock_db
        mock_db.get_database.return_value.get_collection.return_value = mock_collection

        # Simulate task pending
        mock_collection.find_one.return_value = {
            "uid": "123456",
            "status": "pending",
            "country": "Japan",
            "season": "spring",
            "recommendations": []
        }

        from app.main import app
        client = TestClient(app)
        response = client.get("/status/123456")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "uid": "123456",
            "status": "pending",
            "message": "The recommendations are not yet available. Please try again later."
        })

    @patch("pymongo.MongoClient")
    def test_get_status_completed(self, mock_mongo_client):
        # Mock MongoDB client
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_mongo_client.return_value = mock_db
        mock_db.get_database.return_value.get_collection.return_value = mock_collection

        # Simulate task completed
        mock_collection.find_one.return_value = {
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

        from app.main import app
        client = TestClient(app)

        response = client.get("/status/123456")

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

    @patch("pymongo.MongoClient")
    def test_get_status_internal_error(self, mock_mongo_client):
        # Mock MongoDB client to raise an exception
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.find_one.side_effect = Exception("MongoDB error")
        mock_mongo_client.return_value = mock_db
        mock_db.get_database.return_value.get_collection.return_value = mock_collection

        from app.main import app
        client = TestClient(app)

        response = client.get("/status/123456")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Internal Server Error"})

