from pymongo import MongoClient
from database import users_collection
from fastapi import HTTPException
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models import User

client = MongoClient(
    "mongodb+srv://tielferamil:KHp0Wvip8ohKtawk@cluster0.9mh9yk6.mongodb.net/"
)
db = client["nutritrack"]
users_collection = db["users"]


async def init_db():
    client = AsyncIOMotorClient("mongodb+srv://<your-atlas-connection-string>")
    await init_beanie(database=client.nutritrack, document_models=[User])
