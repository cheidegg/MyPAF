#################################################################
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

import ROOT
import args


## styleargs
##-------------------------------------------------------------------
class styleargs:

	alist    = None
	defaults = []
	defs     = []
	name     = "zombie"


	## __init__
	##---------------------------------------------------------------
	def __init__(self, name, instance = "1", color = "ROOT.kBlack"):
		## initializes the hstyle class

		self.style = name
		self.i     = int(instance)
		self.color = color

		self.build()


	## build
	##---------------------------------------------------------------	
	def build(self):

		self.alist = args.args("color=" + self.color)

		## mult
		if   self.style == "mult":
			if   self.i == 1: 
				self.alist.set("draw1mode"  , "pe"  )
				self.alist.set("fillstyle"  , "0"   )
				self.alist.set("linestyle"  , "1"   )
				self.alist.set("linewidth"  , "2"   )
				self.alist.set("markerstyle", "8"   )
				self.alist.set("markersize" , "1.0" )
			elif self.i == 2:
				self.alist.set("draw1mode"  , "hist")
				self.alist.set("fillstyle"  , "1001")
				self.alist.set("linestyle"  , "1"   )
				self.alist.set("linewidth"  , "2"   )
				self.alist.set("markerstyle", "8"   )
				self.alist.set("markersize" , "1.0" )
			else            :
				self.alist.set("draw1mode"  , "hist") 
				self.alist.set("fillstyle"  , "0"   )
				self.alist.set("linestyle"  , "1"   )
				self.alist.set("linewidth"  , "2"   )
				self.alist.set("markerstyle", "8"   )
				self.alist.set("markersize" , "1.0" )

		## default
		else:
			if   self.i == 1: 
				self.alist.set("draw1mode"  , "pe"  )
				self.alist.set("fillstyle"  , "0"   )
				self.alist.set("linestyle"  , "1"   )
				self.alist.set("linewidth"  , "2"   )
				self.alist.set("markerstyle", "8"   )
				self.alist.set("markersize" , "1.8" )
			else            : 
				self.alist.set("draw1mode"  , "hist") 
				self.alist.set("fillstyle"  , "0"   )
				self.alist.set("linestyle"  , "1"   )
				self.alist.set("linewidth"  , "2"   )
				self.alist.set("markerstyle", "8"   )
				self.alist.set("markersize" , "1.8" )


	## get
	##---------------------------------------------------------------	
	def get(self, key):
		return self.alist.get(key)


	## getAll
	##---------------------------------------------------------------	
	def getAll(self, key):
		return self.alist.getAll(key)


	## reinit
	##---------------------------------------------------------------	
	def reinit(self, name, instance = "1", color = "ROOT.kBlack"):

		self.style = name
		self.i     = int(instance)
		self.color = color

		del self.alist
		self.build()


	## set
	##---------------------------------------------------------------	
	def set(self, key, value):
		return self.alist.set(key, value)



