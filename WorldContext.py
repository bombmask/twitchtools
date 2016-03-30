from .TObjectBase import TObjectBase
from .Interfaces.ISerializeable import ISerializeable

class WSPAWNINSTRUCTION(TObjectBase, ISerializeable):
	pass
	
class WCTX(TObjectBase, ISerializeable):
	instructions = []