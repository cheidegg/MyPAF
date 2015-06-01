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

import args, cfg, dbreader, lib, mypaf, source, vb


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

		self.build()


	## build
	##---------------------------------------------------------------
	def build(self):

		if   self.mypaf.imodule == 1: return self.buildTree()
		elif self.mypaf.imodule == 2: return self.buildDraw()
		elif self.mypaf.imodule == 3: return self.buildPlot()
		elif self.mypaf.imodule == 4: return self.buildScan()
		elif self.mypaf.imodule == 5: return self.buildStat()
		elif self.mypaf.imodule == 6: return self.buildHist()
		elif self.mypaf.imodule == 7: return self.buildPubl()
		
		return False


	## buildDraw
	##---------------------------------------------------------------
	def buildDraw(self):

		idir = self.cfg.getVar("inputdir")
		iobj = self.cfg.getVar("inputtree")

		## better treatment of the sources!!! 

		self.sources = []
		for s in self.cfg.getAll("input", "type=='tree'", "name-args"):
			name  = s[0]
			path  = self.mypaf.inputfile(idir, s[1])
			alist = args.args(s[2])
			tree  = self.mypaf.inputobject(iobj, alist.get("tree"))

			dsname = self.db.getVar("samples", s[0], "dataset")
			idx = lib.findElmAttr(self.sources, "name", dsname)
			if idx == -1:
				ds = source.source(self.mypaf, dsname)
				self.sources.append(ds)
				idx = len(self.sources)-1
			self.sources[idx].addSample(s[0], path, tree)

		self.samples = []
		for ds in self.sources:
			self.samples.extend(ds.samples)

		self.selection = [["tree", "none", ""]]
		self.selection.extend(self.cfg.getAll("selection", "type=='tree'"))
		self.output    = self.cfg.getAll("output", "(type=='file' or type=='plot')")


	## buildHist
	##---------------------------------------------------------------
	def buildHist(self):

		## collect input / output of other modules? run other modules in runHist ? 

		self.schemes = self.cfg.getAll("schemes")
		self.input   = self.cfg.getAll("input")
		self.output  = self.cfg.getAll("output")
		self.modules = []
		ignore = []

		for i, scheme in enumerate(self.schemes):
			needs     = scheme[2].strip().split()[0].strip()
			needstype = lib.getElmVar(self.output, 1, needs, 0)
			if needstype == "tree":
				self.vb.warning("scheme wants to use invaliv input. scheme not drawn.")
				ignore.append(i)
			elif needstype == "file" or needstype == "plot":
				needsdef = lib.getElmVar(self.output, 1, needs, 2)
				if needsdef[0:4] == "FILE" or needsdef[0:4] == "HIST":
					self.modules = lib.addToVectorIfMissing(self.modules, "plot")
				else:
					self.modules = lib.addToVectorIfMissing(self.modules, "draw")
			elif needstype == "evlist" or needstype == "oblist":
				self.modules = lib.addToVectorIfMissing(self.modules, "scan") 
			elif needstype == "evyields" or needstype == "obyields" or needstype == "effmap" or needstype == "roc":
				self.modules = lib.addToVectorIfMissing(self.modules, "stat") 
			## SCHEMES ALSO MAY USE OTHER SCHEMES AS INPUT!
			#else:
			#	self.vb.warning("scheme wants to use invalid input. scheme not drawn.")
			#	ignore.append(i)	

		self.modules = lib.removeFromVector(self.modules, ignore)


	## buildPlot
	##---------------------------------------------------------------
	def buildPlot(self):

		idir = self.cfg.getVar("inputdir")
		self.files  = self.cfg.getAll("input", "(type=='file' or type=='root')")

		for entry in self.files:
			entry[2] = self.mypaf.inputfile(idir, entry[2])

		self.output = self.cfg.getAll("output", "(type=='file' or type=='plot')")
		## no selection?
		self.selection = [["tree", "none", ""]]
		#self.selection.extend(self.cfg.getAll("selection", "type=='tree'"))


	## buildScan
	##---------------------------------------------------------------
	def buildScan(self):

		idir = self.cfg.getVar("inputdir")
		iobj = self.cfg.getVar("inputtree")

		## better treatment of the sources!!! 

		self.sources = []
		for s in self.cfg.getAll("input", "type=='tree'", "name-args"):
			name  = s[0]
			path  = self.mypaf.inputfile(idir, s[1])
			alist = args.args(s[2])
			tree  = self.mypaf.inputobject(iobj, alist.get("tree"))

			dsname = self.db.getVar("samples", s[0], "dataset")
			idx = lib.findElmAttr(self.sources, "name", dsname)
			if idx == -1:
				source = source.source(self.mypaf, dsname)
				self.sources.append(ds)
				idx = len(self.sources)-1
			self.sources[idx].addSample(s[0], path, tree)

		self.samples = []
		for ds in self.sources:
			self.samples.extend(ds.samples)

		self.selection = [["tree", "none", ""]]
		self.selection.extend(self.cfg.getAll("selection", "type=='tree'"))
		self.output    = self.cfg.getAll("output", "type=='plot' or type=='root'")



	## buildTree
	##---------------------------------------------------------------
	def buildTree(self):

		idir = self.cfg.getVar("inputdir")
		iobj = self.cfg.getVar("inputtree")

		## better treatment of the sources!!! 

		self.sources = []
		for s in self.cfg.getAll("input", "type=='tree'", "name-args"):
			name  = s[0]
			path  = self.mypaf.inputfile(idir, s[1])
			alist = args.args(s[2])
			tree  = self.mypaf.inputobject(iobj, alist.get("tree"))

			self.samples.append(sample.sample(self.mypaf, s[0], path, tree))

		self.evtsel = []
		self.objsel = []
		for s in self.cfg.getAll("selection", "type=='tree'"):
			alist = args.args(s[3])
			if alist.has("obj"):
				self.objsel.append(s)
			else:
				self.evtsel.append(s)

		self.output    = self.cfg.getAll("output", "type=='tree'")



