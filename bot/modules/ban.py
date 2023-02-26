import pymongo
from pyrogram import Client, filters
from pyrogram.types import Message, User

# Set up MongoDB client and connect to database
mongo_client = pymongo.MongoClient("DATABASE_URL")
db = mongo_client["mydatabase"]
banned_users = db["banned_users"]

# Set up Pyrogram client and connect to Telegram API

# Define a command to ban users
@Client.on_message(filters.command("ban") & filters.user(OWNER_ID))
def ban_user(client: Client, message: Message):
    try:
        user_id = message.reply_to_message.from_user.id
        client.kick_chat_member(chat_id=message.chat.id, user_id=user_id)
        banned_users.insert_one({"user_id": user_id})
        message.reply_text(f"{user_id} has been banned.")
    except Exception as e:
        message.reply_text(f"Failed to ban user: {e}")

# Define a command to unban users
@Client.on_message(filters.command("unban") & filters.user(OWNER_ID))
def unban_user(client: Client, message: Message):
    try:
        user_id = message.reply_to_message.from_user.id
        banned_users.delete_one({"user_id": user_id})
        client.unban_chat_member(chat_id=message.chat.id, user_id=user_id)
        message.reply_text(f"{user_id} has been unbanned.")
    except Exception as e:
        message.reply_text(f"Failed to unban user: {e}")

# Define a filter to check whether a user is banned
def is_banned(user_id: int) -> bool:
    return banned_users.find_one({"user_id": user_id}) is not None

# Define a function to handle incoming messages
@Client.on_message(filters.text & ~filters.private)
def handle_message(client: Client, message: Message):
    user_id = message.from_user.id
    if is_banned(user_id):
        message.reply_text("You are banned from using this bot.")
    else:
        # process the message normally
        pass
