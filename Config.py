from configparser import *
import json


class Config:
    path = {
        "config": "./config/config.ini",
        "answers": "./locales/ru.json"
    }

    def __init__(self):

        # config
        parser = ConfigParser()
        parser.read(self.path["config"])
        self.config = parser

        # get answers

        f = open(self.path["answers"], mode="r", encoding="utf8")
        self.answers = json.loads(f.read())
