from .TObjectCore import TObjectCore
from .WorldContext import WCTX 
from .Events import *
# from .Events.APostInitalize import APostInitalize

from time import sleep
from threading import Thread
import multiprocessing


class Engine(TObjectCore):
	def AddWorldCTX(self, WCTXObject):
		self.CTX = WCTXObject
		
		return

	def Initalize(self):
		self.CTX.RunInstructions(self)

		self.PostInitalize()

	def PostInitalize(self):
		
		APostInitalize.APostInitalize.Dispatch()
		pass
		# Callback procedures
		# Only avalible to plugin content and factory modification

	def Start(self):
		print("Started Engine")

		self.Shutdown()
		print("Shutdown Engine")
		pass

	def InitalizeEventSubsystem(self):
		pass

	def InitalizeObjectFactory(self):
		self.CreateObjectSubfactoryInitalizer()

	def InitalizeAsyncSubsystem(self):
		self.DetachTickThread()
		self.DetachEventThread()

	def Shutdown(self):
		self.CleanupTickThread()
		self.CleanupEventThread()
		self.CleanupUnusedResources()
		AShutdown.AShutdown.Dispatch()
		pass

	###############################
	## Threaded Async Submodules ##
	#@TODO
	# Colapse into seprate classes
	# Convert event function to event
	# manager. 
	#
	# Convert tick to tick manager
	# with "smart" resources
	###############################

	def DetachTickThread(self):
		#Detach the tick thread you dummy
		# This is something that is runnning a loop. 
		# Needs to be async and ticking as much as the CPU will
		# let it along the lines of the internal tick requirements
		self.TickThreadHandle = Thread(target=self.TickThreadRuntime)
		self.TickThreadHandle.start()
		
		pass

	def CleanupTickThread(self):
		self.bTickThreadRuntimeKeepTicking = False
		self.TickThreadHandle.join()

	def TickThreadRuntime(self):
		self.bTickThreadRuntimeKeepTicking = True
		while self.bTickThreadRuntimeKeepTicking:
			pass
			# print("Hello Ticking World!")

	def DetachEventThread(self):
		#Detach the Event thread please
		self.EventThreadHandle = Thread(target=self.EventThreadRuntime)
		self.EventThreadHandle.start()
		pass

	def CleanupEventThread(self):
		# Tell it to stop
		self.EventThreadHandle.join()

	def EventThreadRuntime(self):
		pass

	#######################
	## Object Subfactory ##
	#######################

	def CreateObjectSubfactoryInitalizer(self):
		pass

	def NewObject(self, cls):
		pass

	###########################
	## Internal Engine Loops ##
	###########################
	def Watchman(self):


		pass

	def FBL(self):

		pass

	###################################
	## Runtime Optimiation inspector ##
	###################################

	def Reroute(self):
		pass

	def RemapTick(self):
		pass

	def RemapEventCallers(self):
		pass

	def CleanupUnusedResources(self):
		pass


def CreateWCTX(CTXObjectRoot = WCTX, *args, **kwargs):
	CreateWCTX.CTX = CTXObjectRoot(*args, **kwargs)
	return GetCurrentWCTX()

def GetCurrentWCTX():
	return CreateWCTX.CTX

def StartEngine():
	StartupTwitchToolsEngineRuntimeWithModules()

def IsEngineValid(Engine):
	#@TODO: Implement this
	return True

# A Get Current Engine Macro
def GetEngine():
	# Do some checking to make sure engine is valid
	return StartupTwitchToolsEngineRuntimeWithModules.PrivateEngineObjectRoot

# Sparkplug
def StartupTwitchToolsEngineRuntimeWithModules():
	StartupTwitchToolsEngineRuntimeWithModules.PrivateEngineObjectRoot = Engine()

	# Ensure Engine Is Valid
	if not IsEngineValid(GetEngine()): return 1

	# Load modules
	LoadPlugins(GetEngine())

	# Setup plugin content
	PostLoadPlugins(GetEngine())

	# Load prereq files
	# Initalize Config
	LoadConfigs(GetEngine())
	
	# Create and initalize callback events
	GetEngine().InitalizeEventSubsystem()

	# Create Object Factory
	GetEngine().InitalizeObjectFactory()
	
	# Setup Async pool
	GetEngine().InitalizeAsyncSubsystem()

	GetEngine().AddWorldCTX(GetCurrentWCTX())
	# Begin main boot cycle after initalizing modules
	# callback events are initalized. Begin procedures
	GetEngine().Initalize()


	# Mainloop. Block till finished or any cancel event is called
	# @TODO: Config setting to attach engine to async task and return and not block
	# bEngineShouldBlockOnStart

	GetEngine().Start()

	return 0


def LoadPlugins(Engine):
	pass

def PostLoadPlugins(Engine):
	pass

def LoadConfigs(Engine):
	# Get module config for WCTX object
	# Load new WCTX
	# Get permissions
	# Setup new world
	
	pass