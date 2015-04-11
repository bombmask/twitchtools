#! /usr/bin/env python2.7

# import socket
# from sys import path 
# import os
# import thread
import time
import datetime


class Message(object):
    """
    Message : Prefix command params 

    """

    def __init__(self, raw_message):
        """ Message spec (@<tags> )?:<headers> (:<message>)?<CRLF> """
        self.raw = raw_message
        self.creation_time = datetime.datetime.now()
        #.strftime('%Y-%m-%d %H:%M')
        self.__dict__.update({
                "prefix": "X",
                "command" : "X",
                "params" : [],
                "message" : "X",
                "user" : ""
            })


        if self.raw[0] == "@":
            #Tags present
            self.ParseMessageTags(self.raw.split(" :")[0])
            self.ParseMessageMain(self.raw.split(" :",1)[1])

        elif self.raw[0] == ":":
            self.tags = False
            self.ParseMessageMain(self.raw.strip(":"))

        else:
            raise TypeError("String not valid message")


    def __str__(self):
        if False:
            tagsString = ""
            for k,v in self.tags.items():
                tagsString += k+"="+v+", "
        else:
            tagsString = ""

        return tagsString+" ".join([self.command, ", ".join(self.params), self.message])

    def ParseMessageMain(self, message_string):
        """ Exepcts ":<Prefix [user!host, host]> <Command> <Params> (( :) <Message>)? <<CR><LF>>" """
        message_split = message_string.split(" :", 2)
        headers = message_split[0]
        #Get <Prefix> and <Command>
        self.prefix, self.command = headers.split(" ")[:2]

        #Get <Params>
        self.params = headers.split(" ")[2:]

        #Optional <Message>
        if len(message_split) > 1:
            # print "[Message]:", "Incoming:", message_string # print "[Message]:", "List:", message_split # print "[Message]:", "RAW:", self.raw # print "[Message]:", "Message:",self.message 
            self.message = message_split[-1].strip()
            if "!" in self.prefix: self.user = self.prefix.split("!")[0]

        #Ensure <CRLF>


        return

        

    def ParseMessageTags(self, tagString):
        """ Exepcts "@<Tags>" """
        self.tags = {}
        tagString = tagString.strip("@")
        for pair in tagString.split(";"):
            tag, value = pair.split("=")

            value = [item for item in value.split("/")]

            self.tags[tag] = (value[0] if len(value) == 1 else value)


    @property 
    def channel(self):
        return self.params[0].strip("#")

    @property 
    def target(self):
        if self.command == "CLEARCHAT":
            return self.message

        return self.user

    def time(self):
        return self.creation_time.strftime('%Y-%m-%d %H:%M')