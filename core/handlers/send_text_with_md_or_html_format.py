import telebot
def register(bot):
    @bot.message_handler(commands = ["Markdown"])
    def handle_message(message):
        bot.send_message(message.chat.id, "This is _italic_ text", parse_mode="Markdown")
        bot.send_message(message.chat.id, "[Google](http://www.google.com)", parse_mode="Markdown")
        bot.send_message(message.chat.id, "`inline code`", parse_mode="Markdown")
        bot.send_message(message.chat.id, "```\nmultiline code\n```", parse_mode="Markdown")


    @bot.message_handler(commands = ["HTML"])
    def handle_message(message):
        bot.send_message(message.chat.id, "<b>This is bold text</b>", parse_mode="HTML")
        bot.send_message(message.chat.id, "<i>This is italic text</i>", parse_mode="HTML")
        bot.send_message(message.chat.id, '<a href="http://www.google.com">Google</a>', parse_mode="HTML")
        bot.send_message(message.chat.id, "<code>inline code</code>", parse_mode="HTML")
        bot.send_message(message.chat.id, "<pre>multiline code</pre>", parse_mode="HTML")