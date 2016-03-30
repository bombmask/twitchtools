#!/usr/bin/env python3.5
"""
Copyright: Firestack 2015
-------------------------
IRC Class to Implement Event Based Message response
"""

import socket
import threading

from . import IRC_Advanced
from . import EventHandler

class IRC_Event(IRC_Advanced.IRC_Advanced):
    """docstring for IRC_Event"""

    def __init__(self):
        # Ensure we build the objects super class
        super().__init__()

        #Clarify what type of object this is by using dict()
        self.callback_objects = dict()
        self.netfile = self.link.makefile(
            buffering=1,
            newline="\r\n",
            encoding="UTF-8",
            errors="replace"
        )

    def Read(self, timeout=500):
        # Bad implementation. replace.
        return list(self.ReadLines(lines=1, timeout=timeout))[0]

    def ReadLines(self, timeout=None, lines=0, return_messages=True):
        # Ensure value is set, called once per function call.
        # When used as iterator it's only called once
        self.link.settimeout(timeout)

        # Remake file (memory leak?) because of possible timeout error
        # self.netfile.close()
        # self.netfile = self.link.makefile(
        #     buffering=1,
        #     newline="\r\n",
        #     encoding="UTF-8",
        #     errors="replace"
        # )

        # Count lines
        lines_read = 0
        try:
            for line in self.netfile:

                self.Intercept(line)

                if return_messages == True:
                    # Yeild current message to client
                    yield line

                # Check if we reached the asked for amount of lines
                if lines != 0:
                    lines_read += 1
                    if lines_read >= lines:

                        break

        except socket.timeout as e:
            # Stop if timeout

            raise StopIteration

    def ReadFile(self, timeout=None, lines=0):
        # Ensure value is set, called once per function call.
        # When used as iterator it's only called once
        self.link.settimeout(timeout)

        # Remake file (memory leak?) because of possible timeout error
        self.netfile.close()
        self.netfile = self.link.makefile(
            buffering=1,
            newline="\r\n",
            encoding="UTF-8",
            errors="replace"
        )

        # Count lines
        lines_read = 0

        for line in self.netfile:

            self.Intercept(line)

            # Check if we reached the asked for amount of lines
            if lines != 0:
                lines_read += 1
                if lines_read >= lines:
                    break



    def RegisterClass(self, UserEvent):
        if not issubclass(UserEvent, EventHandler.EventHandler):
            raise TypeError("UserEvent is not of EventHandler")

        try:
            self.callback_objects[UserEvent.TYPE].append(UserEvent)

        except KeyError as E:
            self.callback_objects[UserEvent.TYPE] = [UserEvent]

    def RegisterObject(self, UserObject):
        if not isinstance(UserObject, EventHandler.EventHandler):
            raise TypeError("UserObject is not of EventHandler")

        try:
            self.callback_objects[UserObject.TYPE].append(UserObject)
        except KeyError as E:
            self.callback_objects[UserObject.TYPE] = [UserObject]

    def RegisterSpawnable(self, UserClassSpawnable):
        pass

    def Intercept(self, message):
        print(message)

    def MainLoop(self, fork=False):
        if not fork:
            self.ReadFile()
            return

        self.thread_object = threading.Thread(
            target=self.ReadFile,
            kwargs={},
            daemon=True
        )

        self.thread_object.start()

        return self.thread_object
