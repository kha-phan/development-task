import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


class TestRecommendations(unittest.TestCase):
    @patch("app.api.recommendations.MongoClient")
    @patch("app.api.recommendations.KafkaProducer")
    def test_get_recommendations_invalid_season(self, mock_mongo_client, mock_kafka_producer):
        from app.main import app
        client = TestClient(app)

        response = client.get("/recommendations/?country=Japan&season=invalid")

        self.assertEqual(response.status_code, 422)

    @patch("app.api.recommendations.MongoClient")
    @patch("app.api.recommendations.KafkaProducer")
    def test_get_recommendations_mongo_failure(self, mock_mongo_client, mock_kafka_producer):
        from app.main import app
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = Exception("MongoDB error")
        mock_mongo_client.return_value = mock_db
        mock_db.get_database.return_value.get_collection.return_value = mock_collection

        client = TestClient(app)

        response = client.get("/recommendations/?country=Paris&season=spring")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Internal Server Error")

    @patch("app.api.recommendations.MongoClient")
    @patch("app.api.recommendations.KafkaProducer")
    def test_get_recommendations_kafka_failure(self, mock_mongo_client, mock_kafka_producer):
        from app.main import app
        # Simulate Kafka send failure
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_mongo_client.return_value = mock_db
        mock_db.get_database.return_value.get_collection.return_value = mock_collection

        mock_producer_instance = MagicMock()
        mock_producer_instance.send.side_effect = Exception("Kafka error")
        mock_kafka_producer.return_value = mock_producer_instance

        client = TestClient(app)

        response = client.get("/recommendations/?country=Paris&season=spring")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Internal Server Error")
