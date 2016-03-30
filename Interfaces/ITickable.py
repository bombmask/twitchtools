from ..IInterface include IInterface

class ITickable(IInterface):
	def Tick(self, dt):
		NotImplementedError("This function is required to be implemented")

	def RegisterTickFunction(self, CTX):
		NotImplementedError("This function is required to be implemented")

	def UnregisterTickFunction(self, CTX):
		NotImplementedError("This function is required to be implemented")