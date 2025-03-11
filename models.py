from pydantic import BaseModel
from typing import List


# model for a food item
class FoodItem(BaseModel):
    name: str
    calories: int


# model for calorie tracking data
class CalorieData(BaseModel):
    target: int = 0
    foods: List[FoodItem] = []
    totalCalories: int = 0
