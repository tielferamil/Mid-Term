from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://tielferamil:KHp0Wvip8ohKtawk@cluster0.9mh9yk6.mongodb.net/"
)
db = client["nutritrack"]
users_collection = db["users"]
