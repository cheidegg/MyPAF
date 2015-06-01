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
import args, clist, dbreader, objcoll, hscheme, lib, mypaf, vb


## output
##------------------------------------------------------------------- 
class output:

	cfg        = None
	db         = None
	input      = None
	mypaf      = None
	vb         = None

	treefiles  = None
	treecoll   = None

	#histcoll   = None
	histfile   = None

	file       = None	
	evlist     = None
	oblist     = None
	evyields   = None
	obyields   = None
	efficiency = None


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf):

		self.mypaf    = mypaf
		self.cfg      = mypaf.cfg
		self.db       = mypaf.db
		self.input    = mypaf.input
		self.vb       = mypaf.vb	

		self.objcoll  = objcoll.objcoll(self.mypaf)
		self.build()


	## build
	##---------------------------------------------------------------
	def build(self):

		if   self.mypaf.imodule == 1: return self.buildTree()
		elif self.mypaf.imodule == 2: return self.buildDraw()
		elif self.mypaf.imodule == 3: return self.buildPlot()
		elif self.mypaf.imodule == 4: return self.buildScan()
		elif self.mypaf.imodule == 5: return self.buildStat()
		#elif self.mypaf.imodule == 6: return self.buildHist()
		elif self.mypaf.imodule == 7: return self.buildPubl()
		
		return False


	## buildDraw
	##---------------------------------------------------------------
	def buildDraw(self):

		self.openFile()

		## initialize the histogram collection
		if self.mypaf.input.cfg.getVar("dataset") == "y":
			sources = lib.attr(self.mypaf.input.datasets, "name")
		else:
			sources = lib.attr(self.mypaf.input.samples, "name")
		categories = lib.column(self.mypaf.input.selection, 1)
		self.objcoll.setSources(sources)
		self.objcoll.setCategs(categories)

		## get the histogram info and initialize the histograms
		for entry in self.mypaf.input.output:
			if entry[0] == "plot" or entry[0] == "root":
				alist = args.args(entry[3])
				if not alist.has("obs"):
					self.vb.warning("observable is not given for plot. plot ignored.")
				else:
					binargs, names = lib.prepareHistInfo(self.db, alist)
					self.objcoll.addHist(entry[1], binargs, names, entry[3])
					if entry[0] == "plot": self.objcoll.setHistP(entry[1])


		## build the histogram collection
		#self.histcoll.build()
		self.objcoll.build()


	## buildHist
	##---------------------------------------------------------------
	def buildHist(self):

		self.mypaf.runTier2Modules(self.mypaf.input.modules)

		## initialize also every histogram produced before as a (trivial)scheme
		self.schemes = []
		
		## trivial schemes
		if hasattr(self, "objcoll") and self.objcoll != None:
			for h in self.objcoll.hists:
				self.schemes.append(hscheme.hscheme(self.mypaf, "hist", h.var))
				self.schemes[-1].setTrivial(h)
			for evl in self.objcoll.evlists:
				self.schemes.append(hscheme.hscheme(self.mypaf, "elhist", evl.name))
				self.schemes[-1].setTrivial(evl)
			for evy in self.objcoll.evyields:
				self.schemes.append(hscheme.hscheme(self.mypaf, "eyhist", evy.name))
				self.schemes[-1].setTrivial(evy)
			for obl in self.objcoll.oblists:
				self.schemes.append(hscheme.hscheme(self.mypaf, "olhist", obl.name))
				self.schemes[-1].setTrivial(obl)
			for oby in self.objcoll.obyields:
				self.schemes.append(hscheme.hscheme(self.mypaf, "oyhist", oby.name))
				self.schemes[-1].setTrivial(oby)	
	
		## non-trivial schemes
		self.sdefs = self.mypaf.input.cfg.getAll("schemes")
		for entry in self.sdefs:
			self.schemes.append(hscheme.hscheme(self.mypaf, entry[0], entry[1], entry[2], entry[3]))


	## buildPlot
	##---------------------------------------------------------------
	def buildPlot(self):

		## actually, what we want to do is different than in the DRAW case
		## DRAW: take samples * selection * observables => hists for all cases
		## PLOT: take hists * selection => hists
		## do we need the histcoll? 

		## todo:
		## - sketch workflow:
		##   + input file (no further specification)
		##   + selection does selection on the bins, manipulates this histogram
		##   + output is plot or root, i.e. a list of histograms
		##   + output hist in canvas or larger file, specify path
		##   + need to say which dataset, group, gengroup this is to be used
		##   + need to specify binning, style

		self.openFile()

		## reserve hist with one source per hist
		for entry in self.mypaf.input.output:
			if entry[0] == "plot" or entry[0] == "file":
				alist = args.args(entry[3])
				if not alist.has("obs") and not alist.has("obs1"):
					self.vb.warning("observable is not given for plot. plot ignored.")
				else:
					## actually, find the selection which has the good name?
					categories = lib.column(self.mypaf.input.selection, 1)
					source = alist.get("source")
					binargs, names = lib.prepareHistInfo(self.db, alist)
					self.objcoll.addHist(entry[1], binargs, names, entry[3], [source], categories)
					if entry[0] == "plot": 
						self.objcoll.setHistP(entry[1]) 

	## WHAT TO DO ABOUT GEN INFO?


	## buildScan
	##---------------------------------------------------------------
	def buildScan(self):
		
		if self.mypaf.input.cfg.getVar("dataset") == "y":
			sources = lib.attr(self.mypaf.input.datasets, "name")
		else:
			sources = lib.attr(self.mypaf.input.samples, "name")
		categories = lib.column(self.mypaf.input.selection, 1)
		self.objcoll.setSources(sources)
		self.objcoll.setCategs(categories)

		#for entry in self.mypaf.input.output:
		#	if entry[0] == "evlist" or entry[0] == "oblist":
				


	## buildStat
	##---------------------------------------------------------------
	def buildStat(self):
		
		if self.mypaf.input.cfg.getVar("dataset") == "y":
			sources = lib.attr(self.mypaf.input.datasets, "name")
		else:
			sources = lib.attr(self.mypaf.input.samples, "name")
		categories = lib.column(self.mypaf.input.selection, 1)
		self.objcoll.setSources(sources)
		self.objcoll.setCategs(categories)
		


	## buildTree
	##---------------------------------------------------------------
	def buildTree(self):

		## to be rewritten
		print "to be rewritten"


	## finalize
	##---------------------------------------------------------------
	def finalize(self):

		if   self.mypaf.imodule == 1: return self.finalizeTree()
		elif self.mypaf.imodule == 2: return self.finalizeDraw()
		elif self.mypaf.imodule == 3: return self.finalizePlot()
		elif self.mypaf.imodule == 4: return self.finalizeScan()
		elif self.mypaf.imodule == 5: return self.finalizeStat()
		elif self.mypaf.imodule == 6: return self.finalizeHist()
		elif self.mypaf.imodule == 7: return self.finalizePubl()
		
		return False


	## finalizeDraw
	##---------------------------------------------------------------
	def finalizeDraw(self):
		## draw and save the histograms

		self.objcoll.draw()


	## finalizeHist
	##---------------------------------------------------------------
	def finalizeHist(self):
		print "nothing to do"


	## finalizePlot
	##---------------------------------------------------------------
	def finalizePlot(self):
		## draw and save the histograms

		self.objcoll.draw()


	## finalizeScan
	##---------------------------------------------------------------
	def finalizeScan(self):
		print "nothing to do"


	## openFile
	##---------------------------------------------------------------
	def openFile(self, postpend = ""):

		if self.file != None:
			self.file.Close()
		if postpend != "": postpend = "_" + postpend
		self.file = ROOT.TFile(self.mypaf.prodpath + "file" + postpend + ".root", "recreate") 


	## openTree
	##---------------------------------------------------------------
	def openTree(self, treename = "tree", filename = ""):

		if self.tree != None:
			self.vb.warning("existing tree is tried to be reopened. closing it first")
			self.tree.Close()
			openFile(filename)
		if self.file == None:
			openFile(filename)
		self.tree = ROOT.TTree(treename, treename)


	## save
	##---------------------------------------------------------------
	def save(self):
		## write everything from this class to the production directory
		## copy cfg file to the production directory

		if self.file != None:
			#self.file.Write()
			self.file.Close()

		#if self.evlist != None:
		#	self.evlist.close()

		#if self.oblist != None:
		#	self.oblist.close()

		#if self.evyields != None:
		#	file = open(self.mypaf.prodpath + "eyyields.txt", "w")
		#	text = self.evyields.export()
		#	print text
		#	file.write(text)
		#	file.close()
	
		#if self.obyields != None:
		#	file = open(self.mypaf.prodpath + "obyields.txt", "w")
		#	text = self.obyields.export()
		#	print text
		#	file.write(text)
		#	file.close()

		#if self.efficiency != None:
		#	file = open(self.mypaf.prodpath + "efficiency.txt", "w")
		#	text = self.efficiency.export()
		#	print text
		#	file.write(text)
		#	file.close()

	

