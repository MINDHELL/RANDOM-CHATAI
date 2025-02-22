import pymongo
import datetime
from config import MONGO_URL

client = pymongo.MongoClient(MONGO_URL)
db = client["telegram_bot"]
users_col = db["users"]
videos_col = db["videos"]

# Add a new user
def add_user(user_id):
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id, "premium": False, "daily_count": 0, "last_reset": datetime.datetime.utcnow()})

# Check if user is premium
def is_premium(user_id):
    user = users_col.find_one({"user_id": user_id})
    return user["premium"] if user else False

# Update user subscription
def set_premium(user_id, status):
    users_col.update_one({"user_id": user_id}, {"$set": {"premium": status}})

# Reset daily limits
def reset_daily_limits():
    users_col.update_many({}, {"$set": {"daily_count": 0, "last_reset": datetime.datetime.utcnow()}})

# Add video to database
def add_video(file_id, title):
    videos_col.insert_one({"file_id": file_id, "title": title})

# Get all videos
def get_videos():
    return list(videos_col.find().limit(10))
