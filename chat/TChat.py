import socket 

from ..TObject import TObject
from .IChat import IChat
from ..Events import *
from ..Util import *

def RespondToPing(*args, **kwargs):
	if kwargs.get("message", False):
		if kwargs["message"].startswith("PING"):
			kwargs.get("object").SendRaw(kwargs["message"].replace("PING", "PONG").strip())


class TChat(TObject, IChat):
	def __init__(self, Server):
		self.server = Server
		self.conn = socket.socket()
		self.FOnStartup = FEvent.FEvent()
		self.FOnMessageRecv = FEvent.FEvent()
		self.FOnMessageSent = FEvent.FEvent()

		AStartup.AStartup.Bind(self.Start)
		AShutdown.AShutdown.Bind(self.Stop)

		self.FOnMessageRecv.Bind(RespondToPing)


	def Start(self):
		self.conn.connect(self.server)

		self.FOnStartup.Dispatch()

		# Spin up message thread 
		

	def Stop(self):
		self.SendRaw("QUIT")
		self.conn.close()

	def Join(self, channels):
		context = {
			"object":self, 
			"channels": channels
		}

		if not isinstance(channels, (list, tuple)):

			channels = (channels, )

		AJoinChannel.APreJoinChannel.Dispatch(context=context)

		for channel in channels:
			# This function may need to allow for 
			# sleeping between joins and 
			# being able to manipulate the strings
			# as well as providing a callback for joins
			self.SendRaw("JOIN #{}".format())

			AJoinChannel.AJoinChannel.Dispatch(context=context)

		AJoinChannel.APostJoinChannel.Dispatch(context=context)



	def Leave(self, channels):
		context = {
			"object":self, 
			"channels": channels
		}

		if not isinstance(channels, (list, tuple)):
			channels = (channels, )

		AJoinChannel.APreJoinChannel.Dispatch(context=context)

		for channel in channels:
			self.SendRaw("PART #{}".format(channel))
			AJoinChannel.AJoinChannel.Dispatch(context=context)

		AJoinChannel.APostJoinChannel.Dispatch(context=context)
		

	"""Basic Send Function"""
	def SendRaw(self, message):
		context = {
			"object":self, 
			"message": message
		}

		# Send message to server and append \r\n
		AMessage.APreMessageSent.Dispatch(context=context)
		
		message = (self.FOnMessageSent.Dispatch(context=context, message=message))
		self.conn.sendall(bytes(message + "\r\n", "UTF-8"))
		AMessage.AMessageSent.Dispatch(context=context)

		AMessage.APostMessageSent.Dispatch(context=context)

	def ReadRaw(self, *args, **kwargs):
		context = {
			"object":self,
			"message":""
		}

		AMessage.APreMessageRecieved.Dispatch(context=context)

		message = self.conn.recv(kwargs.get("buffer", 4096))
		context["message"] = message

		self.FOnMessageRecv.Dispatch(context=context)

		AMessage.AMessageRecieved.Dispatch(context=context)

		AMessage.APostMessageRecieved.Dispatch(context=context)
		return message

	def ReadByLines(self, *args, **kwargs):
		idx = 0
		whileTest = (lambda x: True if kwargs.get("amount", -1) == -1 else lambda x : x < kwargs.get("amount"))
		# textBuffer = ""
		# while whileTest(idx):
		# 	tmpBuffer = 
		# 	# End
		# 	idx += 1
		socketfile = self.conn.makefile(newline="\r\n", encoding="UTF-8", errors="replace")

		while whileTest(idx):
			yield socketfile.readline()

	def RequestTag(self, tag):

		self.SendRaw("CAP REQ :{}".format(tag))

	def PrivateMessage(self, channel, *message_parts):

		self.SendRaw("PRIVMSG #{channel} :{message}".format(channel=channel.strip('#'), message=" ".join(map(str, message_parts))))
