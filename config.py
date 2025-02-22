import os

BOT_TOKEN = "YOUR_BOT_TOKEN"
MONGO_URL = "YOUR_MONGODB_URL"

# Subscription settings
FREE_LIMIT = 5  # Free users can fetch 5 files per day
PREMIUM_LIMIT = 30  # Premium users can fetch 30 files per day
FREE_VIDEO_LENGTH = 300  # Max 5 min video for free users (300 sec)
PREMIUM_VIDEO_LENGTH = None  # No limit for premium users

# Payment and Contact Details
OWNER_ID = 123456789  # Your Telegram ID
PAYMENT_QR_IMAGE = "qr.jpg"  # Replace this with your actual QR code file

# Features Control
FORCE_SUBSCRIBE = True  # Enable/Disable force subscription
AUTO_DELETE = True  # Enable/Disable auto file deletion
VERIFICATION_REQUIRED = True  # Enable/Disable manual user verification
