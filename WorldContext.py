from .TObjectBase import TObjectBase
from .Interfaces.ISerializeable import ISerializeable
from .Interfaces.IExecutable import IExecutable

class WSPAWNINSTRUCTION(TObjectBase, ISerializeable):
	pass
	
class WCTX(TObjectBase):
	instructions = []

	def CreateInstruction(self, voidSpawner):
		if issubclass(voidSpawner, IExecutable):
			self.instructions.append(voidSpawner)

	def RunInstructions(self, Engine):
		for instruct in self.instructions:
			instruct.Execute(engine=Engine, WCTX=self)
