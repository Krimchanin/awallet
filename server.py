# -*- coding: utf-8 -*-

"""
This global file for start
here you can enable or disable the key features of the bot
The code was written by Alexey Vinogradov for the project
"""

import telebot
from responses import Response
from Config import Config
CONFIG = Config()


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.MODULE_RESPONSE = Response(
            CONFIG.answers,
            CONFIG.config["Telegram"]["debug_mode"],
            self.bot)

    #   Function for connect module read messages
    def check_messages(self):
        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            self.MODULE_RESPONSE.check(
                type_message=0,
                telegram_user_id_message=message.chat.id,
                text_message=message.text,
                callback_data_message=None,
                message=message)

    #   Function for connect module read callback(buttons)
    def check_callbacks(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            self.MODULE_RESPONSE.check(
                type_message=1,
                telegram_user_id_message=call.message.chat.id,
                text_message=None,
                callback_data_message=call.data,
                message=call.message)

    def pool(self):
        self.check_messages()
        self.check_callbacks()
        self.bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    """
    if the telegram servers do not respond,
    the bot will simply restart and continue working
    """
    while True:
        try:
            bot = Bot(CONFIG.config["Telegram"]["token"])
            bot.pool()
        except Exception as E:
            print(E)
