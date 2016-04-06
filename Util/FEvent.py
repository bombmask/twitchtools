import types
from ..Interfaces.IEventable import IEventable

class FEvent(IEventable):

	bAsyncCallback = False
	bAsyncDispatch = False
	
	delagates = []

	def __init__(self):
		self.delagates = list()

	
	def Dispatch(self, *args, **kwargs):
		for delagate in self.delagates:
			# print(delagate)
			if isinstance(delagate, types.FunctionType):
				delagate(*args, **kwargs)
			else:
				delagate.Execute(*args, **kwargs)

		#NotImplementedError("This function is required to be implemented")
		# Creating Global Event
	
	def IsAsync(self):
		return self.bAsyncDispatch
		# NotImplementedError("This function is required to be implemented")

	def Bind(self, Delagate):
		# print("binding delagate: {}:{} == {}".format(Delagate, IExecutable, issubclass(Delagate, IExecutable)))
		#NotImplementedError("This function is required to be implemented")
		if isinstance(Delagate, types.FunctionType):
			self.delagates.append(Delagate)
			# Assume it's a class, Test subclass
		try:
			if issubclass(Delagate, IExecutable):
				self.delagates.append(Delagate)
		except:
			pass

		try:
			if isinstance(Delagate, IExecutable):
				self.delagates.append(Delagate)
		except:
			pass
