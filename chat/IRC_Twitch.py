#!/usr/bin/env python3.5
"""
Copyright: Firestack 2015
-------------------------
IRC Class to Implement Basic Twitch Functions
Inherits from IRC Event to reduce cpu strain
"""

import socket

from . import ChannelStorage as CS
from . import MessageParser as MP
from . import IRC_Event
from . import EventHandler as EH

class IRC_Twitch(IRC_Event.IRC_Event):
    """docstring for IRC_Event"""

    def __init__(self, parent):
        # Ensure we build the objects super class
        super().__init__()
        self.parent = parent
        self.channels = []

        self.username = ""
        self.password = ""
        self.serverPair = []

        self.channelStorage = dict()

    def login(self):
        self.Raw("PASS {}".format(self.password))
        self.Raw("NICK {}".format(self.username))


    def Join(self, channel):
        channel = channel.lower().strip("#")
        # Join channel
        self.Raw("JOIN #{}".format(channel))
        # Store joined channels
        self.channels.append(channel)

    def Leave(self, channel):
        channel = channel.lower()
        # Leave channel
        self.Raw("PART #{}".format(channel))

        # Remove channel from current channel list
        self.channels.remove(channel)

    def InitalizeEvents(self):
        for EventGroupName, EventGroup in self.callback_objects.items():
            for Event in EventGroup:
                Event.Once(self)

    def Intercept(self, message):
        # Play ping pong with server
        # First class action
        if message.startswith("PING"):
            self.Raw(message.replace("PING", "PONG").strip())

        self.tMessage = MP.Message(message)
        #print(self.tMessage.GetEvent(), self.tMessage.GetAction())
        # Safety First
        if self.tMessage.GetEvent() == EH.TEvent.UNKNOWN:
            print(self.tMessage.GetEvent(), self.tMessage.GetAction())

        if self.tMessage.GetEvent() == EH.TEvent.NOTICE:
            print(self.tMessage.GetRaw())

        for Handler in self.callback_objects.get(self.tMessage.GetEvent(), []):
            Handler.Execute(self, message, self.tMessage)

        # If registered for all types
        for Handler in self.callback_objects.get(EH.TEvent.ALL, []):
            Handler.Execute(self, message, self.tMessage)

        if self.tMessage.GetEvent() == EH.TEvent.PRIVMSG:
            self.Save(self.tMessage.params[0][1:])


    def Start(self):
        self.InitalizeEvents()
        self.Load()
        self.ConnectTo(*self.serverPair)
        self.login()

    def Load(self):
        
        pass

    def Save(self, channel):
        channel = self.channelStorage.get(channel,False)
        if (channel):
            channel.Save(self.parent)



    def ChannelData(self, channel = None):
        if channel == None:
            channel = self.tMessage.params[0][1:]

        try:
            return self.channelStorage[channel]

        except KeyError:
            self.channelStorage[channel] = CS.ChannelData(channel)
            self.channelStorage[channel].Load(self.parent)
            return self.channelStorage[channel]
