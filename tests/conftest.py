import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(scope='session', autouse=True)
def mock_kafka_producer():
    with patch('kafka.KafkaProducer') as mock_kafka_producer:
        mock_producer = MagicMock()
        mock_kafka_producer.return_value = mock_producer
        yield mock_producer


@pytest.fixture(scope='session', autouse=True)
def mock_mongo_client():
    with patch('pymongo.MongoClient') as mock_mongo_client:
        mock_db = MagicMock()
        mock_mongo_client.return_value = mock_db
        yield mock_mongo_client
