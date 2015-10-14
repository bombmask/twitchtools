#! /usr/bin/env python2.7

import socket
import codecs
# import thread
import time
from sys import path
import os

from .User import User
import twitchtools.login
import twitchtools.utils

import traceback
import sys

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

        #self.term(self.Operators+Channel.Operators,self.OperatorInstances)

        for op in self.Operators + self.ircParent.Operators:
            if op not in self.OperatorInstances and op.init_on_attach:
                self.term("Attaching Operator", op)
                self.OperatorInstances[op] = op()

            if op.poll(self, message):
                try:
                    #self.term(op)
                    self.OperatorInstances[op].execute(self, message)
                except KeyError as e:

                    print ('-'*60)
                    traceback.print_exc(file=sys.stdout)
                    print ('-'*60)

                    self.OperatorInstances[op] = op()
                    self.OperatorInstances[op].execute(self, message)



    def AddOperator(self, ops):

        if isinstance(ops, twitchtools.utils.Operator):
            self.Operators.append(ops)

            if hasattr(ops, init_on_attach):
                if ops.init_on_attach == True:
                    self.OperatorInstances[ops] = op()

        else:
            raise TypeError("'{}' is not of type '{}'".format(ops, twitchtools.utils.Operator))


    def createUser(self, username):
        self.users[username] = User(self, username)

    def pm(self, *message_parts):
        self.ircParent.pm(self, " ".join([codecs.decode(part) if isinstance(part, bytes) else part for part in message_parts]))

    def whisper(self, user, *message_parts):
        self.ircParent.whisper(user, " ".join([codecs.decode(part) if isinstance(part, bytes) else part for part in message_parts]))
