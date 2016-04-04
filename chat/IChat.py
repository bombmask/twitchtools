from ..IInterface import IInterface

class IChat(IInterface):
	def Start(self):
		NotImplementedError("This function is required to be implemented")

	def Stop(self):
		NotImplementedError("This function is required to be implemented")

	def Join(self, sChannel):
		NotImplementedError("This function is required to be implemented")

	def Leave(self, sChannel):
		NotImplementedError("This function is required to be implemented")
