#!/usr/bin/env python3.5
"""
Copyright: Firestack 2015
-------------------------
Basic IRC Class ment for extention.
"""

import socket

class IRC_Basic(object):

    def __init__(self):
        # Ensure we build the object super class
        super().__init__()
        # Build socket connection for base irc
        self.link = socket.socket()


    """Basic Send Function"""
    def Raw(self, message):
        # Send message to server and append \r\n
        self.link.sendall(bytes(message + "\r\n", "UTF-8"))


    """Basic Read Function"""
    def Read(self, timeout=500):
        return self.link.recv(4096)

    """
    This function is provided to all subclasses as
    a way of bypassing init arguments and starting the
    IRC's connection and callbacks when the client is
    ready for the connections to be made after variables
    and configs have been set. IRC_Basic does not implement
    Start because it is a very basic class designed for
    extention rather than use. While it can be used it
    is not often useful as it puts all of the work in the
    user's hands intead of the classes internal code.

    Start can be added to the classes __init__ based
    on certain inheritance.
    """
    def Start():
        pass
