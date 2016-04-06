from __future__ import print_function
from . import Engine


__all__ = [
	"IInterface",
	"TObject",
	"TObjectBase",
	"TObjectCore",
	"WorldContext",
	
	"Interfaces",
	"Chat",
	"API",

]


DEBUG = False

Start = Engine.StartEngine
GetEngine = Engine.GetEngine
CreateWCTX = Engine.CreateWCTX
GetCurrentWCTX = Engine.GetCurrentWCTX


# Log "macro"
def LOG(*args, **kwargs):
	# No printing durring shipping unless important
	if not DEBUG and kwargs.get("LEVEL", False) == "PRINT":
		return

	prefix = ""
	if kwargs.get("LOG", False):
		prefix = kwargs["LOG"]

	print(prefix + " ".join(args), end=kwargs.get("end", "\n"))

