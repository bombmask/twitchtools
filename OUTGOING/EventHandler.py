#!/usr/bin/env python3.5
"""
Copyright: Firestack 2015
-------------------------
Basic Event Handling object.
"""
from enum import Enum

class TEvent(Enum):
    UNKNOWN     =-4
    NOCALL      =-3
    ALLTEXT     =-2
    ALL         =-1
    #-------------#
    PRIVMSG     = 0
    PING        = 1
    NOTICE      = 2
    NUMBERS     = 3
    ROOMSTATE   = 4
    JOIN        = 5
    PART        = 6
    CAP         = 7
    USERSTATE   = 8
    HOSTTARGET  = 9
    CLEARCHAT   = 10
    WHISPER     = 11

class EventHandler(object):
    TYPE = TEvent.NOCALL
    REWINDABLE = False

    def __init__(self):
        super().__init__()

    def Execute(self, ref, *args):
        raise NotImplementedError(
            "You need to Implement the 'Execute' method of '{}'".format(self.__class__.__name__)
        )

    @classmethod
    def Once(self, ref):
        pass
