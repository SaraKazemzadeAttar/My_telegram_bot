import telebot
import logging
from telebot.types import  InlineKeyboardMarkup , InlineKeyboardButton

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
    
    # if user upload a photo , the bot send photo again with a caption 
    def send_photo_file(message):
        FILE_ID = "AgACAgQAAxkBAAIBqmexBOjoicSl1T0Gz-Z44ua-ut8MAAKKyjEbUBSJUfirODec8kgQAQADAgADeAADNgQ"
        markup = InlineKeyboardMarkup()
        like_Btn = InlineKeyboardButton("👍" , callback_data = "like")
        dislike_Btn = InlineKeyboardButton("👎",callback_data = "dislike")
        markup.add(like_Btn, dislike_Btn) 
        bot.send_photo(message.chat.id,FILE_ID , caption= "این عکس اپلود شد", reply_markup = markup)
            
    @bot.message_handler(content_types=["photo" , "video", "document" , "audio" , "voice"])
    def check_id(message):
        # telebot.logger.info(message.__dict__)
        send_photo_file(message)
        # we need the last file id in json