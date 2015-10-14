# -*- coding: utf-8 -*-
#!join romscout FlareRDB RandomRambo Thenoosh22 HSdogdog IGN LotharHS Draskyl

import codecs

class Printer(object):

    LEVELS = {"DEBUG", "NOMINAL", "LOGGING", "NONE"}
    EXTRA = {"HIGH", "MED", "LOW", "ALL"}
    ON = True

    def __init__(self, prefix):
        self.pref = prefix
        self.prefix = "[ " + str(prefix) + " ]"

    def __call__(self, *args, **kwargs):
        if Printer.level == "DEBUG":
            self.write(args, kwargs)

    def error(self, *args, **kwargs):
        cState = Printer.ON
        Printer.ON = True
        self.write(args, kwargs)
        Printer.ON = cState

    def addSpecial(self, special):
        self.prefix = "[ " + self.pref + "." + special + " ]"

    def user(self, *args, **kwargs):
        if Printer.level == "NOMINAL":
            self.write(args, kwargs)

    def format(self, args, kwargs):
        return str(self.prefix+" "+" ".join(map(str, args)))


    def write(self, args, kwargs):
        if Printer.ON or True:
            s = self.format(args, kwargs)
            if isinstance(s, bytes):
                print(codecs.decode(s, 'UTF-8', "replace"))
            elif isinstance(s, str):
                print(s)
            else:
                print(codecs.encode(s, "UTF-8", "replace"))


    @property
    @classmethod
    def level(cls):
        try:
            return cls._level

        except AttributeError:
            cls._level = "NOMINAL"
            return cls._level

    @level.setter
    @classmethod
    def level(cls, value):
        #if value in regesterd types
        cls._level = value
        #else Raise Type Error
