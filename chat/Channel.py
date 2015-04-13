#! /usr/bin/env python2.7

import socket
# import thread
import time
from sys import path 
import os

from User import User
import twitchtools.login
import twitchtools.utils

class Channel(object):
    """
    Channel(IRCobject, name)
    """
    Operators = []


    def __init__(self, IRCOBJ, name):
        super(Channel, self).__init__()
        self.users = {}
        self.ircParent = IRCOBJ
        self.name = name
        self.owner = name.strip("#").strip()
        self.AttachedCommands = []
        self.Operators = []
        self.OperatorInstances = {}
        self.term = twitchtools.utils.Printer("Channel.{}".format(self.name))

    
    def RecvMessage(self, message):
        try:
            self.users[message.user].addMessage(message)
            self.term("Inserting Message Into User:", message.user )

        except KeyError:
            self.createUser(message.user)
            self.users[message.user].addMessage(message)
            self.term("Creating User:", message.user)

        #self.term(self.Operators+Channel.Operators)
        for op in self.Operators + Channel.Operators:
            if op.poll(self, message):
                try:
                    self.OperatorInstances[op].execute(self, message)
                except KeyError, e:
                    self.OperatorInstances[op] = op()
                    self.OperatorInstances[op].execute(self, message)
                    


    def AddOperator(self, ops):
        if isinstance(ops, twitchtools.utils.Operator):
            self.Operators.append(ops)

        else:
            raise TypeError("'{}' is not of type '{}'".format(ops, twitchtools.utils.Operator))


    def createUser(self, username):
        self.users[username] = User(self, username)

    def pm(self, message):

        self.ircParent.pm(self, message)
# import time
# from IRC import IRC

# class TwitchChannel(IRC):

#     def __init__(self, host, port, speaker_queue, channels):
#         super().__init__(host, port)
#         self.running = False
#         self.channels = channels
#         self.speaker_queue = speaker_queue

#     def main_connect(self):
#         self.sock_init()
#         self.sock_connect()
#         self.send_pass("bleh")
#         self.send_nick("justinfan7219")
#         self.sock_recv(1024)
#         self.send_raw("CAP REQ :twitch.tv/tags")
#         self.sock_recv(1024)
#         for i in self.channels:
#             self.send_join(i)
#             time.sleep(1)

#     def main_loop(self):
#         self.main_connect()
#         msg = ""
#         self.running = True
#         while self.running:
#             msg += self.sock_recv(2048)
#             if msg:
#                 messages = msg.split("\r\n")
#                 while len(messages) > 1:
#                     current_msg = messages.pop(0)
#                     if not current_msg.startswith('@'):
#                         continue
#                     c_msg = current_msg.split(' ', 4)
#                     if c_msg[2] == "PRIVMSG":
#                         user = c_msg[1].split('!')[0][1:]
#                         target_channel = c_msg[3]
#                         self.speaker_queue.put([target_channel, user, "speaking", 1])
#                 msg = messages[0]