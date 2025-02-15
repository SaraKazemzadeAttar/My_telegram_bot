import telebot
import logging


def register(bot):
    @bot.message_handler(commands=['send_voice'])
    def send_voice_file(message):
        with open("voices/voice.mp3", 'rb') as voice_file:
            bot.send_voice(chat_id=message.chat.id, voice=voice_file)