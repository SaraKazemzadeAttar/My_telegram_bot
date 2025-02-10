import telebot
import os
import pprint
import json
from telebot import apihelper
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton

logger = telebot.logger
apihelper.ENABLE_MIDDLEWARE = True

telebot.logger.setLevel(logging.INFO)
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("triggered Welcome")
    markup = ReplyKeyboardMarkup(resize_keyboard=True , input_field_placeholder= "انتخاب کن", one_time_keyboard=True)
    markup.add(KeyboardButton('/help') , KeyboardButton('/setname')) # horizental
    # or:
    markup.add(KeyboardButton('Send Audio or Docs'))
    markup.add(KeyboardButton('/Connect_Me'))
    bot.send_message(message.chat.id ,"سلام ! ❤️چه کمکی میتونم بهت بکنم؟ ", reply_markup=markup)
    
@bot.message_handler(func = lambda message: message.text == "Send Audio or Docs")
def message_for_audio_docs(message):
    bot.send_message(message.chat.id , "اینجا میتونی فایل یا صوت آپلود کنی !")
    
@bot.message_handler(commands=['Connect_Me'])
def connect_me(message):
    logger.info("Connection request")
    markup = InlineKeyboardMarkup()
    button_linkedin = InlineKeyboardButton("linkedin",url = "https://www.linkedin.com/in/sara-kazemzade-attar")
    button_github = InlineKeyboardButton("github",url = "https://github.com/SaraKazemzadeAttar")
    button_quit = InlineKeyboardButton("quit",callback_data = "quit")
    markup.add(button_linkedin , button_github)
    bot.send_message(message.chat.id , "میتونی صفحه من رو توی گیت هاب و لینکدین ببینی",reply_markup = markup)
    


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """🌟 **راهنمای ربات** 🌟
    
سلام دوست عزیز! 👋 
این اولین رباتیه که من برای آموزش دیدن راه اندازی کردم  🛠️  

📌 **دستورات قابل استفاده:**  
✅ `/start` - شروع و خوشامدگویی  
✅ `/help` - دریافت راهنمای ربات  
✅ ارسال **"hello"**  
✅ ارسال **"❤️"**   
✅ ارسال کلمه **"سارا"**   

📂 **پشتیبانی از فایل‌ها و صداها:**  
🤖❤️  
    """
    bot.reply_to(message, help_text)


    # print(message)
    # pprint.pprint(message.chat.__dict__ , width = 4)
    # bot.send_message(message.chat.id , json.dumps(message.chat.__dict__, indent = 4 , ensure_ascii = False))
    


@bot.message_handler(commands= ["setname"])
def setup_name(message):
    bot.send_message(message.chat.id , "اسم خودت رو بنویس")
    bot.register_next_step_handler(message , callback = assign_fname)
    
def assign_fname(message,*args, **kwargs):
    logger.info(message.text)
    fname = message.text
    bot.send_message(message.chat.id ,"لطفا فامیلی خودت رو هم بنویس")
    bot.register_next_step_handler(message ,assign_lname , fname)

def assign_lname(message , fname):
    lname = message.text
    bot.send_message(message.chat.id , f"{fname} {lname}  عزیز خوشحالم که به ربات من پیام دادی🩶")


    
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    if message.content_type == "document":
        bot.send_message(message.chat.id, "📄 شما یک **سند (Document)** ارسال کردید!")
        print("It's a document")
    elif message.content_type == "audio":
        bot.send_message(message.chat.id, "🎵 شما یک **فایل صوتی (Audio)** ارسال کردید!")
        print("It's an audio file")
        

@bot.message_handler(regexp = "سارا")
def handle_message(message):
    bot.send_message(message.chat.id ,"سلام سارا! 🩶")

# @bot.message_handler(func=lambda message: message.text =="hello")
# def handle_text_doc(message):   
#     print("triggered")
    
def check_hello(message):
    return message.text == "hello"

@bot.message_handler(func = check_hello)
def handle_text_doc(message):   
	bot.reply_to(message, "hello my friend")

@bot.message_handler(commands=['I love you'])
@bot.message_handler(func=lambda msg: msg.text == "❤️") 
def send_something(message):
    bot.reply_to(message, "I love you too")

@bot.edited_message_handler(func = lambda msg: True)
def trigger_edited(message):
    bot.reply_to(message, "اگر پیام خود را edit کرده ای لطفا دوباره ارسال کن")
    
    
@bot.middleware_handler(update_types =['message'])
def modify_message(bot_instance , message):
    # print(bot_instance.__dict__) # information about bot 
    if message.text is None:
        message.another_text = "No text received."
    else:
        message.another_text = message.text + "  ,You said "
    
@bot.message_handler(func = lambda message :True)
def reply_modified(message):
    bot.reply_to(message,message.another_text)
    




# listener with server 
bot.infinity_polling()
