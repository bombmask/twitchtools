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



Start = Engine.StartEngine
GetEngine = Engine.GetEngine
CreateWCTX = Engine.CreateWCTX
GetCurrentWCTX = Engine.GetCurrentWCTX