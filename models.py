from pydantic import BaseModel
from typing import List
from typing import Optional
from beanie import Document


# model for a food item
class FoodItem(BaseModel):
    name: str
    calories: int
    recipe: Optional[str] = None


# model for calorie tracking data
class CalorieData(BaseModel):
    target: int = 0
    foods: List[FoodItem] = []
    totalCalories: int = 0


# Define user model
class User(Document):
    username: str
    hashed_password: str

    class Settings:
        name = "users"


class UserSignup(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
