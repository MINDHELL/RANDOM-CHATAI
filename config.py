import os

BOT_TOKEN = os.getenv("7725707727:AAFtx6Sy-q6GgB9eaPoN2-oYPx2D6hjnc1g")  # Get from environment variables

# MongoDB Configuration
MONGO_URL = os.getenv("mongodb+srv://aarshhub:6L1PAPikOnAIHIRA@cluster0.6shiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  
DATABASE_NAME = os.getenv("Randomai2")  

# Force Subscription (FSub)
FORCE_SUBSCRIBE = os.getenv("FORCE_SUBSCRIBE", "True").lower() == "true"  
FSUB_CHANNEL_ID = int(os.getenv("FSUB_CHANNEL_ID", "-1002490575006"))  

# Video Indexing Channel
INDEX_CHANNEL_ID = int(os.getenv("INDEX_CHANNEL_ID", "-1002492623985"))  

# Premium System
FREE_LIMIT = int(os.getenv("FREE_LIMIT", "5"))  
PREMIUM_LIMIT = int(os.getenv("PREMIUM_LIMIT", "30"))  

# Auto-Delete File Time (Seconds) - 0 (disabled) to 5 days (432000 seconds)
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "15"))  

# Owner Special Permissions
OWNER_ID = int(os.getenv("OWNER_ID", "6860316927"))
