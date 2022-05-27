# -*- coding: utf-8 -*-
from database import BaseDatabase
from telebot import types
from utils import Utils
from html_generator import HtmlGenerator
"""
This file is needed in order to process messages and callback (buttons)
The code was written by Alexey Vinogradov for the project
"""


class Response:
    def __init__(self, answers, param_debug, telegram_bot):
        self.answers = answers
        #   logging variables to cmd
        self.mode_debug = param_debug
        #   this import telegram bot for send messages
        self.bot = telegram_bot
        #   this import database
        self.db = BaseDatabase()
        #   this import utils
        self.utils = Utils()
        #   this import htmlgen for detalization
        self.html_gen = HtmlGenerator()

    #   Generic Function for Checking Messages and callback
    #   type_message == 0 == message
    #   type_message other == callback (information from button)

    def check(self, type_message, telegram_user_id_message,
              text_message=None, callback_data_message=None, message=None):

        keyboard = types.InlineKeyboardMarkup()

        if self.db.check_registration_user(telegram_user_id=telegram_user_id_message) is False:
            if callback_data_message == "registration":
                pass
            else:

                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Зарегистрироваться',
                        callback_data='registration'))

                self.bot.send_message(
                    chat_id=telegram_user_id_message,
                    text=self.answers["c_start_unregistered"],
                    reply_markup=keyboard)
                return 0

        #   message
        if type_message == 0:
            keyboard = types.InlineKeyboardMarkup()

            if text_message == "/start":
                if self.db.check_registration_user(
                        telegram_user_id=telegram_user_id_message):

                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='Зачисление',
                            callback_data='enrollment'))
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='Трата',
                            callback_data='spending'))
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='Статистика',
                            callback_data='stats'))
                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='Настройки',
                            callback_data='settings'))

                    self.bot.send_message(
                        chat_id=telegram_user_id_message,
                        text=self.answers["c_start_registered"],
                        reply_markup=keyboard)
                else:

                    keyboard.add(
                        types.InlineKeyboardButton(
                            text='Зарегистрироваться',
                            callback_data='registration'))

                    self.bot.send_message(
                        chat_id=telegram_user_id_message,
                        text=self.answers["c_start_unregistered"],
                        reply_markup=keyboard)
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Вернуться в меню',
                        callback_data='menu'))
                self.bot.send_message(
                    chat_id=telegram_user_id_message,
                    text=self.answers["c_unk"],
                    reply_markup=keyboard)

        #   callback
        elif type_message == 1:
            keyboard = types.InlineKeyboardMarkup()
            if callback_data_message == "registration":
                self.db.registration_user(telegram_id=telegram_user_id_message)
                self.bot.send_message(
                    chat_id=telegram_user_id_message,
                    text=self.answers["c_registration_complete"],
                    reply_markup=keyboard)

            elif callback_data_message == "menu":
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Зачисление',
                        callback_data='enrollment'))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Трата',
                        callback_data='spending'))
                keyboard.add(types.InlineKeyboardButton(text='Статистика',
                                                        callback_data='stats'))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Настройки',
                        callback_data='settings'))

                self.bot.send_message(chat_id=telegram_user_id_message,
                                      text=self.answers["c_start_registered"],
                                      reply_markup=keyboard)

            elif callback_data_message == "enrollment":
                self.bot.send_message(chat_id=telegram_user_id_message,
                                      text=self.answers["c_enrollment"],
                                      reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.enrollment)

            elif callback_data_message == "spending":
                self.bot.send_message(chat_id=telegram_user_id_message,
                                      text=self.answers["c_spending"],
                                      reply_markup=keyboard)
                self.bot.register_next_step_handler(message, self.spending)

            elif callback_data_message == "stats":
                data = self.db.get_stats_user(
                    telegram_id=telegram_user_id_message)
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Детализация',
                        callback_data='detalization'))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Вернуться в меню',
                        callback_data='menu'))
                self.bot.send_message(
                    chat_id=telegram_user_id_message, text=self.answers["c_stats"].format(
                        self.utils.locale_balance(
                            data[1]), self.utils.locale_balance(
                            data[0]['dream_price']), data[0]["dream_name"], self.utils.locale_balance(
                            data[2])), reply_markup=keyboard)

            elif callback_data_message == "detalization":
                self.bot.send_document(
                    chat_id=telegram_user_id_message,
                    document=open(
                        self.html_gen.generation(telegram_user_id_message),
                        mode="r",
                        encoding='utf-8'))

            elif callback_data_message == "settings":
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Изменить цель',
                        callback_data='change_dream'))
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Удалить данные обо мне',
                        callback_data='delete_me'))
                self.bot.send_message(
                    chat_id=telegram_user_id_message,
                    text=self.answers["c_settings"],
                    reply_markup=keyboard)

            elif callback_data_message == "delete_me":
                self.db.delete_user(telegram_id=message.chat.id)
                self.bot.send_message(
                    chat_id=telegram_user_id_message,
                    text=self.answers["c_deleted"],
                    reply_markup=keyboard)

            elif callback_data_message == "change_dream":
                self.bot.send_message(
                    chat_id=telegram_user_id_message,
                    text=self.answers["c_change_dream"]
                )
                self.bot.register_next_step_handler(message, self.change_dream)

            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Вернуться в меню',
                        callback_data='menu'))
                self.bot.send_message(
                    chat_id=telegram_user_id_message,
                    text=self.answers["c_unk"],
                    reply_markup=keyboard)

    def change_dream(self, message):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Вернуться в меню',
                                                callback_data='menu'))
        if message.text == "0":

            self.bot.send_message(chat_id=message.chat.id,
                                  text=self.answers["c_cancel"],
                                  reply_markup=keyboard)
            if message.text.count(",") != 1:
                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_error_user"],
                                      reply_markup=keyboard)
                return 0
        else:
            try:
                self.db.dream_edit(telegram_id=message.chat.id,
                                   dream_name=message.text.split(",")[0],
                                   dream_price=message.text.split(",")[1]
                                   )

                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_complete"],
                                      reply_markup=keyboard)
            except Exception as e:
                print(e)
                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_error"],
                                      reply_markup=keyboard)

    def enrollment(self, message):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Вернуться в меню',
                                                callback_data='menu'))
        if message.text == "0":

            self.bot.send_message(chat_id=message.chat.id,
                                  text=self.answers["c_cancel"],
                                  reply_markup=keyboard)
            if message.text.count(",") != 1:
                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_error_user"],
                                      reply_markup=keyboard)
                return 0
        else:
            try:
                self.db.transaction_add(telegram_id=message.chat.id,
                                        summ=message.text.split(",")[0],
                                        comment=message.text.split(",")[1],
                                        type=1)

                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_complete"],
                                      reply_markup=keyboard)
            except Exception as e:
                print(e)
                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_error"],
                                      reply_markup=keyboard)

    def spending(self, message):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Вернуться в меню',
                                                callback_data='menu'))
        if message.text == "0":
            self.bot.send_message(chat_id=message.chat.id,
                                  text=self.answers["c_cancel"],
                                  reply_markup=keyboard)
            if message.text.count(",") != 1:
                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_error_user"],
                                      reply_markup=keyboard)
                return 0
        else:
            try:
                self.db.transaction_add(telegram_id=message.chat.id,
                                        summ=message.text.split(",")[0],
                                        comment=message.text.split(",")[1],
                                        type=0)

                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_complete"],
                                      reply_markup=keyboard)
            except Exception as e:
                print(e)
                self.bot.send_message(chat_id=message.chat.id,
                                      text=self.answers["c_error"],
                                      reply_markup=keyboard)
