import os

from fastapi import APIRouter, HTTPException, status
from pymongo import MongoClient
from dotenv import load_dotenv

from utils import logger


# Load environment variables
load_dotenv()

router = APIRouter()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database("travel_recommendations")
collection = db.get_collection("tasks")


@router.get("/{uid}")
async def get_status(uid: str):
    try:
        task = collection.find_one({"uid": uid})
        if not task:
            logger.warning(f"UID not found: {uid}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UID not found")

        if task["status"] == "pending":
            logger.info(f"Task with UID: {uid} is still pending")
            return {"uid": uid, "status": "pending", "message": "The recommendations are not yet available. Please try again later."}

        logger.info(f"Task with UID: {uid} is completed")
        return task

    except Exception as e:
        logger.error(f"Error while fetching task status for UID: {uid}, error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
