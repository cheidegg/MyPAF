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

import sys
import args, cfg, cfgobj, dbreader, lib, mypaf, source, vb


## input
##------------------------------------------------------------------- 
class input:

	cfg        = None
	db         = None
	mypaf      = None
	vb         = None


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, cfgfile):


		self.mypaf = mypaf
		self.cfg   = cfg.cfg(self, cfgfile)
		self.db    = mypaf.db
		self.vb    = mypaf.vb
		self.vb.call("input", "__init__", [self, mypaf, cfgfile], "Initializing input class.") 

		self.build()
		self.setSources()


	## build
	##---------------------------------------------------------------
	def build(self):

		self.vb.modulein()
		self.vb.call("input", "build", [self], "Building the module.")

		if self.mypaf.imodule == 6: return self.buildHist()
		#if   self.mypaf.imodule == 1: return self.buildTree()
		#elif self.mypaf.imodule == 2: return self.buildDraw()
		#elif self.mypaf.imodule == 3: return self.buildPlot()
		#elif self.mypaf.imodule == 4: return self.buildScan()
		#elif self.mypaf.imodule == 5: return self.buildStat()
		#elif self.mypaf.imodule == 6: return self.buildHist()
		#elif self.mypaf.imodule == 7: return self.buildPubl()
		
		return False


	## buildDraw
	##---------------------------------------------------------------
	#def buildDraw(self):

	#	idir = self.cfg.getVar("inputdir")
	#	iobj = self.cfg.getVar("inputtree")

	#	## better treatment of the sources!!! 

	#	self.sources = []
	#	for s in self.cfg.getAll("input", "type=='tree'", "name-args"):
	#		name  = s[0]
	#		path  = self.mypaf.inputfile(idir, s[1])
	#		alist = args.args(s[2])
	#		tree  = self.mypaf.inputobject(iobj, alist.get("tree"))

	#		dsname = self.db.getVar("samples", s[0], "dataset")
	#		idx = lib.findElmAttr(self.sources, "name", dsname)
	#		if idx == -1:
	#			ds = source.source(self.mypaf, dsname)
	#			self.sources.append(ds)
	#			idx = len(self.sources)-1
	#		self.sources[idx].addSample(s[0], path, tree)

	#	self.samples = []
	#	for ds in self.sources:
	#		self.samples.extend(ds.samples)

	#	self.selection = [["tree", "none", ""]]
	#	self.selection.extend(self.cfg.getAll("selection", "type=='tree'"))
	#	self.output    = self.cfg.getAll("output", "(type=='file' or type=='plot')")


	## buildHist
	##---------------------------------------------------------------
	def buildHist(self):

		self.vb.call("input", "buildHist", [self], "Building the hist module.")

		## collect input / output of other modules? run other modules in runHist ? 

		self.schemes = self.cfg.getAll("schemes")
		self.input   = self.cfg.getAll("input")
		self.output  = self.cfg.getAll("output")
		self.modules = []
		self.objects = []
		ignore = []

		for i, scheme in enumerate(self.schemes):
			needs     = scheme[2].strip().split()
			for n in needs:
				n = n.strip()
				needstype = lib.getElmVar(self.output, 1, n, 0)
				if needstype == "tree":
					self.vb.warning("Invalid input given to scheme. The scheme is ignored. Make sure that all objects used by the scheme are defined in the cfg file.")
					ignore.append(i)
				elif needstype == "file" or needstype == "plot":
					needsdef = lib.getElmVar(self.output, 1, n, 2)
					if needsdef[0:4] == "FILE" or needsdef[0:4] == "HIST":
						self.modules = lib.addToVectorIfMissing(self.modules, "plot")
					else:
						self.modules = lib.addToVectorIfMissing(self.modules, "draw")
					self.objects = lib.addToVectorIfMissing(self.objects, n) 
				elif needstype == "evlist" or needstype == "oblist":
					self.modules = lib.addToVectorIfMissing(self.modules, "scan") 
					self.objects = lib.addToVectorIfMissing(self.objects, n) 
				elif needstype == "evyield" or needstype == "obyield" or needstype == "effmap" or needstype == "roc":
					self.modules = lib.addToVectorIfMissing(self.modules, "stat") 
					self.objects = lib.addToVectorIfMissing(self.objects, n) 

		## remove all modules where we had invalid input
		## not necessary to remove the objects from those modules as they won't be drawn
		self.modules = lib.removeFromVector(self.modules, ignore)


	## buildPlot
	##---------------------------------------------------------------
	#def buildPlot(self):

	#	idir = self.cfg.getVar("inputdir")
	#	self.files  = self.cfg.getAll("input", "(type=='file' or type=='root')")

	#	for entry in self.files:
	#		entry[2] = self.mypaf.inputfile(idir, entry[2])

	#	self.output = self.cfg.getAll("output", "(type=='file' or type=='plot')")
	#	## no selection?
	#	self.selection = [["tree", "none", ""]]
	#	#self.selection.extend(self.cfg.getAll("selection", "type=='tree'"))


	## buildScan
	##---------------------------------------------------------------
	#def buildScan(self):

	#	idir = self.cfg.getVar("inputdir")
	#	iobj = self.cfg.getVar("inputtree")

	#	## better treatment of the sources!!! 

	#	self.sources = []
	#	for s in self.cfg.getAll("input", "type=='tree'", "name-args"):
	#		name  = s[0]
	#		path  = self.mypaf.inputfile(idir, s[1])
	#		alist = args.args(s[2])
	#		tree  = self.mypaf.inputobject(iobj, alist.get("tree"))

	#		dsname = self.db.getVar("samples", s[0], "dataset")
	#		idx = lib.findElmAttr(self.sources, "name", dsname)
	#		if idx == -1:
	#			source = source.source(self.mypaf, dsname)
	#			self.sources.append(ds)
	#			idx = len(self.sources)-1
	#		self.sources[idx].addSample(s[0], path, tree)

	#	self.samples = []
	#	for ds in self.sources:
	#		self.samples.extend(ds.samples)

	#	self.selection = [["tree", "none", ""]]
	#	self.selection.extend(self.cfg.getAll("selection", "type=='tree'"))
	#	self.output    = self.cfg.getAll("output", "type=='plot' or type=='root'")



	## buildTree
	##---------------------------------------------------------------
	#def buildTree(self):

	#	idir = self.cfg.getVar("inputdir")
	#	iobj = self.cfg.getVar("inputtree")

	#	## better treatment of the sources!!! 

	#	self.sources = []
	#	for s in self.cfg.getAll("input", "type=='tree'", "name-args"):
	#		name  = s[0]
	#		path  = self.mypaf.inputfile(idir, s[1])
	#		alist = args.args(s[2])
	#		tree  = self.mypaf.inputobject(iobj, alist.get("tree"))

	#		self.samples.append(sample.sample(self.mypaf, s[0], path, tree))

	#	self.evtsel = []
	#	self.objsel = []
	#	for s in self.cfg.getAll("selection", "type=='tree'"):
	#		alist = args.args(s[3])
	#		if alist.has("obj"):
	#			self.objsel.append(s)
	#		else:
	#			self.evtsel.append(s)

	#	self.output    = self.cfg.getAll("output", "type=='tree'")


	## setSources
	##---------------------------------------------------------------
	def setSources(self):
		## source can be
		## - sample
		## - dataset
		## - group
		## - gengroupbasic
		## - gengroupraw
		## - gengroupfine
		## - custom
		## source variable in header can take, only applies to tree input!
		## - sample
		## - dataset
		## - group

		self.vb.call("input", "setSources", [self], "Setting the sources of this instance.")

		self.sources = []

		if not self.cfg.hasVar("source"):
			self.vb.error("Default source is not specified in the header of the cfg file.")

		hs = self.cfg.hasVar("source")
		sn = self.cfg.getVar("source")
		
		for i, iobj in enumerate(self.cfg.getObjs("region=='input' and type=='tree'")):
			alist = args.args(iobj.argstring)

			if not iobj.type == "tree" and not alist.has("source"): 
				self.vb.error("No source is specified for input object " + iobj.name + ".")

			## source given to this input object
			if alist.has("source"): 
				s = alist.get("source")

			## source not given, take default defined in header
			else:
				if not iobj.type == "tree":			
					self.vb.error("No source is specified for input object " + iobj.name + ".")

				if sn == "dataset":
					s = self.db.getVar("samples", iobj.name, "dataset")
				elif sn == "group":
					s = self.db.getVar("samples", iobj.name, "group")
				else:
					s = iobj.name

			sidx = lib.findElm(self.sources, s)
			if sidx == -1:
				self.sources.append(s)
				sidx = len(self.sources) - 1

			iobj.setSource(sidx)


		for i, iobj in enumerate(self.cfg.getObjs("region=='output'")):
			alist = args.args(iobj.argstring)
			if alist.has("source"):
				sidx = lib.findElm(self.sources, alist.get("source"))
				if sidx == -1:
					self.sources.append(alist.get("source"))
					sidx = len(self.sources) - 1


