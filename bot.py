from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import pymongo
import datetime
from config import BOT_TOKEN, MONGO_URL, FREE_LIMIT, PREMIUM_LIMIT, OWNER_ID, PAYMENT_QR_IMAGE, FORCE_SUBSCRIBE, AUTO_DELETE

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URL)
db = client["telegram_bot"]
users_col = db["users"]
videos_col = db["videos"]

# Start command
def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    user = users_col.find_one({"user_id": user_id})
    
    if not user:
        users_col.insert_one({"user_id": user_id, "premium": False, "daily_count": 0, "last_reset": datetime.datetime.utcnow()})
    
    keyboard = [[InlineKeyboardButton("🔍 Browse Videos", callback_data="browse_videos")]]
    if FORCE_SUBSCRIBE:
        keyboard.append([InlineKeyboardButton("📢 Join Channel", url="https://t.me/your_channel")])
    
    update.message.reply_text("Welcome to the Video Bot!", reply_markup=InlineKeyboardMarkup(keyboard))

# Browse videos
def browse_videos(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat_id
    user = users_col.find_one({"user_id": user_id})

    if user["daily_count"] >= (PREMIUM_LIMIT if user["premium"] else FREE_LIMIT):
        query.message.reply_text("You have reached your daily limit!")
        return

    videos = list(videos_col.find().limit(10))
    buttons = [[InlineKeyboardButton(v["title"], callback_data=f"video_{v['_id']}")] for v in videos]
    query.message.reply_text("Choose a video:", reply_markup=InlineKeyboardMarkup(buttons))

# Fetch and send video
def send_video(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.message.chat_id
    video_id = query.data.split("_")[1]
    
    user = users_col.find_one({"user_id": user_id})
    video = videos_col.find_one({"_id": video_id})

    if user["daily_count"] >= (PREMIUM_LIMIT if user["premium"] else FREE_LIMIT):
        query.message.reply_text("You have reached your daily limit!")
        return

    context.bot.send_video(chat_id=user_id, video=video["file_id"])
    users_col.update_one({"user_id": user_id}, {"$inc": {"daily_count": 1}})

    if AUTO_DELETE:
        context.bot.delete_message(chat_id=user_id, message_id=query.message.message_id)

# Payment command
def payment(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("📞 Contact Owner", url=f"tg://user?id={OWNER_ID}")]]
    update.message.reply_photo(PAYMENT_QR_IMAGE, caption="Scan the QR code to pay!", reply_markup=InlineKeyboardMarkup(keyboard))

# Command handlers
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("payment", payment))
    dp.add_handler(CallbackQueryHandler(browse_videos, pattern="browse_videos"))
    dp.add_handler(CallbackQueryHandler(send_video, pattern="video_.*"))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
