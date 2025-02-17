import telebot
from telebot.types import InlineQueryResultArticle , InputTextMessageContent


def register(bot):
    @bot.inline_handler(func = lambda query:True)
    def query_handler(query):
        # logger.info(query)
        results = []
        results.append(
            InlineQueryResultArticle(
                id ='1',
                title= "Ask me",
                input_message_content= InputTextMessageContent(message_text="سلام چطوری میتونم کمکت کنم؟")
            )
        )
        results.append(
            InlineQueryResultArticle(
                id ='2',
                title= "Join the bot",
                input_message_content= InputTextMessageContent(message_text="https://t.me/My_First_projecttbot"),
                url="https://t.me/My_First_projecttbot"
            )
        )
        bot.answer_inline_query(query.id , results,cache_time = 0) # because it waste so time to check cache we assign to 0
        