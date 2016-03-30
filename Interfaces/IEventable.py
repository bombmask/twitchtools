from ..IInterface include IInterface

class IEventable(IInterface):
	def Dispatch(self):
		NotImplementedError("This function is required to be implemented")

	def IsAsync(self):
		NotImplementedError("This function is required to be implemented")
