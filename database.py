from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://tielferamil:KHp0Wvip8ohKtawk@cluster0.xxxxx.mongodb.net/nutritrack?retryWrites=true&w=majority"
)
db = client["nutritrack"]
users_collection = db["users"]
