# 
# The Root of ALL Twitch tools
# 
# Naming conventions/Prefixes
# F = Utility functions/Objects... Floats XD
# T = Classes that inherit from TObject
# I = Interfaces for classes # Interfaces contain no implementation unless explicitly needed.
# S = Data Structures: JUST for passing around data. No Functions
# E = Event responders
# A = Async classes and Events
# U = Utility classes
# X = Factories
# E = Enumerators
#
#
# Tabs over spaces
# Cammel Case
#


class TObjectCore(object):
	pass




#@TODO
"""
Integrate TChat into engine calls. 
Bind Start to threading function with 
async callbacks and continue with main loop. 
Bind Engine Stop to TChat and allow TChat to shutdown self and Engine
"""