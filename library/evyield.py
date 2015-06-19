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

import args, clist, dbreader, hist, mypaf, vb


## evyield
##------------------------------------------------------------------- 
class evyield:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, name, variable, argstring = ""):

		self.mypaf     = mypaf
		self.db        = mypaf.db
		self.vb        = mypaf.vb

		self.name      = name.strip()
		self.variable  = variable.strip()
		self.alist     = args.args(argstring)
		self.built     = False


	## build
	##---------------------------------------------------------------
	def build(self, sources, categs):

		self.sources = sources
		self.categs  = categs

		self.yields = [[0. for cidx in range(len(categs))] for sidx in range(len(sources))]
		self.built  = True


	## count
	##---------------------------------------------------------------
	def count(self, sidx, cidx, weight = 1.):
		if len(self.yields) > sidx:
			self.yields[sidx][cidx] += weight
	

	## exportAsHist
	##---------------------------------------------------------------
	def exportAsHist(self):
		## exports the event yields as a hist instance

		h = hist.hist(self.mypaf, self.name, clist.clist(1, 0, 1), [self.name, "events"])
		h.build(self.sources, self.categs)

		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				h.setBinContent(sidx, cidx, 1, self.yields[sidx][cidx])
	

	## exportAsText
	##---------------------------------------------------------------
	def export(self):
		## returns the content of the event list as a string in readable form

		print "do nothing"


	## inject
	##---------------------------------------------------------------
	def inject(self, sidx, cidx, value):
		if len(self.yields) > sidx:
			self.yields[sidx][cidx] = value



