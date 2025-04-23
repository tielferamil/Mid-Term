from beanie import Document
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId


# User document stored in MongoDB
class User(Document):
    username: str
    hashed_password: str

    class Settings:
        name = "users"  # MongoDB collection name


# Request schemas (not stored directly)
class UserSignup(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# A food item from frontend
class FoodItem(BaseModel):
    name: str
    calories: int


# Food log stored per user
class FoodLog(Document):
    user_id: ObjectId
    name: str
    calories: int

    class Settings:
        name = "foodlogs"  # MongoDB collection name
