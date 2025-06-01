import json
import os
import telebot
from web3 import Web3

# 🔹 تنظیمات ربات و بلاکچین
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@benjaminfranklintoken"
CONTRACT_ADDRESS = "0xd5baB4C1b92176f9690c0d2771EDbF18b73b8181"
AIRDROP_WALLET = "0xd5F168CFa6a68C21d7849171D6Aa5DDc9307E544"
WEB3_PROVIDER = "https://bsc-dataseed.binance.org/"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# 🔹 اتصال به تلگرام
bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 بررسی عضویت در کانال
def check_membership(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# 🔹 بررسی اطلاعات کاربر در JSON
def check_user(telegram_id):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
        return str(telegram_id) in users
    except FileNotFoundError:
        return False

# 🔹 ثبت کاربر و ارسال توکن
@bot.message_handler(commands=['start'])
def welcome_user(message):
    user_id = message.chat.id

    if check_membership(user_id):
        if not check_user(user_id):
            invite_link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"
            users = {}
            if os.path.exists("users.json"):
                with open("users.json", "r") as file:
                    users = json.load(file)

            users[str(user_id)] = {"invite_link": invite_link, "tokens_received": 500}
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)

            # ارسال ۵۰۰ توکن
            tx_hash = send_tokens(AIRDROP_WALLET, 500 * (10**18))
            save_transaction(user_id, tx_hash, 500)

            welcome_text = f"✅ خوش آمدید! ۵۰۰ توکن BJF دریافت کردید.\nلینک دعوت شما: {invite_link}\n"
            bot.send_message(user_id, welcome_text)
        else:
            bot.send_message(user_id, "❌ شما قبلاً ثبت نام کرده‌اید!")
    else:
        bot.send_message(user_id, "⚠️ ابتدا باید در کانال @benjaminfranklintoken عضو شوید!")

# 🔹 ذخیره اطلاعات دعوت‌ها
@bot.message_handler(commands=['invite'])
def manage_invite(message):
    inviter_id = message.chat.id
    invitee_id = message.text.split(" ")[1] if len(message.text.split()) > 1 else None

    if invitee_id:
        invites = {}
        if os.path.exists("invites.json"):
            with open("invites.json", "r") as file:
                invites = json.load(file)

        if str(invitee_id) not in invites:
            invites[str(invitee_id)] = {"inviter": inviter_id, "status": "Valid"}
            with open("invites.json", "w") as file:
                json.dump(invites, file, indent=4)

            # ارسال ۱۰۰ توکن
            tx_hash = send_tokens(AIRDROP_WALLET, 100 * (10**18))
            save_transaction(inviter_id, tx_hash, 100)

            bot.send_message(inviter_id, "✅ دعوت موفق! ۱۰۰ توکن BJF به حساب شما ارسال شد.")
        else:
            bot.send_message(inviter_id, "❌ این دعوت قبلاً ثبت شده است.")
    else:
        bot.send_message(inviter_id, "❌ خطا در دریافت شناسه دعوت‌شونده!")

bot.polling()
