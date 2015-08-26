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
import effmap, evlist, evyield, hist, lib, oblist, obyield


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
		self.vb.call("objcoll", "__init__", [self, mypaf, categories, sources], "Initializing the objcoll class.")

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

		self.vb.call("objcoll", "addEffMap", [self, name, definition, argstring, sources, categories], "Adding an EffMap to the object collection.")
		self.effmaps.append(effmap.effmap(self.mypaf, name, definition, argstring))

		if sources != [] and categories != []:
			self.effmaps[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addEvList
	##---------------------------------------------------------------
	def addEvList(self, name, variables, argstring = "", sources = [], categories = []):

		self.vb.call("objcoll", "addEvList", [self, name, variables, argstring, sources, categories], "Adding an EvList to the object collection.")
		self.evlists.append(evlist.evlist(self.mypaf, name, variables, argstring))

		if sources != [] and categories != []:
			self.evlists[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addEvYield
	##---------------------------------------------------------------
	def addEvYield(self, name, variable, argstring = "", sources = [], categories = []):

		self.vb.call("objcoll", "addEvYield", [self, name, variable, argstring, sources, categories], "Adding an EvYield to the object collection.")
		self.evyields.append(evyield.evyield(self.mypaf, name, variable, argstring))

		if sources != [] and categories != []:
			self.evyields[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addHist
	##---------------------------------------------------------------
	def addHist(self, name, dim, argstring = "", sources = [], categories = []):

		self.vb.call("objcoll", "addHist", [self, name, dim, argstring, sources, categories], "Adding a Hist to the object collection.")
		self.hists.append(hist.hist(self.mypaf, name, dim, argstring))

		if sources != [] and categories != []:
			self.hists[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addObList
	##---------------------------------------------------------------
	def addObList(self, objname, name, variables, argstring = "", sources = [], categories = []):

		self.vb.call("objcoll", "addObList", [self, objname, name, variables, argstring, sources, categories], "Adding an ObList to the object collection.")	
		self.oblists.append(oblist.oblist(self.mypaf, objname, name, variables, argstring))

		if sources != [] and categories != []:
			self.oblists[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## addObYield
	##---------------------------------------------------------------
	def addObYield(self, objname, name, variable, argstring = "", sources = [], categories = []):

		self.vb.call("objcoll", "addObYield", [self, objname, name, variable, argstring, sources, categories], "Adding an ObYield to the object collection.")	
		self.obyields.append(obyield.obyield(self.mypaf, objname, name, variable, argstring))

		if sources != [] and categories != []:
			self.obyields[-1].build(sources, categories)
			self.sources  .extend(sources)
			self.categories = categories


	## build
	##---------------------------------------------------------------
	def build(self):

		self.vb.call("objcoll", "build", [self], "Building the object collection.")
		self.buildEffMaps()
		self.buildEvLists()
		self.buildEvYields()
		self.buildHists()
		self.buildObLists()
		self.buildObYields()


	## buildEffMaps
	##---------------------------------------------------------------
	def buildEffMaps(self):

		self.vb.call("objcoll", "buildEffMaps", [self], "Building the list of EffMaps in the object collection.")
		if not all([e.built for e in self.effmaps]):
			for e in self.effmaps:
				e.build(self.sources, self.categories)


	## buildEvLists
	##---------------------------------------------------------------
	def buildEvLists(self):

		self.vb.call("objcoll", "buildEvLists", [self], "Building the list of EvLists in the object collection.")
		if not all([e.built for e in self.evlists]):
			for e in self.evlists:
				e.build(self.sources, self.categories)


	## buildEvYields
	##---------------------------------------------------------------
	def buildEvYields(self):

		self.vb.call("objcoll", "buildEvYields", [self], "Building the list of EvYields in the object collection.")
		if not all([e.built for e in self.evyields]):
			for e in self.evyields:
				e.build(self.sources, self.categories)


	## buildHists
	##---------------------------------------------------------------
	def buildHists(self):

		self.vb.call("objcoll", "buildHists", [self], "Building the list of Hists in the object collection.")
		if not all([h.built for h in self.hists]):
			for h in self.hists:
				h.build(self.sources, self.categories)


	## buildObLists
	##---------------------------------------------------------------
	def buildObLists(self):

		self.vb.call("objcoll", "buildObLists", [self], "Building the list of ObLists in the object collection.")
		if not all([o.built for o in self.oblists]):
			for o in self.oblists:
				o.build(self.sources, self.categories)


	## buildObYields
	##---------------------------------------------------------------
	def buildObYields(self):

		self.vb.call("objcoll", "buildObYields", [self], "Building the list of ObYields in the object collection.")
		if not all([o.built for o in self.obyields]):
			for o in self.obyields:
				o.build(self.sources, self.categories)


	## draw
	##---------------------------------------------------------------
	def draw(self):

		self.vb.call("objcoll", "draw", [self], "Drawing the objects in the object collection.")
		#if self.mypaf.imodule > 5: return
		self.drawHists()
		self.drawEffMaps()
		self.drawEvLists()


	## drawEffMaps
	##---------------------------------------------------------------
	def drawEffMaps(self):

		self.vb.call("objcoll", "drawEffMaps", [self], "Drawing the list of EffMaps in the object collection.")
		for e in self.effmaps:
			e.exportAsCSV()
			e.exportAsTXT()


	## drawEvLists
	##---------------------------------------------------------------
	def drawEvLists(self):

		self.vb.call("objcoll", "drawEvLists", [self], "Drawing the list of EvLists in the object collection.")
		for e in self.evlists:
			e.exportAsCSV()
			e.exportAsPick()


	## drawHists
	##---------------------------------------------------------------
	def drawHists(self):

		self.vb.call("objcoll", "drawHists", [self], "Drawing the list of Hists in the object collection.")
		for h in self.hists:
			h.draw()


	## getEffMap
	##---------------------------------------------------------------
	def getEffMap(self, name):

		self.vb.call("objcoll", "getEffMap", [self, name], "Returning an EffMap according to its name.")
		return lib.getObj(self.effmaps, name)


	## getEvList
	##---------------------------------------------------------------
	def getEvList(self, name):

		self.vb.call("objcoll", "getEvList", [self, name], "Returning an EvList according to its name.")
		return lib.getObj(self.evlists, name)


	## getEvYield
	##---------------------------------------------------------------
	def getEvYield(self, name):

		self.vb.call("objcoll", "getEvYield", [self, name], "Returning an EvYield according to its name.")
		return lib.getObj(self.evyields, name)


	## getHist
	##---------------------------------------------------------------
	def getHist(self, name):

		self.vb.call("objcoll", "getHist", [self, name], "Returning an Hist according to its name.")
		return lib.getObj(self.hists, name)


	## getHistBins
	##---------------------------------------------------------------
	def getHistBins(self, name):

		self.vb.call("objcoll", "getHistBins", [self, name], "Returning the bins of a Hist according to its name.")
		return lib.getObj(self.hists, name).getBins()


	## getHistDim
	##---------------------------------------------------------------
	def getHistDim(self, name):

		self.vb.call("objcoll", "getHistDim", [self, name], "Returning the dimension of a Hist according to its name.")
		return lib.getObj(self.hists, name).getDim()


	## getObList
	##---------------------------------------------------------------
	def getObList(self, name):

		self.vb.call("objcoll", "getObList", [self, name], "Returning an ObList according to its name.")
		return lib.getObj(self.oblists, name)


	## getObYield
	##---------------------------------------------------------------
	def getObYield(self, name):

		self.vb.call("objcoll", "getObYield", [self, name], "Returning an ObYield according to its name.")
		return lib.getObj(self.obyields, name)


	## injectHist
	##---------------------------------------------------------------
	def injectHist(self, name, hist, sidx = 0, cidx = 0):

		self.vb.call("objcoll", "injectHist", [self, name, hist, sidx, cidx], "Injecting a Hist to the object collection.")
		return lib.getObj(self.hists, name).inject(hist, sidx, cidx)


	## setCategs
	##---------------------------------------------------------------
	def setCategs(self, categs):
		self.vb.call("objcoll", "setCategs", [self, categs], "Setting the categories of the object collection.")
		self.categories = categs


	## setHistP
	##---------------------------------------------------------------
	def setHistP(self, name):
		self.vb.call("objcoll", "setHistP", [self, name], "Setting p variable of a Hist according to its name.")
		lib.getObj(self.hists, name).setP(True)


	## setInitial
	##---------------------------------------------------------------
	def setInitial(self):
		self.vb.call("objcoll", "setInitial", [self], "Setting initial for every Hist.")
		for h in self.hists:
			h.setInitial()


	## setNormalizedLumi
	##---------------------------------------------------------------
	def setNormalizedLumi(self):
		self.vb.call("objcoll", "setNormalizedLumi", [self], "Setting normalized to True for every Hist.")
		for h in self.hists:
			h.setNormalizedLumi()


	## setSources
	##---------------------------------------------------------------
	def setSources(self, sources):
		self.vb.call("objcoll", "setSources", [self, sources], "Setting the sources of the object collection.")
		self.sources = sources




