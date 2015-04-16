#! /usr/bin/env python2.7

import socket
import threading
import time
from sys import path 
import os

from Channel import Channel
from Message import Message
import twitchtools.login
import twitchtools.utils




class IRC(object):
    """
    IRC((Address, port), [(user, pass), (Profile object)])
    """

    def __init__(self, AP = None, USER = None):
        self.channels = {}
        self.saveQueue = {}
        self.Operators = []
        self.user = None
        self.IRCNAME = None
        self.link = socket.socket();
        self.term = twitchtools.utils.Printer("IRC.{}".format(USER.name))

        if IRC:
            self.server(AP)

        if USER:
            self.credentials(USER)

        if IRC and USER:
            self.connect()
            self.login()

    def __enter__(self):

        return self

    def __exit__(self, typeof, value, traceback):
        if typeof or value or traceback:
            self.term(typeof, value, traceback)
        else:
            self.term("Closed connection successfully...")
        self.disconnect()

    def StopMessage(self, COMMAND, USERS):
        pass

    def server(self, AP):

        self.IRCNAME = AP

    def credentials(self, USER):
        if isinstance(USER, (tuple, list)):
            self.user = twitchtools.login.Profile(USER[0], oauth=USER[1])

        elif isinstance(USER, twitchtools.login.Profile):
            self.user = USER

        else:
            raise TypeError("User is not of correct type")
   
    def login(self):
        self.password()
        self.nick()

    def connect(self):
        self.term("Attempting to connect to :",' @ '.join(map(str,self.IRCNAME)))
        self.link.connect(self.IRCNAME)
        self.term("Connection successfully created...")
        
    def disconnect(self):
        self.raw("QUIT")
        self.link.close()

    def raw(self, message):
        self.term("<-",message)
        self.link.sendall("{}\r\n".format(message))

    def capibilities(self, req):

        self.raw("CAP REQ :twitch.tv/{}".format(req))

    def nick(self):

        self.raw("NICK {}".format(self.user.name))
        
    def password(self):

        self.raw("PASS {}".format(self.user.password))

    def join(self, channel, limiter=0.5, size=10):
        channels = channel.split(",")

        if len(channels) < size:
            limiter = 0

        for channel in channels:
            #If channel contains a  '#' already get rid if it
            channel = channel.strip('#').strip(' ').lower()

            self.raw("JOIN #{}".format(channel.lower()))

            time.sleep(limiter)
            #pretty print join time ETA? (ref simple_incoming_twitch_irc.py)

            self.channels[channel] = Channel(self, channel)

            #Create channel object and set up redirection to that object storage
            #Save channel object to local hash
            #Return channel object to user

        if len(channels) == 1:
            return self.getChannel(channels[0])

    def part(self, channel):
        channel = channel.lower()
        try:
            self.saveQueue[channel] = self.channels.pop(channel, None)
            self.raw("PART {}".format(channel))
        except KeyError:
            pass

    def getChannel(self, channel):
        channel = channel.lower()
        return self.channels.get(channel, None)

    def pm(self, CHANNELOBJ, message):

        self.raw("PRIVMSG #{} :{}".format(CHANNELOBJ.name, message))

    def read(self, output = True, amount = 512, timeout = 0.5):
        stimeout = self.link.gettimeout()
        self.link.settimeout((timeout if timeout < 0 else float(timeout)))

        try:
            incoming = [i for i in self.readfile()]
        except socket.timeout as e:
            self.term.error(e)
            return 
        finally:
            pass

        for message in incoming:
            if output:
                self.term(message)

            if output.lower() == "file":
                with open("outfile",'a') as fout:
                    fout.write(message)

            self.distrubute(message)


        self.link.settimeout(stimeout)

    def readfile(self, buffsize = 512, timeout=-1, raw=False, lines=False):
        for i in self.link.makefile():
            if i.startswith("PING"):
                self.raw(i.replace("PING", "PONG").strip())
                continue

            yield self.distrubute(Message(i))

    def distrubute(self, message):
        try: 
            if message.command in ["PRIVMSG", "CLEARCHAT"]: self.channels[message.channel].RecvMessage(message)
            
        except KeyError:
            pass


        return message
        """
        Read channel
        Send to channel
        else if not channel 
        send to global (all?)

        """

    def register(self, Ops):
        if issubclass(Ops, twitchtools.utils.Operator):
            self.Operators.append(Ops)

        else:
            raise TypeError("'{}' is not of type '{}'".format(Ops, twitchtools.utils.Operator))


    def auto(self, *args, **kwargs):
        self.read(timeout=500)


if __name__ == '__main__':
    m = IRC(("irc.twitch.tv", 6667), twitchtools.login.Profile("bomb_mask", "C:/Users/bombmask/Source/garden/twitch"))
    m.read(True, timeout = 10)
    m.capibilities("twitch.tv/tags")
    m.read()
    m.pm("snarfybobo",".mods")
    m.read(True)
    
    m.disconnect()
    k = raw_input("press enter to exit...")
