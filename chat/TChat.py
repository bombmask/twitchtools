import socket 
import six

from ..TObject import TObject
from .IChat import IChat
from ..Events import *
from ..Util import *

def RespondToPing(*args, **kwargs):
	if kwargs.get("context", False):
		if kwargs["context"]["message"].startswith("PING"):
			# print(kwargs["context"]["message"])
			kwargs["context"]["object"].SendRaw(kwargs["context"]["message"].replace("PING", "PONG").strip())



class TChat(TObject, IChat):
	def __init__(self, Server):
		self.ForceEnd = False
		self.server = Server
		self.conn = socket.socket()

		self.FOnStartup = FEvent.FEvent()
		self.FOnMessageRecv = FEvent.FEvent()
		self.FOnMessageSent = FEvent.FEvent()
		self.FOnLineRecv = FEvent.FEvent()

		AStartup.AStartup.Bind(self.Start)
		AShutdown.AShutdown.Bind(self.Stop)

		self.FOnMessageRecv.Bind(RespondToPing)
		self.FOnLineRecv.Bind(RespondToPing)




	def Start(self):
		print("Connecting to {}".format(self.server))

		self.conn.connect(self.server)

		self.FOnStartup.Dispatch(context={"object":self})

		# Spin up message thread
		#TEMP
		for i in self.ReadByLines():
			pass
		

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
			self.SendRaw("JOIN #{}".format(channel))

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
		
		self.FOnMessageSent.Dispatch(context=context, message=message)
		if six.PY3:
			self.conn.sendall(bytes(message + "\r\n", "UTF-8"))

		else:
			self.conn.sendall(message + "\r\n")

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
		context = {
			"object":self,
			"message":""
		}

		idx = 0
		whileTest = (lambda x: True if kwargs.get("amount", -1) == -1 else lambda x : x < kwargs.get("amount"))
		# textBuffer = ""
		# while whileTest(idx):
		# 	tmpBuffer = 
		# 	# End
		# 	idx += 1
		if six.PY3:
			socketfile = self.conn.makefile(newline="\r\n", encoding="UTF-8", errors="replace")
		else:
			socketfile = self.conn.makefile()

		while whileTest(idx) and not self.ForceEnd:
			
			m = socketfile.readline()
			m = m.strip()
			context["message"] = m
			AMessage.APreMessageRecieved.Dispatch(context=context)
			self.FOnLineRecv.Dispatch(context=context)
			
			yield m
			
			idx += 1

	def RequestTag(self, tag):

		self.SendRaw("CAP REQ :{}".format(tag))

	def PrivateMessage(self, channel, *message_parts):

		self.SendRaw("PRIVMSG #{channel} :{message}".format(channel=channel.strip('#'), message=" ".join(map(str, message_parts))))
