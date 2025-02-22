import datetime
import pymongo
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import BOT_TOKEN, MONGO_URL, DATABASE_NAME, FORCE_SUBSCRIBE, FSUB_CHANNEL_ID, INDEX_CHANNEL_ID, AUTO_DELETE_TIME, OWNER_ID

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URL)
db = client[DATABASE_NAME]
videos_col = db["videos"]
users_col = db["users"]

# Function to check if the user is subscribed (Owner Bypasses FSub)
def is_user_subscribed(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    if user_id == OWNER_ID:  
        return True  # Owner bypasses FSub
    
    try:
        chat_member = context.bot.get_chat_member(FSUB_CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False  # If bot can't check, assume not subscribed

# Start command
def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    if FORCE_SUBSCRIBE and not is_user_subscribed(update, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{FSUB_CHANNEL_ID}")]]
        update.message.reply_text(
            "🚨 You must join our channel to use this bot!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    update.message.reply_text("✅ Welcome! You can now browse and download videos.")

# Function to index videos from a Telegram channel
def channel_post(update: Update, context: CallbackContext):
    if update.channel_post.chat_id != INDEX_CHANNEL_ID:
        return  # Ignore messages from other channels

    if update.channel_post.video:
        video = update.channel_post.video
        caption = update.channel_post.caption or "Untitled Video"

        if videos_col.find_one({"file_id": video.file_id}):
            return

        videos_col.insert_one({
            "file_id": video.file_id,
            "title": caption,
            "date_added": datetime.datetime.utcnow()
        })

# Function to send videos from the indexed database
def send_video(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    # Owner can send unlimited videos
    if user_id == OWNER_ID:
        videos = list(videos_col.find().limit(10))
    else:
        user_data = users_col.find_one({"user_id": user_id})
        daily_limit = PREMIUM_LIMIT if user_data and user_data.get("is_premium") else FREE_LIMIT
        videos = list(videos_col.find().limit(daily_limit))

    if not videos:
        update.message.reply_text("⚠ No videos available.")
        return

    for video in videos:
        msg = update.message.reply_video(video=video["file_id"], caption=video["title"])
        
        # Auto-delete message after AUTO_DELETE_TIME
        if AUTO_DELETE_TIME > 0:
            time.sleep(1)
            context.job_queue.run_once(
                delete_message, AUTO_DELETE_TIME, context={"chat_id": update.message.chat_id, "message_id": msg.message_id}
            )

# Function to delete messages after the set time
def delete_message(context: CallbackContext):
    job = context.job
    try:
        context.bot.delete_message(job.context["chat_id"], job.context["message_id"])
    except Exception as e:
        print(f"Error deleting message: {e}")

# Owner Command: Add Premium User
def add_premium(update: Update, context: CallbackContext):
    if update.message.chat_id != OWNER_ID:
        return
    
    try:
        user_id = int(context.args[0])
        users_col.update_one({"user_id": user_id}, {"$set": {"is_premium": True}}, upsert=True)
        update.message.reply_text(f"✅ User {user_id} is now a premium user!")
    except:
        update.message.reply_text("⚠ Usage: /addpremium <user_id>")

# Owner Command: Remove Premium User
def remove_premium(update: Update, context: CallbackContext):
    if update.message.chat_id != OWNER_ID:
        return
    
    try:
        user_id = int(context.args[0])
        users_col.update_one({"user_id": user_id}, {"$set": {"is_premium": False}}, upsert=True)
        update.message.reply_text(f"❌ User {user_id} is no longer a premium user!")
    except:
        update.message.reply_text("⚠ Usage: /removepremium <user_id>")

# Main function to run the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    job_queue = updater.job_queue

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("videos", send_video))
    dp.add_handler(CommandHandler("addpremium", add_premium, pass_args=True))
    dp.add_handler(CommandHandler("removepremium", remove_premium, pass_args=True))
    dp.add_handler(MessageHandler(Filters.video, channel_post))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
