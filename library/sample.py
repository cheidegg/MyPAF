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
import cfg, input, lib, mypaf


## sample
##------------------------------------------------------------------- 
class sample:

	#color      = ROOT.kBlack
	db         = None
	#dsname     = ""
	#file       = None
	#legendname = ""
	mypaf      = None
	#name       = "empty"
	#nentries   = 0
	#nevents    = ""
	#ngenevts   = ""
	#path       = "" 
	#tree       = None
	#treename   = ""
	vb         = None


	## __init__
	##--------------------------------------------------------------- 
	def __init__(self, mypaf, name, definition, treename = "tree", dirname = ""):

		self.mypaf = mypaf
		self.db    = mypaf.db
		self.vb    = mypaf.vb

		self.paths = [lib.usePath(self.mypaf.inputpath, self.mypaf.input.cfg.getVar("inputdir"), p, dirname) for p in definition.split()]

		#if path[0] != "/" and path.find("dcap://") == -1 and path.find("root://") == -1: path = mypaf.inputpath + path

		self.name = name
		#self.path = path
		self.treename = treename
		
		#self.load()
		self.setDbParams()	


	## close
	##---------------------------------------------------------------
	def close(self):

		self.file.Close()

		del self.tree
		del self.file
	
		self.file = None
		self.tree = None	


	## load
	##--------------------------------------------------------------- 
	def load(self):
		## loads and opens the TFile and TTree

		self.tree     = ROOT.TChain(self.treename)
		for p in self.paths:
			self.tree.Add(p)

		#self.file     = ROOT.TFile.Open(self.paths[0], "read")
		#self.tree     = self.file.Get(self.treename)
		#self.nentries = self.tree.GetEntries()

		


	## setDbParams
	##--------------------------------------------------------------- 
	def setDbParams(self):	
		## sets the parameters stored in the db

		params = self.db.getAll("samples", "name=='" + self.name + "'", "all")
		if len(params) > 4:
			self.legendname = params[1]
			self.color      = params[2]
			self.nevents    = params[3]
			self.ngenevts   = params[4]
			self.dsname     = params[5]







