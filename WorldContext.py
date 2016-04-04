from .TObjectBase import TObjectBase
from .Interfaces.ISerializeable import ISerializeable
from .Interfaces.IExecutable import IExecutable

class WSPAWNINSTRUCTION(TObjectBase, ISerializeable):
	pass
	
class WCTX(TObjectBase):
	instructions = []
	BindedFuncCall = None

	def Bind(self, Singleton):
		if hasattr(Singleton, "__call__"):
			self.BindedFuncCall = Singleton


	def CreateInstruction(self, voidSpawner):
		if issubclass(voidSpawner, IExecutable):
			self.instructions.append(voidSpawner)

	def RunInstructions(self, Engine):
		if self.BindedFuncCall:
			self.BindedFuncCall(Engine, WCTX)

		for instruct in self.instructions:
			instruct.Execute(engine=Engine, WCTX=self)


