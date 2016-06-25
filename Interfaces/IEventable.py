# from future.utils import with_metaclass
from six import with_metaclass
import types
import sys

from ..IInterface import IInterface
from ..Interfaces.IExecutable import IExecutable

class RemakeList(type):
	def __init__(cls, name, bases, clsdict):
		cls.delagates = list()
		super(RemakeList, cls).__init__(name, bases, clsdict)

# Global Event Interface

class IEventable(with_metaclass(RemakeList, IInterface)):
	# __metaclass__ = RemakeList 
	#PY2 Only


	bAsyncCallback = False
	bAsyncDispatch = False
	
	delagates = []

	@classmethod
	def Dispatch(cls, *args, **kwargs):
		for delagate in cls.delagates:
			# print(delagate)
			if isinstance(delagate, (types.FunctionType, types.MethodType)):
				try:
					try:
						delagate(*args, **kwargs)
					except TypeError:
						print("TYPE ERROR?!?!")
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

	@classmethod
	def IsAsync(cls):
		return cls.bAsyncDispatch
		# NotImplementedError("This function is required to be implemented")

	@classmethod
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

