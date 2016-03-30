from ..IInterface import IInterface

class ISerializeable(IInterface):
	def Serialize(self):
		NotImplementedError("This function is required to be implemented")
		
	def Deserialize(self):
		NotImplementedError("This function is required to be implemented")