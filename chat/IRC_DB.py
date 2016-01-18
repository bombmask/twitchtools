#!/usr/bin/env python3.5
#coding: utf8
"""
Copyright: Firestack 2015
-------------------------
IRC Class to implement sqldatabase storage.
"""

import socket
import time
import sqlite3 as sql


from . import IRC_Twitch

class IRC_DB(IRC_Twitch.IRC_Twitch):
    """docstring for IRC_Event"""

    def __init__(self):
        # Ensure we build the objects super class
        super().__init__()

        self.dbName = "bot.db"



        self.dbConn = sql.connect(self.dbName)

        self.dftCursor = self.dbConn.cursor()
        self.CreateTable("chatdata", "User TEXT, Raw TEXT, Time DATE, Event INT, Channel TEXT, Message TEXT")
        self.CreateTable("config", "Channel TEXT, Data TEXT")
        # self.dftCursor.execute("""
        # create table if not exists chatdata (
        #     USER TEXT,
        #     MESSAGE TEXT
        # )
        # """)

        print("Current SQLite Version: ", sql.sqlite_version)

    def Close(self):
        super().Close()
        self.dbConn.close()

    def ResetData(self):
        self.dftCursor.execute("DELETE FROM chatdata")

    def CreateTable(self, tableName, typeString):
        executeString = "create table if not exists {} ({})".format(tableName, typeString)
        self.dftCursor.execute(executeString)

    def Intercept(self, *message):
        # Call parent hierarchy to ensure twitch pings
        # Defines self.tMessage
        super().Intercept(message[0])

        try:
            self.dftCursor.execute(
                "INSERT INTO chatdata VALUES (?,?,?,?,?,?)",
                (
                    self.tMessage.prefix.split('!')[0],
                    str(message[0]),
                    self.tMessage.GetTime(),
                    self.tMessage.GetEvent().value,
                    self.tMessage.params[0],
                    self.tMessage.GetMessage()
                )
            )
            self.dbConn.commit()

        except sql.Error as E:
            print("An Error occured:",E.args[0])

        #print("{}".format(message[0]))
        # User Latch Point
