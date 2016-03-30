from ..IInterface import IInterface


# Interfaces contain no implementation unless explicitly needed.
class IChat(IInterface):
	def Start(self):
		NotImplementedError("This function is required to be implemented")

	def End(self):
		NotImplementedError("This function is required to be implemented")

	def Join(self, sChannel):
		NotImplementedError("This function is required to be implemented")