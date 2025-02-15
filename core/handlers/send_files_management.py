import telebot
import logging


def register(bot):
    @bot.message_handler(commands=['send_voice'])
    def send_voice_file(message):
        with open("voices/voice.mp3", 'rb') as voice_file:
            bot.send_voice(chat_id=message.chat.id, voice=voice_file)
            bot.send_chat_action(message.chat.id , action ="upload_voice")
            
    @bot.message_handler(commands=['send_video'])
    def send_video_file(message):
        with open("videos/video.mp4", 'rb') as video_file:
            bot.send_video(chat_id=message.chat.id, video=video_file)
            bot.send_chat_action(message.chat.id , action ="upload_video")
            
    @bot.message_handler(commands=['send_document'])
    def send_document_file(message):
        with open("docs/document.pdf", 'rb') as doc_file:
            bot.send_document(chat_id=message.chat.id,  document=doc_file)
            bot.send_chat_action(message.chat.id , action ="upload_document")
            
    @bot.message_handler(commands=['send_photo'])
    def send_photo_file(message):
        with open("photos/photo.jpg", 'rb') as photo_file:
            bot.send_chat_action(message.chat.id , action ="upload_photo")
            bot.send_document(chat_id=message.chat.id,  document=photo_file)
            bot.send_photo(chat_id=message.chat.id,photo = photo_file)