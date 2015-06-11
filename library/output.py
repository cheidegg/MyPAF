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

import ROOT, sys
import args, clist, dbreader, objcoll, hscheme, lib, mypaf, vb


## output
##------------------------------------------------------------------- 
class output:

	#cfg        = None
	#db         = None
	#input      = None
	#mypaf      = None
	#vb         = None

	#treefiles  = None
	#treecoll   = None

	#histcoll   = None
	#histfile   = None

	#file       = None	
	#evlist     = None
	#oblist     = None
	#evyields   = None
	#obyields   = None
	#efficiency = None


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf):

		self.mypaf    = mypaf
		self.cfg      = mypaf.cfg
		self.db       = mypaf.db
		self.input    = mypaf.input
		self.vb       = mypaf.vb	
		self.file     = None

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
	def buildDraw(self, objnames = []):

		self.openFile()

		## initialize the histogram collection
		#self.objcoll.setSources(self.mypaf.input.sources)
		#self.objcoll.setCategs([o.name for o in self.mypaf.input.cfg.getObjs("region=='selection' and (type=='none' or type=='tree')")])

		objlist = self.mypaf.input.cfg.getObjs("region=='output' and (type=='file' or type=='plot')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)

		## get the histogram info and initialize the histograms
		for var in objlist:
			alist = args.args(var.argstring)
			if not alist.has("obs") and not alist.has("obsx"):
				self.vb.warning("observable is not given for plot. plot ignored.")
				continue
			
			categories = [o.name for o in self.mypaf.findSelections(["tree"], alist)]

			binargs, labels = lib.prepareHistInfo(self.db, alist)

			self.objcoll.addHist(var.name, binargs, labels, var.argstring, self.mypaf.input.sources, categories)
			if var.type == "plot": self.objcoll.setHistP(var.name)
			del alist


		## build the histogram collection
		#self.objcoll.build()


	## buildHist
	##---------------------------------------------------------------
	def buildHist(self):

		self.mypaf.runTier2Modules(self.mypaf.input.modules, self.mypaf.input.objects)

		## initialize also every histogram produced before as a (trivial)scheme
		self.schemes = []
		
		## trivial schemes
		if hasattr(self, "objcoll") and self.objcoll != None:
			for h in self.objcoll.hists:
				self.schemes.append(hscheme.hscheme(self.mypaf, "hist", h.name))
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
		#self.sdefs = self.mypaf.input.cfg.getAll("schemes")
		for s in self.mypaf.input.cfg.getObjs("region=='schemes'"):
			self.schemes.append(hscheme.hscheme(self.mypaf, s.type, s.name, s.definition, s.argstring))


	## buildPlot
	##---------------------------------------------------------------
	def buildPlot(self, objnames = []):

		self.openFile()

		objlist = self.mypaf.input.cfg.getObjs("region=='output' and (type=='file' or type=='plot')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)

		## reserve hist with one source per hist
		for var in objlist:
			alist = args.args(var.argstring)
			if not alist.has("obs") and not alist.has("obsx"):
				self.vb.warning("observable is not given for plot. plot ignored.")
				continue

			## actually, find the selection which has the good name?
			categories = [o.name for o in self.mypaf.findSelections(["tree"], alist)]
			source = alist.get("source")
			binargs, names = lib.prepareHistInfo(self.db, alist)
			self.objcoll.addHist(var.name, binargs, names, var.argstring, [source], categories)
			if var.type == "plot": self.objcoll.setHistP(var.name) 
			del alist
	## WHAT TO DO ABOUT GEN INFO?



	## buildScan
	##---------------------------------------------------------------
	def buildScan(self, objnames = []):
		
		## initialize the histogram collection
		self.objcoll.setSources(self.mypaf.input.sources)
		self.objcoll.setCategs([o.name for o in self.mypaf.input.cfg.getObjs("region=='selection' and (type=='none' or type=='tree')")])

		objlist = self.mypaf.input.cfg.getObjs("region=='output' and (type=='evlist' or type=='oblist')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)

		for var in objlist:
			alist = args.args(var.argstring)
			if var.type == "oblist" and not alist.has("obj"):
				self.vb.warning("object is not given for object list. list ignored.")
				continue
			if var.type == "evlist":
				self.objcoll.addEvList(var.name, var.definition.split(":"), var.argstring)
				self.objcoll.addEvYield(var.name, var.definition.split(":")[0], var.argstring)
			elif var.type == "oblist":
				self.objcoll.addObList(alist.get("obj"), var.name, var.definition.split(":"), var.argstring)
				self.objcoll.addObYield(alist.get("obj"), var.name, var.definition.split(":")[0], var.argstring)
			del alist
		self.objcoll.build()


	## buildStat
	##---------------------------------------------------------------
	def buildStat(self, objnames = []):
		
		## initialize the histogram collection
		self.objcoll.setSources(self.mypaf.input.sources)
		self.objcoll.setCategs([o.name for o in self.mypaf.input.cfg.getObjs("region=='selection' and (type=='none' or type=='tree')")])

		objlist = self.mypaf.input.cfg.getObjs("region=='output' and (type=='evyield' or type=='obyield')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)

		for var in objlist:
			alist = args.args(var.argstring)
			if var.type == "obyield" and not alist.has("obj"):
				self.vb.warning("object is not given for object yield. yield ignored.")
				continue
			if var.type == "evyield":
				self.objcoll.addEvYield(var.name, var.definition.split(":")[0], var.argstring)
			elif var.type == "obyield":
				self.objcoll.addObYield(alist.get("obj"), var.name, var.definition.split(":")[0], var.argstring)
			#elif var.type == "effmap":
			#	self.objcoll.addEffMap(var.name, var.definition, var.argstring)
			#elif var.type == "roc":
			#	self.objcoll.addRoc(var.name, var.definition, var.argstring)
			del alist
		self.objcoll.build()


	## buildTree
	##---------------------------------------------------------------
	def buildTree(self):

		## to be rewritten
		print "to be rewritten"


	## finalize
	##---------------------------------------------------------------
	def finalize(self):

		self.objcoll.draw()


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

	

