from ..TObject import TObject
from ..Interfaces.IExecutable import IExecutable


class FLookupDispatch(TObject):

	def __init__(self):
		super(FLookupDispatch, self).__init__()
		self.Lookup = {}

	def Add(self, Key, Value):
		if issubclass(Value, IExecutable):
			self.Lookup[Key] = Value

	def Exec(self, Key, *args, **kwargs):
		return self.Lookup[Key](*args, **kwargs)

class FLookupDispatchLower(FLookupDispatch):
	"""docstring for FLookupDispatchLower"""
	def Add(self, Key, Value):
		return super(FLookupDispatchLower, self).Add(Key.lower(), Value)

	def Exec(self, Key, *args, **kwargs):
		return super(FLookupDispatchLower, self).Exec(Key.lower(), *args, **kwargs)


