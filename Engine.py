from .TObjectCore import TObjectCore

class Engine(TObjectCore):
	
	def Initalize(self):
		pass

	def PostInitalize(self):
		pass
		# Callback procedures
		# Only avalible to plugin content and factory modification

	def Start(self):
		pass

	def InitalizeEventSubsystem(self):
		pass

	def InitalizeObjectFactory(self):
		self.CreateObjectSubfactoryInitalizer()

	def InitalizeAsyncSubsystem(self):
		self.DetachTickThread()
		self.DetachEventThread()

	###############################
	## Threaded Async Submodules ##
	###############################

	def DetachTickThread(self):
		#Detach the tick thread you dummy
		pass

	def TickThreadRuntime(self):
		pass

	def DetachEventThread(self):
		#Detach the Event thread please
		pass

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
		def IsAsync(self):
			return true

		pass

	def FBL(self):
		def IsAsync(self):
			return true
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



def StartEngine():
	StartupTwitchToolsEngineRuntimeWithModules()


def IsEngineValid(Engine):
	#@TODO: Implement this
	return true

# A Get Current Engine Macro
def GetEngine():
	# Do some checking to make sure engine is valid
	return StartupTwitchToolsEngineRuntimeWithModules.PrivateEngineObjectRoot

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
	GetEngine().InitalizeEventSystem()

	# Create Object Factory
	GetEngine().InitalizeObjectFactory()

	# Begin main boot cycle after initalizing modules
	# callback events are initalized. Begin procedures
	GetEngine().Initalize()

	# Setup Async pool
	GetEngine().InitalizeAsyncSubsystem()

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