import telebot
import logging
from telebot.types import ChatPermissions

def register(bot):
    def is_Admin(message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        try:
            user_info = bot.get_chat_member(chat_id, user_id)
            return user_info.status in ["creator", "administrator"]
        except Exception:
            return False  # If error occurs, assume user is not an admin

    @bot.message_handler(commands=['pin'])
    def pin_message(message):
        if not is_Admin(message):
            bot.reply_to(message, "You must be an admin to pin messages!")
            return
        
        if not message.reply_to_message:
            bot.reply_to(message, "Reply to the message you want to pin with /pin.")
            return

        try:
            bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
            bot.reply_to(message, "Message pinned successfully!")
        except Exception as e:
            bot.reply_to(message, f"Failed to pin message: {str(e)}")

