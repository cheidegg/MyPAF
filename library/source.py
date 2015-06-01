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
import dbreader, lib


## source
##-------------------------------------------------------------------
class source:

	#name        = "zombie"
	mypaf       = None
	db          = None
	vb          = None

	#type        = "none"
	#color       = 0
	#fillstyle   = 0
	#linestyle   = 0
	#markerstyle = 0
	#lname       = ""

	#samples     = []



	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, name):
		## initializes the source class

		self.mypaf = mypaf
		self.db    = mypaf.db
		self.vb    = mypaf.vb

		self.name = name

		self.load()


	## addSample
	##---------------------------------------------------------------
	def addSample(self, name, path, tree):
		self.samples.append(sample.sample(self.mypaf, name, path, tree))


	## getSample
	##--------------------------------------------------------------- 
	def getSample(self, name):
		idx = lib.findElmAttr(self.samples, "name", name)
		return self.samples[idx]


	## load
	##---------------------------------------------------------------
	def load(self):

		vars = self.db.getRow("sources", "name == '" + self.name + "'")

		self.type        = vars[1]
		self.lname       = vars[2]
		self.dstype      = vars[3]
		self.cgroup      = vars[4]
		self.color       = vars[5]
		self.fillstyle   = vars[6]
		self.linestyle   = vars[7]
		self.linewidth   = vars[8]
		self.markerstyle = vars[9]
		self.markersize  = vars[10]


