#################################################################
#################################################################
##                                                             ##
## MyPAF - My Purpose Analysis Framework                       ##
## Constantin Heidegger                                        ##
## March 2015                                                  ##
##                                                             ##
#################################################################
#################################################################
#################################################################



## cfgobj
##-------------------------------------------------------------------
class cfgobj:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, region, type, name, definition, arguments = ""):

		self.region     = region
		self.type       = type
		self.name       = name
		self.definition = definition
		self.argstring  = arguments


	## setSource
	##---------------------------------------------------------------
	def setSource(self, source):
		self.source = source

	
