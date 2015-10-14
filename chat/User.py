#! /usr/bin/env python2.7

import time
import datetime
import twitchtools.utils.Printer

class User(object):
	"""

	"""

	def __init__(self, CHANOBJ, name):
		super(User, self).__init__()
		self.messages = []
		self.name = name
		self.channelParent = CHANOBJ
		self.creation_time = datetime.datetime.now()
		self.term = twitchtools.utils.Printer("User.#{}.{}".format(self.channelParent.name, self.name))

	def addMessage(self, message):
		self.term("Appending message:",message.message)
		self.messages.append(message)

	def whisper(self, message):
		self.channelParent.whisper(self, message.strip("/me"))
