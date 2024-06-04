import os
import openai
import json
import time

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client.travel_recommendations
collection = db.recommendations

# Initialize Kafka consumer with retries
while True:
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='travel_recommendations_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("Connected to Kafka")
        break
    except KafkaError as e:
        print(f"Failed to connect to Kafka: {e}")
        time.sleep(5)  # Wait before retrying

# Process messages from Kafka
for message in consumer:
    data = message.value
    uid = data["uid"]
    country = data["country"]
    season = data["season"]

    # Call OpenAI API to get recommendations
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Recommend three things to do in {country} during {season}.",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,

    )
    recommendations = response.choices[0].text.strip().split('\n')

    # Update MongoDB with recommendations
    collection.update_one(
        {"uid": uid},
        {"$set": {"recommendations": recommendations, "status": "completed"}}
    )
    print(f"Processed recommendations for UID: {uid}")
