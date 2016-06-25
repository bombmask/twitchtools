from .FLookupDispatch import FLookupDispatch
from .EEnum import Enum



class ECommandType(Enum):
	UNKNOWN     =-4
	NOCALL      =-3
	ALLTEXT     =-2
	ALL         =-1
	#-------------#
	PRIVMSG     = 0
	PING        = 1
	NOTICE      = 2
	NUMBERS     = 3
	ROOMSTATE   = 4
	JOIN        = 5
	PART        = 6
	CAP         = 7
	USERSTATE   = 8
	HOSTTARGET  = 9
	CLEARCHAT   = 10
	WHISPER     = 11


class FTwitchCommandDispatch(FLookupDispatch):
	def Add(self, Key, Value):
		try:
			self.Lookup[Key].append(Value)
		except KeyError:
			self.Lookup[Key] = [Value]

	def Exec(self, Key, *args, **kwargs):
		for delagate in self.Lookup[Key]:
			delagate(*args, **kwargs)
			


