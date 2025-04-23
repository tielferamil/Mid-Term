from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from models import UserSignup, UserLogin, User, FoodItem, FoodLog
from auth import hash_password, verify_password, create_access_token, get_current_user
from database import init_db
from beanie import PydanticObjectId

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Load frontend pages
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("frontend/index.html", "r") as f:
        return f.read()


@app.get("/goals", response_class=HTMLResponse)
async def serve_goals():
    with open("frontend/goals.html", "r") as f:
        return f.read()


@app.get("/recipes", response_class=HTMLResponse)
async def serve_recipes():
    with open("frontend/recipes.html", "r") as f:
        return f.read()


@app.get("/profile", response_class=HTMLResponse)
async def serve_profile():
    with open("frontend/profile.html", "r") as f:
        return f.read()


@app.get("/login", response_class=HTMLResponse)
async def serve_login():
    with open("frontend/login.html", "r") as f:
        return f.read()


# DB Init
@app.on_event("startup")
async def start_db():
    await init_db()


# Signup Route
@app.post("/signup")
async def signup(user: UserSignup):
    existing = await User.find_one(User.username == user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed)
    await new_user.insert()
    return {"message": "User created"}


# Login Route
@app.post("/login")
async def login(user: UserLogin):
    db_user = await User.find_one(User.username == user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


# Log Food (authenticated)
@app.post("/calories/log")
async def log_food(food: FoodItem, user: User = Depends(get_current_user)):
    log = FoodLog(user_id=user.id, name=food.name, calories=food.calories)
    await log.insert()
    return {"message": "Food logged"}


# Get Food Logs + Total (authenticated)
@app.get("/calories")
async def get_calories(user: User = Depends(get_current_user)):
    logs = await FoodLog.find(FoodLog.user_id == user.id).to_list()
    total = sum(item.calories for item in logs)
    return {"totalCalories": total, "foods": logs}


# Delete Food Log by ID (optional, advanced)
@app.delete("/calories/log/{log_id}")
async def delete_log(log_id: PydanticObjectId, user: User = Depends(get_current_user)):
    log = await FoodLog.get(log_id)
    if not log or log.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    await log.delete()
    return {"message": "Deleted"}
