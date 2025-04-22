from pymongo import MongoClient
from database import users_collection
from fastapi import HTTPException

client = MongoClient(
    "mongodb+srv://tielferamil:KHp0Wvip8ohKtawk@cluster0.9mh9yk6.mongodb.net/"
)
db = client["nutritrack"]
users_collection = db["users"]


@app.get("/test-db")
def test_db_connection():
    try:
        count = users_collection.count_documents({})
        return {"status": "success", "user_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
