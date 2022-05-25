# -*- coding: utf-8 -*-

"""
this file is needed to work with the database
The code was written by Alexey Vinogradov for the project
"""


import sqlite3


class Database:
    def __init__(self):
        self.database_file = "database.db"

    def run_command(self, command, commit):
        try:
            #   create connection
            sqlite_connection = sqlite3.connect(self.database_file)
            #   create cursor
            cursor = sqlite_connection.cursor()
            #   execute command
            cursor.execute(command)

            #   get response database
            response = cursor.fetchall()

            if commit == 1:
                #   commit need for INSERT, UPDATE, DELETE
                sqlite_connection.commit()

            #   close connection
            cursor.close()
            sqlite_connection.close()
            return response

        except Exception as E:
            print(E)


class BaseDatabase(Database):
    def check_registration_user(self, telegram_user_id):
        if self.run_command(
                command=f"SELECT * FROM users WHERE telegram_id = {telegram_user_id}",
                commit=0):
            return True
        else:
            return False

    def get_info_user(self, telegram_user_id):
        if self.check_registration_user(telegram_user_id):
            response = self.run_command(
                command=f"SELECT * FROM users WHERE telegram_id = {telegram_user_id}",
                commit=0)[0]
            return {
                "id": response[0],
                "telegram_id": response[1],
                "dream_name": response[2],
                "dream_price": response[3],
                "permissions": response[4]
            }
        else:
            return False

    def registration_user(self, telegram_id):
        self.run_command(
            command=f"INSERT INTO users"
                    f" (telegram_id, dream_name, dream_price, permissions) "
                    f"VALUES ({telegram_id}, \"Ноутбук\", 1000, 1)",
            commit=1)

    def get_balance_user(self, telegram_id):
        temp = self.run_command(
            command=f"SELECT * FROM transactions WHERE telegram_id={telegram_id}",
            commit=0)
        total = 0
        for t in temp:
            if t[3] == 0:
                total -= t[2]
            else:
                total += t[2]
        return total

    def get_left_balance_dream(self, telegram_id):
        price = self.get_info_user(telegram_user_id=telegram_id)['dream_price']
        left = self.get_balance_user(telegram_id=telegram_id)
        if left >= price:
            return 0
        else:
            return price - left

    def get_stats_user(self, telegram_id):
        stats = self.get_info_user(telegram_user_id=telegram_id)
        balance = self.get_balance_user(telegram_id=telegram_id)
        return stats, balance, self.get_left_balance_dream(
            telegram_id=telegram_id)

    def transaction_add(self, telegram_id, summ, type, comment):
        self.run_command(
            command=f"INSERT INTO transactions"
                    f" (telegram_id, sum, type, comment) "
                    f"VALUES ({telegram_id}, {summ}, {type}, \"{comment}\")",
            commit=1)

    def transactions_get(self, telegram_id):
        return self.run_command(
            command=f"SELECT * FROM transactions WHERE telegram_id = {telegram_id}",
            commit=0)

    def transaction_delete(self, id_transaction, telegram_id):
        self.run_command(
            command=f"SELECT * FROM transactions"
                    f"WHERE id = {id_transaction} AND "
                    f"telegram_id = {telegram_id}",
            commit=1
        )

    def dream_edit(self, telegram_id, dream_name, dream_price):
        self.run_command(
            command=f"UPDATE users "
                    f"SET dream_name=\"{dream_name}\", dream_price={dream_price} "
                    f"WHERE telegram_id = {telegram_id}",
            commit=1
        )

    def delete_user(self, telegram_id):
        self.run_command(
            command=f"DELETE FROM users "
                    f"WHERE telegram_id = {telegram_id}",
            commit=1
        )
        self.run_command(
            command=f"DELETE FROM transactions "
                    f"WHERE telegram_id = {telegram_id}",
            commit=1
        )
