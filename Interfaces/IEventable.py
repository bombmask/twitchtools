# from future.utils import with_metaclass
from six import with_metaclass

from ..IInterface import IInterface
from ..Interfaces.IExecutable import IExecutable

class RemakeList(type):
	def __init__(cls, name, bases, clsdict):
		cls.delagates = list()
		super(RemakeList, cls).__init__(name, bases, clsdict)

class IEventable(with_metaclass(RemakeList, IInterface)):
	# __metaclass__ = RemakeList

	bAsyncCallback = False
	bAsyncDispatch = False
	
	delagates = []

	@classmethod
	def Dispatch(cls):
		for delagate in cls.delagates:
			# print(delagate)
			delagate.Execute()

		#NotImplementedError("This function is required to be implemented")
		# Creating Global Event

	@classmethod
	def IsAsync(cls):
		return cls.bAsyncDispatch
		NotImplementedError("This function is required to be implemented")

	@classmethod
	def Bind(cls, Delagate):

		# print("binding delagate: {}:{} == {}".format(Delagate, IExecutable, issubclass(Delagate, IExecutable)))
		#NotImplementedError("This function is required to be implemented")
		if issubclass(Delagate, IExecutable):
			cls.delagates.append(Delagate)


