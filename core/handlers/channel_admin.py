import telebot
import logging
from telebot.types import ChatPermissions
# use the channel id for public channels and use the @chatIDrobot bot to get channel_id of private or public channels
CHANNEL_ID = "-1002319708853"

def register(bot):
    @bot.message_handler(commands=["send"])
    def send_in_channel(message):
        bot.send_message(CHANNEL_ID , "Hello , This is the first message in my channel! ")