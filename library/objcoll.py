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

#import effmap, evlist, evyield, hist, lib, oblist, obyield, roc
import evlist, hist, lib, oblist


## objcoll
##------------------------------------------------------------------- 
class objcoll:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, categories = [], sources = []):

		self.categories = categories
		self.sources    = sources

		self.mypaf      = mypaf
		self.db         = mypaf.db
		self.vb         = mypaf.vb

		self.effmaps    = []
		self.evlists    = []
		self.evyields   = []
		self.hists      = []
		self.oblists    = []
		self.obyields   = []
		self.rocs       = []


	## addEffMap
	##---------------------------------------------------------------
	def addEffMap(self, name):

		self.effmaps.append(effmap.effmap(self.mypaf, name))


	## addHist
	##---------------------------------------------------------------
	def addHist(self, name, binargs, labels, argstring = "", sources = [], categories = []):

		self.hists.append(hist.hist(self.mypaf, name, binargs, labels, argstring))

		if sources != [] and categories != []:
			self.hists[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories



	## addHistSC
	##---------------------------------------------------------------
	def addHistSC(self, var, binargs, labels, arglist, source, categories):
	
		self.hists     .append(hist.hist(self.mypaf, var, binargs, labels, argstring))
		self.hists[-1].build([source], categories)
		self.sources   .append(source)
		self.categories = categories


	## build
	##---------------------------------------------------------------
	def build(self):

		self.buildHists()


	## buildHists
	##---------------------------------------------------------------
	def buildHists(self):

		if not all([h.isBuilt() for h in self.hists]):
			for h in self.hists:
				h.build(self.sources, self.categories)


	## draw
	##---------------------------------------------------------------
	def draw(self):

		self.drawHists()


	## drawHists
	##---------------------------------------------------------------
	def drawHists(self):

		for h in self.hists:
			h.draw()


	## getHistBins
	##---------------------------------------------------------------
	def getHistBins(self, var):

		idx = lib.findElmAttr(self.hists, "var", var)
		return self.hists[idx].getBins()


	## getHistDim
	##---------------------------------------------------------------
	def getHistDim(self, var):

		idx = lib.findElmAttr(self.hists, "var", var)
		return self.hists[idx].getDim()


	## getHist
	##---------------------------------------------------------------
	def getHist(self, var):

		idx = lib.findElmAttr(self.hists, "var", var)
		return self.hists[idx]


	## injectHist
	##---------------------------------------------------------------
	def injectHist(self, var, hist, sidx = 0, cidx = 0):

		idx = lib.findElmAttr(self.hists, "var", var)
		self.hists[idx].inject(hist, sidx, cidx)


	## setInitial
	##---------------------------------------------------------------
	def setInitial(self):

		for h in self.hists:
			h.setInitial()


	## setHistP
	##---------------------------------------------------------------
	def setHistP(self, name):

		idx = lib.findElmAttr(self.hists, "var", name)
		self.hists[idx].setP(True)




