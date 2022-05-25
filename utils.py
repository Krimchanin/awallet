import locale


class Utils:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

    @staticmethod
    def locale_balance(balance):
        return locale.currency(balance, grouping=True)
