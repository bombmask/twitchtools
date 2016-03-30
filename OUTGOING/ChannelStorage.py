#!/usr/bin/env python3.5
"""
Copyright: Firestack 2015
-------------------------
Storage object class for EventHandler classes
"""

import json
import sqlite3 as sql

def SerializeUser(user):
    return user.__dict__

class DataObject(object):

    def __init__(self):
        super().__init__()

    def GetData(self):
        return self.__dict__

    def Serialize(self):
        return json.dumps(self.__dict__)

    def Deserialize(self, inputString):
        self.__dict__ = json.loads(inputString)

class ChannelData(DataObject):

    def __init__(self, channelName):
        self.channelName = channelName
        self.Users = {}


    def Load(self, botuni):
        cur = botuni.GetCursor()
        cur.execute("SELECT json FROM config WHERE channel=?",(self.channelName,))
        dbData = cur.fetchone()

        if (dbData):

            dbData = json.loads(dbData[0])

            self.__dict__ = dbData
            self.Users = {}
            for username,userdata in dbData["Users"].items():
                self.Users[username] = UserData(username)
                self.Users[username].__dict__ = userdata

        cur.connection.commit()
        cur.close()

    def Save(self, botuni):
        cur = botuni.GetCursor()
        cur.execute("SELECT COUNT(*) FROM config WHERE channel=?",(self.channelName,))

        if(cur.fetchone()[0] == 0):
            cur.execute("INSERT INTO config VALUES (?,?)", (self.channelName, json.dumps(self.__dict__, default=SerializeUser)))
        else:
            cur.execute("UPDATE config SET json=? WHERE channel=?", (json.dumps(self.__dict__, default=SerializeUser), self.channelName))

        cur.connection.commit()
        cur.close()

    def GetChannel(self):
        return self.channelName

    def GetUser(self, username):
        username = username.lower()
        try:
            return self.Users[username]

        except KeyError:
            self.InitalizeNewUser(username)
            return self.Users[username]

    def InitalizeNewUser(self, username):
        self.Users[username.lower()] = UserData(username.lower())

class UserData(DataObject):

    def __init__(self, UserName):
        self.UserName = UserName

    def GetUser(self):
        return self.UserName
