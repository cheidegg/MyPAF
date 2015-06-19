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
import evlist, evyield, hist, lib, oblist, obyield


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
	def addEffMap(self, name, definition, argstring = "", sources = [], categories = []):

		self.effmaps.append(effmap.effmap(self.mypaf, name, definition, argstring))

		if sources != [] and categories != []:
			self.effmaps[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addEvList
	##---------------------------------------------------------------
	def addEvList(self, name, variables, argstring = "", sources = [], categories = []):

		self.evlists.append(evlist.evlist(self.mypaf, name, variables, argstring))

		if sources != [] and categories != []:
			self.evlists[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addEvYield
	##---------------------------------------------------------------
	def addEvYield(self, name, variable, argstring = "", sources = [], categories = []):

		self.evyields.append(evyield.evyield(self.mypaf, name, variable, argstring))

		if sources != [] and categories != []:
			self.evyields[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addHist
	##---------------------------------------------------------------
	def addHist(self, name, binargs, labels, argstring = "", sources = [], categories = []):

		self.hists.append(hist.hist(self.mypaf, name, binargs, labels, argstring))

		if sources != [] and categories != []:
			self.hists[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addObList
	##---------------------------------------------------------------
	def addObList(self, objname, name, variables, argstring = "", sources = [], categories = []):

		self.oblists.append(oblist.oblist(self.mypaf, objname, name, variables, argstring))

		if sources != [] and categories != []:
			self.oblists[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addObYield
	##---------------------------------------------------------------
	def addObYield(self, objname, name, variable, argstring = "", sources = [], categories = []):

		self.obyields.append(obyield.obyield(self.mypaf, objname, name, variable, argstring))

		if sources != [] and categories != []:
			self.obyields[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## build
	##---------------------------------------------------------------
	def build(self):

		self.buildEvLists()
		self.buildEvYields()
		self.buildHists()
		self.buildObLists()
		self.buildObYields()


	## buildEvLists
	##---------------------------------------------------------------
	def buildEvLists(self):

		if not all([e.built for e in self.evlists]):
			for e in self.evlists:
				e.build(self.sources, self.categories)


	## buildEvYields
	##---------------------------------------------------------------
	def buildEvYields(self):

		if not all([e.built for e in self.evyields]):
			for e in self.evyields:
				e.build(self.sources, self.categories)


	## buildHists
	##---------------------------------------------------------------
	def buildHists(self):

		if not all([h.built for h in self.hists]):
			for h in self.hists:
				h.build(self.sources, self.categories)


	## buildObLists
	##---------------------------------------------------------------
	def buildObLists(self):

		if not all([o.built for o in self.oblists]):
			for o in self.oblists:
				o.build(self.sources, self.categories)


	## buildObYields
	##---------------------------------------------------------------
	def buildObYields(self):

		if not all([o.built for o in self.obyields]):
			for o in self.obyields:
				o.build(self.sources, self.categories)


	## draw
	##---------------------------------------------------------------
	def draw(self):

		#if self.mypaf.imodule > 5: return
		self.drawHists()


	## drawHists
	##---------------------------------------------------------------
	def drawHists(self):

		for h in self.hists:
			h.draw()


	## getEvList
	##---------------------------------------------------------------
	def getEvList(self, name):

		return lib.getObj(self.evlists, name)


	## getEvYield
	##---------------------------------------------------------------
	def getEvYield(self, name):

		return lib.getObj(self.evyields, name)


	## getHist
	##---------------------------------------------------------------
	def getHist(self, name):

		return lib.getObj(self.hists, name)


	## getHistBins
	##---------------------------------------------------------------
	def getHistBins(self, name):

		return lib.getObj(self.hists, name).getBins()


	## getHistDim
	##---------------------------------------------------------------
	def getHistDim(self, name):

		return lib.getObj(self.hists, name).getDim()


	## getObList
	##---------------------------------------------------------------
	def getObList(self, name):

		return lib.getObj(self.oblists, name)


	## getObYield
	##---------------------------------------------------------------
	def getObYield(self, name):

		return lib.getObj(self.obyields, name)


	## injectHist
	##---------------------------------------------------------------
	def injectHist(self, name, hist, sidx = 0, cidx = 0):

		return lib.getObj(self.hists, name).inject(hist, sidx, cidx)


	## setCategs
	##---------------------------------------------------------------
	def setCategs(self, categs):
		self.categories = categs


	## setHistP
	##---------------------------------------------------------------
	def setHistP(self, name):
		lib.getObj(self.hists, name).setP(True)


	## setInitial
	##---------------------------------------------------------------
	def setInitial(self):

		for h in self.hists:
			h.setInitial()


	## setSources
	##---------------------------------------------------------------
	def setSources(self, sources):
		self.sources = sources




