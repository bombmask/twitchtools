import types
import sys

from ..Interfaces.IEventable import IEventable

class FEvent(IEventable):

	bAsyncCallback = False
	bAsyncDispatch = False
	
	delagates = []

	def __init__(self):
		self.delagates = list()

	
	def Dispatch(cls, *args, **kwargs):
		for delagate in cls.delagates:
			# print(delagate)
			if isinstance(delagate, (types.FunctionType, types.MethodType)):
				try:
					try:
						delagate(*args, **kwargs)
					except TypeError as e:
						print("TYPE ERROR?!?! {}".format(e))
						sys.last_traceback.print_last()	
						delagate()
				except Exception as e:
					print("Delagate Failed {} @ {}".format(delagate, e))

			else:
				try:
					delagate.Execute(*args, **kwargs)
				except Exception as e:
					print("Delagate Failed {} @ {}".format(delagate, e))



		#NotImplementedError("This function is required to be implemented")
		# Creating Global Event

	def IsAsync(cls):
		return cls.bAsyncDispatch
		# NotImplementedError("This function is required to be implemented")

	
	def Bind(cls, Delagate):
		# print("binding delagate: {}:{} == {}".format(Delagate, IExecutable, issubclass(Delagate, IExecutable)))
		#NotImplementedError("This function is required to be implemented")
		if isinstance(Delagate, (types.FunctionType, types.MethodType)):
			cls.delagates.append(Delagate)
			return True
			# Assume it's a class, Test subclass
		try:
			if issubclass(Delagate, IExecutable):
				cls.delagates.append(Delagate)
				return True
		except:
			print("Delagate {} failed to pass subclass test in {}".format(Delagate, cls))

		try:
			if isinstance(Delagate, IExecutable):
				cls.delagates.append(Delagate)
				return True
		except:
			print("Delagate {} failed to pass instance test in {}".format(Delagate, cls))

		return False
