from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()

# enables CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# data model for a food item
class FoodItem(BaseModel):
    name: str
    calories: int


# data model for calorie tracking
class CalorieData(BaseModel):
    target: int = 0
    foods: List[FoodItem] = []
    totalCalories: int = 0


# in-memory database for calorie data
calorie_data = CalorieData()


# serve the frontend HTML file
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("frontend/index.html", "r") as file:
        return HTMLResponse(content=file.read())


# set the daily calorie target
@app.post("/calories/target")
def set_calorie_target(target: int):
    calorie_data.target = target
    return {"message": "Calorie target set", "target": target}


# logs a new food item
@app.post("/calories/log")
def log_food(food: FoodItem):
    calorie_data.foods.append(food)
    calorie_data.totalCalories += food.calories
    return {"message": "Food logged", "food": food}


# updates an existing food item
@app.put("/calories/log/{food_id}")
def update_food(food_id: int, updated_food: FoodItem):
    if food_id < 0 or food_id >= len(calorie_data.foods):
        raise HTTPException(status_code=404, detail="Food item not found")

    # subtracts the old calories before updating
    calorie_data.totalCalories -= calorie_data.foods[food_id].calories

    # updates the food item
    calorie_data.foods[food_id] = updated_food

    # adds the new calories
    calorie_data.totalCalories += updated_food.calories

    return {"message": "Food updated", "food": updated_food}


# deletes a food item
@app.delete("/calories/log/{food_id}")
def delete_food(food_id: int):
    if food_id < 0 or food_id >= len(calorie_data.foods):
        raise HTTPException(status_code=404, detail="Food item not found")

    # subtracts the calories of the deleted food item
    deleted_food = calorie_data.foods.pop(food_id)
    calorie_data.totalCalories -= deleted_food.calories

    return {"message": "Food deleted", "food": deleted_food}


# retrieves all calorie data
@app.get("/calories/")
def get_calories():
    return calorie_data


# resets all calorie data
@app.delete("/calories/reset")
def reset_calories():
    calorie_data.target = 0
    calorie_data.foods = []
    calorie_data.totalCalories = 0
    return {"message": "Calorie data reset"}
