import socket 

from ..TObject import TObject
from .IChat import IChat
from ..Events import *


class TChat(TObject, IChat):
	def __init__(self, Server):
		self.server = Server
		self.conn = socket.socket()

		AStartup.AStartup.Bind(self.Start)
		AShutdown.AShutdown.Bind(self.Stop)


	def Start(self):
		self.conn.connect(self.server)

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
		
		self.conn.sendall(bytes(message + "\r\n", "UTF-8"))
		AMessage.AMessageSent.Dispatch(context=context)

		AMessage.APostMessageSent.Dispatch(context=context)

	def ReadRaw(self, *args, **kwargs):
		context = {
			"object":self,
			"message":""
		}

		AMessage.APreMessageRecieved.Dispatch(context=context)

	def ReadByLines(self, *args, **kwargs):
		pass



		
