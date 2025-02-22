# RANDOM-CHATAI

📺 Telegram Video Fetcher Bot  

A powerful Telegram bot that fetches and delivers videos indexed from Telegram channels. It supports **premium subscriptions, auto-delete, force subscription, and MongoDB indexing**.  

---

✨ FEATURES  
✅ Fetch videos from indexed Telegram channels  
✅ MongoDB Integration for storing user & video data  
✅ Premium System (free & paid plans)  
✅ Force Subscribe (require users to join a channel)  
✅ Auto-delete videos after sending  
✅ Admin Controls (add/remove premium users)  
✅ Manual Payment System (QR code & contact owner)  

---

🛠 INSTALLATION & DEPLOYMENT  

1️⃣ INSTALL DEPENDENCIES  
Make sure Python is installed, then run:  
pip install python-telegram-bot pymongo  

2️⃣ CONFIGURE THE BOT  
Edit the `config.py` file with your **Bot Token** and **MongoDB URL**.  

3️⃣ RUN THE BOT LOCALLY  
Test the bot on your machine before deployment:  
python bot.py  

---

🚀 DEPLOY TO KOYEB  
This bot is optimized for **Koyeb cloud hosting**.  

STEPS TO DEPLOY ON KOYEB  
1️⃣ Go to [Koyeb](https://www.koyeb.com/) and Sign Up  
2️⃣ Create a New Service  
   - Select **GitHub Deployment** (if your code is on GitHub)  
   - Or choose **Docker Image** (if using Docker)  
3️⃣ Set Environment Variables:  
   - BOT_TOKEN = Your Telegram Bot Token  
   - MONGO_URL = Your MongoDB Connection String  
4️⃣ Deploy & Run the Bot! 🎉  

---

🔥 BOT COMMANDS  
/start - Start the bot  
/payment - Show payment QR code & contact owner  
/browse - Browse available videos  
/admin - Admin panel to manage users  

---

🛒 PREMIUM SUBSCRIPTION  
- **Free Users:** 5 videos per day, max 5-minute length  
- **Premium Users:** 30 videos per day, unlimited length  
- **Pricing:**  
  - 1 Month: ₹50  
  - 2 Months: ₹90  
  - 3 Months: ₹130  

To upgrade, scan the QR code and contact the owner!  

---

📞 SUPPORT & CONTACT  
For any issues, contact the **Bot Owner** directly on Telegram.  

---

🌟 Star this repository if you find it useful! 🌟
