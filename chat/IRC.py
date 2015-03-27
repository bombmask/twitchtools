#! /usr/bin/env python2.7

import socket
# import thread
from sys import path 
import os
path.append(os.path.abspath(r"C:\Users\bombmask\Source"))

import twitchtools.login



# class IRC:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port

#     def sock_init(self):
#         try:
#             self.irc = socket.socket()
#             self.irc.settimeout(600)
#         except Exception as e:
#             print("Failed to create socket.")
#             raise

#     def sock_connect(self):
#         try:
#             self.irc.connect((self.host, self.port))
#         except Exception as e:
#             print("Failed to connect to the host.")
#             raise

#     def send_raw(self, msg):
#         self.irc.sendall("{}\r\n".format(msg).encode("utf-8"))

#     def send_pass(self, password):
#         self.send_raw("PASS {}".format(password))

#     def send_nick(self, nick):
#         self.send_raw("NICK {}".format(nick))

#     def send_join(self, channel):
#         self.send_raw("JOIN #{}".format(channel))

#     def send_pm(self, channel, msg):
#         self.send_raw("PRIVMSG #{} :{}".format(channel, msg))

#     def sock_raw_recv(self, amount):
#         msg = self.irc.recv(amount)
#         if msg:
#             return msg
#         elif msg == "":
#             raise ValueError
#         else:
#             return None

#     def sock_recv(self, amount):
#         msg = self.sock_raw_recv(amount)
#         try:
#             msg = msg.decode("utf-8")
#         except AttributeError as e:
#             return None

#         if msg.startswith("PING"):
#             self.send_raw(msg.replace("PING", "PONG"))
#         return msg

#     def sock_disconnect(self):
#         try:
#             self.send_raw("QUIT")
#         except Exception as e:
#             pass
#         finally:
#             self.irc.close()

#     def destroy_socket(self):
#         del self.irc



class IRC(object):
    """
    IRC((Address, port), [(user, pass), (Profile object)])
    """
    user = None

    channels = {}

    def __init__(self, AP = None, USER = None):
        self.link = socket.socket();

        if IRC:
            self.server(AP)

        if USER:
            self.credentials(USER)

        if IRC and USER:
            self.connect()
            self.login()

    def server(self, AP):
        self.IRCNAME = AP

    def credentials(self, USER):
        if isinstance(USER, (tuple, list)):
            self.user = twitchtools.login.Profile(USER[0], username=USER[0], oauth=USER[1])

        elif isinstance(USER, twitchtools.login.Profile):
            self.user = USER

        else:
            raise TypeError("User is not of correct type")

        

    def login(self):
        self.password()
        self.nick()

    def connect(self):
        print "Attempting to connect to :",' @ '.join(map(str,self.IRCNAME)),'\n','...'*3
        self.link.connect(self.IRCNAME)
        
    def disconnect(self):
        self.raw("QUIT")
        self.link.close()

    def raw(self, message):
        self.link.sendall("{}\r\n".format(message))

    def nick(self):
        self.raw("NICK {}".format(self.user.name))
        
    def password(self):
        self.raw("PASS {}".format(self.user.password))

    def join(self, channel):
        #If channel containsa  '#' already get rid if it
        self.raw("JOIN #{}".format(channel))
        #Create channel object and set up redirection to that object storage
        #Save channel object to local hash
        #Return channel object to user

    def part(self, channel):
        self.raw("PART {}".format(channel))

    def pm(self, CHANNELOBJ, message):
        self.raw("PRIVMSG #{} :{}".format(CHANNELOBJ.channel, message))

    def read(self, output = False, amount = 512, timeout = -1):
        self.link.settimeout((None if timeout < 0 else float(timeout)))
        try:
            incoming = self.link.recv(amount)
        except socket.timeout as e:
            print e
        finally:
            pass

        if output:
            print incoming

        self.parse(incoming)

    def parse(self, incoming):
        pass
        """
        for i in messages:
            self.distrubute(i)
        """

    def distrubute(self, message):
        pass
        """
        Read channel
        Send to channel
        else if not channel 
        send to global (all?)

        """

class Channel(object):
    """
    Channel(IRCobject, name)
    """

    users = {}

    def __init__(self, name):
        super(Channel, self).__init__()
        self.name = name
    
    def enter_message(self, message):
        pass
        
    def enter_user(self, username):
        self.users[username] = User(username)

class User(object):
    """

    """
    messages = []
    def __init__(self, name):
        pass

    def enter_message(self, message):
        pass

if __name__ == '__main__':
    m = IRC(("irc.twitch.tv", 6667), twitchtools.login.Profile(r"C:\Users\bombmask\Source\garden\twitch\bomb_mask"))
    m.read(True, timeout = 10)
    m.disconnect()
    k = raw_input("press enter to exit...")