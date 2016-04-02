from ..IInterface import IInterface

class IExecutable(IInterface):
	@classmethod
	def __call__(self, *args, **kwargs):
		return self.Execute(*args, **kwargs)

	@classmethod
	def Execute(self, *args, **kwags):
		pass
