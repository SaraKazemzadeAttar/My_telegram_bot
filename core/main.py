import telebot
from config import API_TOKEN
import os
import pprint
import json
from telebot import apihelper
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton
from handlers import send_files_management , inline_query_handler , send_text_with_md_or_html_format
import importlib
import importlib.util
import sys

logger = telebot.logger
apihelper.ENABLE_MIDDLEWARE = True

telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN)

# Add the core directory to Python path
sys.path.append(os.path.dirname(__file__))

handlers_dir = os.path.join(os.path.dirname(__file__), 'handlers')

for file in os.listdir(handlers_dir):
    if file.endswith(".py") and file != "__init__.py":
        module_name = f"handlers.{file[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(handlers_dir, file))
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        if hasattr(module, 'register'):
            module.register(bot)
# sequence with inline keyboard

def send_welcome(message, from_start=True):
    logger.info("triggered Welcome")
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, 
        input_field_placeholder="انتخاب کن", 
        one_time_keyboard=True
    )
    markup.add(KeyboardButton('/help'), KeyboardButton('/setname'))  # افقی
    markup.add(KeyboardButton('Send Audio or Docs'))
    markup.add(KeyboardButton('/Connect_Me'))
    
    if from_start:
        bot.send_message(
            message.chat.id, 
            "سلام ! ❤️چه کمکی میتونم بهت بکنم؟", 
            reply_markup=markup
        )
    else:
        bot.send_message(
            message.chat.id, 
            "بازگشت به منوی اصلی 📋", 
            reply_markup=markup
        )

@bot.message_handler(commands=['start'])
def start_command(message):
    send_welcome(message, from_start=True)
    
@bot.message_handler(func = lambda message: message.text == "Send Audio or Docs")
def message_for_audio_docs(message):
    bot.send_message(message.chat.id , "اینجا میتونی فایل یا صوت آپلود کنی !")
    
@bot.message_handler(commands=['Connect_Me'])
def connect_me(message):
    logger.info("Connection request")
    markup = InlineKeyboardMarkup()
    button_linkedin = InlineKeyboardButton("linkedin",url = "https://www.linkedin.com/in/sara-kazemzade-attar")
    button_github = InlineKeyboardButton("github",url = "https://github.com/SaraKazemzadeAttar")
    button_next_step = InlineKeyboardButton("More Options", callback_data="step1")
    markup.add(button_linkedin , button_github)
    markup.add(button_next_step)
    bot.reply_to(message, "میتونی صفحه من رو توی گیت هاب و لینکدین ببینی", reply_markup=markup)
    
@bot.callback_query_handler(func= lambda call:True)
def reply_call(call):
    if call.data == "step1" :
        markup = InlineKeyboardMarkup()
        button_webpage = InlineKeyboardButton("Quera" , url = "https://quera.org/profile/Sara_kazemzade612")
        button_cancell = InlineKeyboardButton("بازگشت به منوی اصلی" , callback_data ="main_menu")
        markup.add(button_webpage)
        markup.add(button_cancell)
        bot.edit_message_text(chat_id= call.message.chat.id , message_id= call.message.id , text= " آدرس صفحه من در quera " , reply_markup = markup) 

    if call.data == "main_menu":
        send_welcome(call.message, from_start=False)
        bot.delete_message(chat_id= call.message.chat.id , message_id= call.message.id , timeout = 20)

        
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """🌟 **راهنمای ربات** 🌟
    
سلام دوست عزیز! 👋 
این اولین رباتیه که من برای آموزش دیدن راه اندازی کردم  🛠️  

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
@bot.message_handler(func=lambda msg: msg.text in ["سلام", "👋","❤️"]) 
def handle_text_doc(message):   
	bot.reply_to(message, "hello my friend")


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
