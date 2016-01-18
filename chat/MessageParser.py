#!/usr/bin/env python3.5
"""
Copyright: Firestack 2015
-------------------------
Simple Message Parser Class
"""
# import socket
# from sys import path
# import os
# import thread

import datetime

from . import EventHandler as EH

class Message(object):

    def __init__(self, message, time=None):
        # Parse message into serializeable data
        # Should be left open for extention
        # NOTE: Right now it feels like the message class
        #$ IS going to limit most of the code
        #$ Let us not build the entire framework around
        #$ This class
        # THOUGHTS: Should I build this class as a parser utility?

        """ Message spec (@<tags> )?:<headers> (:<message>)?<CRLF> """
        if time:
            self.SetTime(time)
        else:
            self.time = datetime.datetime.now()

        self.raw = message

        self.tags = dict()
        self.headers = ""
        self.cachedParsedMessage = ""
        self.params = ""
        self.action = ""
        self.prefix = ""

        self.weird = False

        self.ParseMessage()


    def ParseMessage(self):
        """
        Example Message :
        @color=#78CFE0;display-name=Bomb_Mask;emotes=;subscriber=0;turbo=0;user-id=31985816;user-type= :bomb_mask!bomb_mask@bomb_mask.tmi.twitch.tv PRIVMSG #bomb_mask :2
        @slow=0 :tmi.twitch.tv ROOMSTATE #bomb_mask
        @broadcaster-lang=en;r9k=1;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #bomb_mask
        @msg-id=slow_off :tmi.twitch.tv NOTICE #bomb_mask :This room is no longer in slow mode.
        PING :tmi.twitch.tv
        :tmi.twitch.tv CLEARCHAT #bomb_mask :testuser
        :tmi.twitch.tv CLEARCHAT #bomb_mask
        :tmi.twitch.tv HOSTTARGET #bomb_mask :johnmackay13 0
        @msg-id=host_on :tmi.twitch.tv NOTICE #bomb_mask :Now hosting johnmackay13.
        @color=#78CFE0;display-name=Bomb_Mask;emote-sets=0;subscriber=0;turbo=0;user-type= :tmi.twitch.tv USERSTATE #bomb_mask
        :bomb_mask.tmi.twitch.tv 353 bomb_mask = #bomb_mask :bomb_mask
        """

        self.raw = self.raw.strip("\r\n")

        # Parse Tags Section
        ## Assume we have tags if starts with @ sign
        if self.raw[0] == "@":
            tempTags, payload = self.raw.split(" :", 1)
            tempTags = tempTags[1:]

            for item in tempTags.split(";"):
                key, value = item.split("=")
                self.tags[key] = value

        elif self.raw[0] == ":":
            # Simple Quick fix, Reimplement functions, extendablity.
            payload = self.raw

        else: #Odd condition, things like PING
            payload = self.raw
            self.weird = True

        if not self.weird:
            # Parse message Main Content
            loadingBay = payload.split(" :",1)

            if len(loadingBay) == 2:
                self.headers, self.cachedParsedMessage = loadingBay

            else:
                self.headers = loadingBay[0]
                self.cachedParsedMessage = ''

            loadingBay = self.headers.split(" ",2)
            self.prefix = loadingBay[0]
            self.action = loadingBay[1]
            self.params = loadingBay[2].split(' ')
            # print(loadingBay)


        else:
            # IT WAS WEIRD?!? (PINGS)
            self.action, self.cachedParsedMessage = payload.split(' ', 1)
            self.params = [self.cachedParsedMessage]
            self.prefix = self.GetRaw()


    def HasTags(self):
        return bool(self.tags)

    def GetTags(self):
        if self.HasTags():
            return self.tags
        else:
            return dict()

    def GetHeaders(self):
        return self.headers

    def GetMessage(self):
        return self.cachedParsedMessage

    def GetAction(self):
        return self.action

    def GetEvent(self):
        # Temporary
        try:
            if self.GetAction().isnumeric():
                return EH.TEvent.NUMBERS

            return EH.TEvent[self.GetAction().upper()]

        except KeyError:
            return EH.TEvent.UNKNOWN

    def GetRaw(self):
        return self.raw

    def GetTime(self):
        return self.time

    def SetTime(self, timeObject):
        # Time was a major issue in the last version of this
        self.time = timeObject
