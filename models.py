from pydantic import BaseModel
from typing import List
from typing import Optional


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
