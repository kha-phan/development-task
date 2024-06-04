import os
import json

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from uuid import uuid4
from pymongo import MongoClient
from kafka import KafkaProducer
from dotenv import load_dotenv

from utils import logger

router = APIRouter()

# Load environment variables
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database("travel_recommendations")
collection = db.get_collection("tasks")

producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))


@router.get("/")
async def get_recommendations(country: str = Query(...), season: str = Query(..., regex="^(spring|summer|fall|winter)$")):
    try:
        uid = str(uuid4())
        country = country.lower()
        season = season.lower()

        task = {
            "uid": uid,
            "country": country,
            "season": season,
            "status": "pending",
            "recommendations": []
        }
        collection.insert_one(jsonable_encoder(task))
        producer.send(os.getenv("KAFKA_TOPIC"), json.dumps(task).encode("utf-8"))
        logger.info(f"Task created with UID: {uid} for country: {country}, season: {season}")
        return {"uid": uid}

    except Exception as e:
        logger.error(f"Error while creating task: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
