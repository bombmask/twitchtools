#!/usr/bin/env python3.5
"""
Copyright: Firestack 2015
-------------------------
IRC Class that implements more advanced basic functions
"""

import socket

from . import IRC_Basic

class IRC_Advanced(IRC_Basic.IRC_Basic):

    def __init__(self):
        # Ensure we build the object super class
        super().__init__()
        self.flags = {}
        self.Message_Buffer = []

    def Close(self):
        # Provide super interface to close objects on exit.
        self.Disconnect()

    """Send Function that combines arbitrary args"""
    def Raw(self, *message_parts):
        message = (" ".join( map( str, message_parts ) ) + "\r\n")

        # Debugging script
        if self.flags.get("write", False):
            print(message[:-2])

        # Send message to server and append \r\n
        self.link.sendall(bytes(message, "UTF-8"))


    """Read Function: >> Simple << Message Buffer"""
    def Read(self, timeout=500):
        # You really shouldn't use this function, makefile() is a better way to do this.
        # You can miss important information with this function.
        if len(self.Message_Buffer) == 0:
            self.Message_Buffer.append(self.link.read(4096).split("\r\n"))

        return self.Message_Buffer.pop(0)


    def ConnectTo(self, serverIP, portNumber):
        self.link.connect((serverIP, portNumber))


    def Disconnect(self):
        self.Raw("QUIT")
        self.link.close()


    def Request(self, cap):
        self.Raw("CAP REQ :{}".format(cap))


    def PrivateMessage(self, channel, *message_parts):
        self.Raw("PRIVMSG", "#{channel} :{message}".format(channel=channel.strip('#'), message=" ".join(message_parts)))
