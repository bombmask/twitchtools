#!/usr/bin/env python3.5
# __all__ = ["IRC", "Channel", "User", "Message"]
# from .IRC import IRC
# from .Channel import Channel
# from .Message import Message
# from .User import User
# from os.path import dirname, basename, isfile
# import glob
# modules = glob.glob(dirname(__file__)+"/*.py")
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
__all__ = [
	"IChat",
	"TChat", 
	"TIRC",
]
