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

import array, copy, datetime, inspect, ROOT, os
import args, cfg, clist, dbreader, input, lib, objcoll, output, parser, rstuff, sample, sel, vb
from PIL import PngImagePlugin


## mypaf
##------------------------------------------------------------------- 
class mypaf:

	cfg        = None
	db         = None
	input      = None
	output     = None
	vb         = None

	canvas     = rstuff.canv()
	pads       = [rstuff.pad()]
	canvas.Update()
	pads[0].cd()

	imodule       = -1
	module        = ""
	#path          = "/Users/conni/Computing/MyPAF/"
	path          = "/shome/cheidegg/p/MyPAF/"
	www           = "/afs/cern.ch/user/c/cheidegg/www/MyPAF/"
	url           = "https://cheidegg.web.cern.ch/cheidegg/MyPAF/"
	prod          = ""

	cfgpath       = path + "cfg/"
	dbpath        = path + "db/"
	inputpath     = path + "input/"
	outputpath    = path + "output/"
	prodpath      = path + "output/" 
	temppath      = path + "temp/"
	templatepath  = path + "templates/"
	templateindex = templatepath + "index.php"


	## __init__
	##---------------------------------------------------------------
	def __init__(self, module, cfgfile, title = ""):

		self.vb     = vb.vb(self, 2) 
		self.createEnvironment()

		self.title  = title.strip().lower()
		self.setModule(module)

		self.db     = dbreader.dbreader(self)
		self.input  = input.input(self, cfgfile.strip())
		self.cfg    = self.input.cfg
		self.vb.setVB(int(lib.useVal("1", self.cfg.getVar("verbosity"))))
		self.vb.call("mypaf", "__init__", [self, module, cfgfile, title], "Initializing mypaf class.")

		self.newProd()
		self.createOutputStruct()
		self.vb.move()

		self.output = output.output(self)


	## close
	##---------------------------------------------------------------
	def close(self):

		self.vb.call("mypaf", "close", [self], "Finalizing production output.")
		lib.groupFileExtensions(self.prodpath)
		lib.cpFileAllSubDirs(self.templateindex, self.prodpath, ["png"])
		lib.cpFile(self.input.cfg.path, self.prodpathmypaf)
		for dbfpath in lib.getAllFiles(self.dbpath):
			lib.cpFile(dbfpath, self.prodpathmypaf)

		lib.writeFile(self.prodpathmypaf + "note.txt", "\n".join(self.prodInfo()))
		self.zip()
		lib.cleanDir(self.temppath)
		self.vb.end()
		self.syncWWW()


	## createEnvironment
	##---------------------------------------------------------------
	def createEnvironment(self):

		self.vb.call("mypaf", "createEnvironment", [self], "Creating directory environment.")

		for attr in dir(self):
			if attr.find("path") != -1:
				lib.mkDir(getattr(self, attr))
		

	## createOutputStruct
	##---------------------------------------------------------------
	def createOutputStruct(self):

		self.vb.call("mypaf", "createOutputStruct", [self], "Creating output directory structure.")

		lib.mkDir(self.outputpath)
		lib.mkDir(self.outputpath + self.module)
		lib.mkDir(self.prodpath)
		lib.mkDir(self.prodpathmypaf)

		lib.mkDir(self.www)
		lib.mkDir(self.www + self.module)

		#alltypes = []
		#for iobj in self.input.cfg.getObjs("region=='output'"):
		#	alltypes = lib.addToVectorIfMissing(alltypes, iobj.type)

		#for type in alltypes:
		#	lib.mkDir(self.prodpath + lib.getOutputDirPerType(type))		


	## divideCanv
	##---------------------------------------------------------------
	def divideCanv(self, nx, ny, ratio = False):
		## divides the canvas into several pads
		## nx ... number of pads on top of each other (rows)
		## ny ... number of pads next to each other (columns)

		## the rule always is: first fill up the columns of that row, then go to the next row

		self.vb.call("mypaf", "divideCanv", [self, nx, ny, ratio], "Dividing canvas in a number of pads.")

		## 975 x 600
		if nx == 1 and ny == 1:
			if ratio:
				self.resetCanv("rstuff.plotpad(), rstuff.ratiopad()")
			else:
				self.resetCanv()

		x1coord = []
		y1coord = []

		## 975 x 1200
		if nx == 2 and ny == 1: 
			self.resizeCanv(975, 1200)
			if ratio:
				self.resetCanv("rstuff.plotpad(0.0, 0.65, 1.0, 1.0), rstuff.ratiopad(0.0, 0.5, 1.0, 0.65), rstuff.plotpad(0.0, 0.15, 1.0, 0.5), rstuff.ratiopad(0.0, 0.0, 1.0, 0.15)")
			else:
				self.resetCanv("rstuff.pad(0.0, 0.5, 1.0, 1.0), rstuff.pad(0.0, 0.0, 1.0, 0.5)")

		## 1950 x 600
		elif nx == 1 and ny == 2:
			self.resizeCanv(975, 1200)
			if ratio:
				self.resetCanv("rstuff.plotpad(0.0, 0.3, 0.5, 1.0), rstuff.ratiopad(0.0, 0.0, 0.5, 0.3), rstuff.plotpad(0.5, 0.3, 1.0, 1.0), rstuff.ratiopad(0.5, 0.0, 1.0, 0.3)")
			else:
				self.resetCanv("rstuff.pad(0.0, 0.0, 0.5, 1.0), rstuff.pad(0.5, 0.0, 1.0, 1.0)")

		## 1950 x 1200
		elif nx == 2 and ny == 2:
			self.resizeCanv(975, 1200)
			if ratio:
				self.resetCanv("rstuff.plotpad(0.0, 0.65, 0.5, 1.0), rstuff.ratiopad(0.0, 0.5, 0.5, 0.65), rstuff.plotpad(0.5, 0.65, 1.0, 1.0), rstuff.ratiopad(0.5, 0.5, 1.0, 0.65), rstuff.plotpad(0.0, 0.15, 0.5, 0.5), rstuff.ratiopad(0.0, 0.0, 0.5, 0.15), rstuff.plotpad(0.5, 0.15, 1.0, 0.5), rstuff.ratiopad(0.5, 0.0, 1.0, 0.15)")
			else:
				self.resetCanv("rstuff.pad(0.0, 0.5, 0.5, 1.0), rstuff.pad(0.5, 0.5, 1.0, 1.0), rstuff.pad(0.0, 0.0, 0.5, 0.5), rstuff.pad(0.5, 0.0, 1.0, 0.5)")


	## finalize
	##---------------------------------------------------------------
	def finalize(self):

		self.vb.call("mypaf", "finalize", [self], "Finalizing outputs before closing.")
 		self.output.finalize()


	## findSelections
	##---------------------------------------------------------------
	def findSelections(self, types, alist):

		self.vb.call("mypaf", "findSelections", [self, types, alist], "Getting a list of cfgobj for the selections according to the given types.")
		tr = " or ".join(["type=='" + t + "'" for t in types])
		if alist.has("sel"):
			sels = alist.get("sel").split(",")
			add = " or ".join(["name=='" + n + "'" for n in sels])
			return self.input.cfg.getObjs("region=='selection' and (type=='none' or " + tr + ") and (" + add + ")")
		return self.input.cfg.getObjs("region=='selection' and (type=='none' or " + tr + ")")


	## normalizeHistLumi
	##---------------------------------------------------------------
	def normalizeHistLumi(self, hist, samplename, alist):

		norm =       lib.useVal("none", self.input.cfg.getVar("norm")      , alist.get("norm"))
		lumi = float(lib.useVal("0"   , self.input.cfg.getVar("luminosity"), alist.get("luminosity")))

		if norm       != "lumi": return hist
		if samplename == ""    : return hist
		if lumi       == 0.    : return hist
		 
		sam    = self.db.getRow("samples", "name == '" + samplename + "'")
		sou    = self.db.getRow("sources", "name == '" + samplename + "'")
		dstype = sou[3]
		xsec   = float(eval(sam[4]))
		nevt   = float(eval(sam[6]))
		
		if dstype == "d" or xsec == 0: return hist
	
		return lib.normalizeHistLumi(hist, lumi, xsec, nevt)	


	## prodInfo
	##---------------------------------------------------------------
	def prodInfo(self):

		self.vb.call("mypaf", "prodInfo", [self], "Assembling a list of information for this production.")
		info = []
		info.append("prod timestamp: " + self.prod) 
		info.append("MyPAF version: "  + lib.bash("git describe --abbrev=4 --dirty --always"))

		if self.input.cfg.getVar("prodtitle")   != "":	 
			info.append("prod title: "       + self.input.cfg.getVar("prodtitle"))
		if self.input.cfg.getVar("description") != "":
			info.append("prod description: " + self.input.cfg.getVar("description"))

		return info


	## resetCanv
	##---------------------------------------------------------------
	def resetCanv(self, padstring = "rstuff.pad()"):

		self.vb.call("mypaf", "resetCanv", [self, padstring], "Resetting the canvas to a single pad.")
		self.canvas.Clear()
		self.pads = None
		self.pads = [eval(s.strip()) for s in padstring.split(",")]
		self.canvas.Update()
		self.pads[0].cd()

	
	## resizeCanv
	##---------------------------------------------------------------
	def resizeCanv(self, x, y):
		self.vb.call("mypaf", "resizeCanv", [self, x, y], "Resizing canvas.")
		self.canvas.SetWindowSize(x, y)


	## restart
	##---------------------------------------------------------------
	def restart(self, module):

		self.vb.call("mypaf", "restart", [self, module], "Re-initializing mypaf instance.")
		self.createEnvironment()
		cfgfile = self.cfg.path

		self.setModule(module)
		self.createOutputStruct()
		
		self.vb     = vb.vb(self, 1) 
		self.vb.move()
		self.db     = dbreader.dbreader(self)
		
		self.input  = input.input  (self, cfgfile)
		self.output = output.output(self)
		self.cfg    = self.input.cfg


	## run
	##---------------------------------------------------------------
	def run(self):

		self.vb.modulerun()
		self.vb.call("mypaf", "run", [self], "Running the module.")
		#eval("return self.run" + self.module.title())

		if   self.imodule == 1: return self.runTree()
		elif self.imodule == 2: return self.runDraw()
		elif self.imodule == 3: return self.runPlot()
		elif self.imodule == 4: return self.runScan()
		elif self.imodule == 5: return self.runStat()
		elif self.imodule == 6: return self.runHist()
		elif self.imodule == 7: return self.runPubl()

		return False


	## runDraw
	##---------------------------------------------------------------
	def runDraw(self, objnames = []):

		self.vb.call("mypaf", "runDraw", [self, objnames], "Running the draw module.")
		objlist = self.input.cfg.getObjs("region=='output' and (type=='file' or type=='plot')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)

		##loop over samples
		for i, sam in enumerate(self.input.cfg.getObjs("region=='input' and type=='tree'")):

			alist = args.args(sam.argstring)
			#samp  = sample.sample(self, sam.name, \
			#                            lib.usePath(self.inputpath, self.input.cfg.getVar("inputdir"), sam.definition, alist.get("dir")), \
			#                            lib.useVal("tree", self.input.cfg.getVar("inputtree"), alist.get("tree")))
			samp  = sample.sample(self, sam.name, \
			                            sam.definition, \
			                            lib.useVal("tree", self.input.cfg.getVar("inputtree"), alist.get("tree")), \
			                            alist.get("dir"))
			samp.load()
			t    = samp.tree
			sidx = sam.source

			## loop over variables to plot
			for j, var in enumerate(objlist):

				valist = args.args(var.argstring)
				lumi = float(lib.useVal("0", self.input.cfg.getVar("luminosity"), valist.get("luminosity"))) 

				## loop over selection
				allselobj = self.findSelections(["tree"], valist)
				allselstr = [[s.name, s.definition] for s in self.input.cfg.getObjs("region=='selection' and (type=='none' or type=='tree')")]
				for cidx, csel in enumerate(allselobj):

					vdef = var.definition.split("::")
					ssel = sel.sel(csel.definition, allselstr)

					dim  = self.output.objcoll.getHistDim (var.name)
					bins = self.output.objcoll.getHistBins(var.name)

					if   dim == 2 and valist.get("profile") == "y": 
					               htemp = ROOT.TProfile2D("htemp", "htemp", len(bins[0].list)-1, array.array('d', bins[0].list), \
					                                                   len(bins[1].list)-1, array.array('d', bins[1].list))
					elif dim == 2: htemp = ROOT.TH2F("htemp", "htemp", len(bins[0].list)-1, array.array('d', bins[0].list), \
					                                                   len(bins[1].list)-1, array.array('d', bins[1].list))
					elif dim == 3: htemp = ROOT.TH3F("htemp", "htemp", len(bins[0].list)-1, array.array('d', bins[0].list), \
					                                                   len(bins[1].list)-1, array.array('d', bins[1].list), \
					                                                   len(bins[2].list)-1, array.array('d', bins[2].list))
					else:          htemp = ROOT.TH1F("htemp", "htemp", len(bins[0].list)-1, array.array('d', bins[0].list))

					if len(vdef) == 2 and valist.get("profile") == "y": 
					                     num = t.Draw(vdef[1] + ":" + vdef[0] + ">>htemp",          ssel.string) ## averaging over the weight
					elif len(vdef) == 2: num = t.Draw(vdef[0] +                 ">>htemp", vdef[1], ssel.string) ## weight given
					else               : num = t.Draw(vdef[0] +                 ">>htemp",          ssel.string) ## weight set to 1

					## underflow bin
					if dim == 1 and valist.get("ufb").find("x") != -1:
						ssel.addAnd(vdef[0] + "<" + str(bins[0].list[0]))
						htemp2 = copy.deepcopy(htemp) ##CH: totally ugly but t.Draw will overwrite htemp :-(
						if len(vdef) == 2: ufb = t.Draw(vdef[0], vdef[1], ssel.string)
						else             : ufb = t.Draw(vdef[0],          ssel.string)
						htemp = htemp2
						del htemp2
						htemp.SetBinContent(1, htemp.GetBinContent(1) + ufb)

					## overflow bin
					if dim == 1 and valist.get("ofb").find("x") != -1:
						ssel.addAnd(vdef[0] + ">" + str(bins[0].list[-1]))
						htemp2 = copy.deepcopy(htemp) ##CH: totally ugly but t.Draw will overwrite htemp :-(
						if len(vdef) == 2: ofb = t.Draw(vdef[0], vdef[1], ssel.string)
						else             : ofb = t.Draw(vdef[0],          ssel.string)
						htemp = htemp2
						del htemp2
						htemp.SetBinContent(len(bins[0].list)-1, htemp.GetBinContent(len(bins[0].list)-1) + ofb)

					self.vb.talk("Drawing " + str(num) + " entries into " + var.name + ".", 1)
					#if valist.get("profile") != "y":
					#	htemp.Scale(self.findScale(alist))
					htemp = self.normalizeHistLumi(htemp, sam.name, valist) 
					self.output.objcoll.injectHist(var.name, htemp, sidx, cidx)

					htemp.Delete()	
					del htemp
			samp.close()

		self.output.objcoll.setNormalizedLumi()
		self.output.objcoll.setInitial()


	## runHist
	##---------------------------------------------------------------
	def runHist(self):

		self.vb.call("mypaf", "runHist", [self], "Running the hist module.")
		self.output.buildHist()
		self.output.openFile()

		for i, scheme in enumerate(self.output.schemes):
			if not scheme.isTrivial():
				scheme.setSchemes(self.output.schemes)
				scheme.build()
				if scheme.isPrimary():
					scheme.getHist().setInitial()
	
		self.output.save()


	## runPlot
	##---------------------------------------------------------------
	def runPlot(self, objnames = []):

		self.vb.call("mypaf", "runPlot", [self, objnames], "Running the plot module.")
		objlist = self.input.cfg.getObjs("region=='output' and (type=='file' or type=='plot')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)
	
		for j, var in enumerate(objlist):
			alist = args.args(var.argstring)
			for sdef in var.definition.split():
				htemp = parser.access(self, self.input.cfg.getObjs("region=='input' and (type=='file' or type=='root')"), sdef, alist.get("dir"))
				htemp = self.normalizeHistLumi(htemp, sdef.split("::")[2], alist)
				htemp = lib.setProperBinning(htemp)
				htemp = lib.rebin(htemp, self.output.objcoll.getHistBins(var.name))
				self.output.objcoll.injectHist(var.name, htemp)
				htemp.Delete()	
				del htemp, valist

		self.output.objcoll.setNormalizedLumi()
		self.output.objcoll.setInitial()


	## runScan
	##---------------------------------------------------------------
	def runScan(self, objnames = []):

		self.vb.call("mypaf", "runScan", [self, objnames], "Running the scan module.")
		tvrun  = lib.useVal("run" , self.input.cfg.getVar("treevarrun" ))
		tvlumi = lib.useVal("lumi", self.input.cfg.getVar("treevarlumi"))
		tvevt  = lib.useVal("evt" , self.input.cfg.getVar("treevarevt" ))

		objlist = self.input.cfg.getObjs("region=='output' and (type=='evlist' or type=='oblist')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)

		for i, sam in enumerate(self.input.cfg.getObjs("region=='input' and type=='tree'")):

			alist = args.args(sam.argstring)
			samp  = sample.sample(self, sam.name, \
			                            sam.definition, \
			                            lib.useVal("tree", self.input.cfg.getVar("inputtree"), alist.get("tree")), \
			                            alist.get("dir"))
			samp.load()
			t    = samp.tree
			sidx = sam.source

			t.GetPlayer().SetScanRedirect(True)
			t.GetPlayer().SetScanFileName(self.temppath + "templist.txt")

			for j, var in enumerate(objlist):
				valist = args.args(var.argstring)

				for cidx, sel in enumerate(self.findSelections(["tree"], valist)):
					num = t.Scan(tvrun + ":" + tvlumi + ":" + tvevt + ":" + var.definition, sel.definition) 
					if   var.type == "evlist":
						self.output.objcoll.getEvList (var.name).injectScanFile(sidx, cidx, self.temppath + "templist.txt")
						self.output.objcoll.getEvYield(var.name).inject(sidx, cidx, int(num))
					elif var.type == "oblist":
						self.output.objcoll.getObList (var.name).injectScanFile(sidx, cidx, self.temppath + "templist.txt")
						self.output.objcoll.getObYield(var.name).inject(sidx, cidx, int(num))
					lib.rmFile(self.temppath + "templist.txt")
			samp.close()

		self.output.objcoll.setInitial()



	## runStat
	##---------------------------------------------------------------
	def runStat(self, objnames = []):

		self.vb.call("mypaf", "runStat", [self, objnames], "Running the stat module.")
		objlist = self.input.cfg.getObjs("region=='output' and (type=='evyield' or type=='obyield' or type=='effmap')")
		if len(objnames) > 0:
			objlist = lib.getElmAttrAllOr(objlist, "name", objnames)
		allselstr = [[s.name, s.definition] for s in self.input.cfg.getObjs("region=='selection' and (type=='none' or type=='tree')")]

		for i, sam in enumerate(self.input.cfg.getObjs("region=='input' and type=='tree'")):

			alist = args.args(sam.argstring)
			#samp  = sample.sample(self, sam.name, \
			#                            lib.usePath(self.inputpath, self.input.cfg.getVar("inputdir"), sam.definition, alist.get("dir")), \
			#                            lib.useVal("tree", self.input.cfg.getVar("inputtree"), alist.get("tree"))) 
			samp  = sample.sample(self, sam.name, \
			                            sam.definition, \
			                            lib.useVal("tree", self.input.cfg.getVar("inputtree"), alist.get("tree")), \
			                            alist.get("dir"))
			samp.load()
			t    = samp.tree
			sidx = sam.source

			for j, var in enumerate(objlist):
				valist = args.args(var.argstring)
				for cidx, csel in enumerate(self.findSelections(["tree"], valist)):
					ssel = sel.sel(csel.definition, allselstr)

					if   var.type == "evyield":
						self.output.objcoll.getEvYield(var.name).inject(sidx, cidx, int(t.GetEntries(ssel.string)))
					elif var.type == "obyield":
						self.output.objcoll.getObYield(var.name).inject(sidx, cidx, int(t.GetEntries(ssel.string)))
					elif var.type == "effmap":
						selsteps = lib.buildSelSteps(ssel.string, (valist.get("ind") == "y"))
						self.output.objcoll.getEffMap(var.name).inject(sidx, cidx, [int(t.GetEntries(ss)) for ss in selsteps])
					#elif var.type == "roc":

			samp.close()

		self.output.objcoll.setInitial()



	## runTier2Modules
	##---------------------------------------------------------------
	def runTier2Modules(self, modulelist, objlist = []):

		self.vb.call("mypaf", "runTier2Modules", [self, modulelist, objlist], "Running the modules of tier2.")
		for module in modulelist:
			if module == "draw":
				self.output.buildDraw(objlist)
				self.runDraw(objlist)
			elif module == "plot":
				self.output.buildPlot(objlist)
				self.runPlot(objlist)
			elif module == "scan":
				self.output.buildScan(objlist)
				self.runScan(objlist)
			elif module == "stat":
				self.output.buildStat(objlist)
				self.runStat(objlist)


	## runTree
	##---------------------------------------------------------------
	def runTree(self, direct = False):
		## implements the tier1 module "tree"
		## event-by-event loop over tree
		## compute variables and write them to the tree
		## always writes an unskimmed tree
		## also writes a skimmed tree for every selection

		self.vb.call("mypaf", "runTree", [self, direct], "Running the tree module.")



		## ATTENTION: need to only loop over EVENT SELECTIONS, and pass the object selections to the tvars instance!

		tv = tvars.tvars(self, self.input.cfg.getObjs("region=='output' and type=='tree'"))

		for i, sam in enumerate(self.input.cfg.getObjs("region=='input' and type=='tree'")):

			alist = args.args(sam.argstring)
			sample = sample.sample(self, sam.name, \
			                             lib.usePath(self.inputpath, self.input.cfg.getVar("inputdir"), sam.definition, alist.get("dir")), \
			                             lib.useVal("tree", self.input.cfg.getVar("inputtree"), alist.get("tree"))) 
			sample.load()
			t    = sample.tree
			tv.setOldTree(t)

			for cidx, sel in enumerate(self.input.cfg.getObjs("region=='selection' and (type=='none' or type=='tree')")):

				nt = self.output.openTree(sample.name + "_tree", sample.name + "_" + sel.name)
				tv.setNewTree(nt)

				for evt in t:

					tv.load(evt)
					tv.applySelection(sel.definition)
					tv.write()

			self.output.file.Write()		
			tv.closeTrees()	
			sample.close()

		tv.close()



		#tv = tvars.tvars(self, lib.column(self.input.output, 1), lib.column(self.input.output, 2), lib.column(self.input.selection,3))

		### read tree, fill objects, apply selection and write to new tree
		#for i, sample in enumerate(self.input.samples):
		#	sample.load()
		#	t = sample.tree
		#	tv.setOldTree(t)
		#	
		#	for j, sel in enumerate(self.input.selection):

		#		nt = self.output.openTree(sample.name + "_tree", sample.name + "_" + sel[1])
		#		tv.setNewTree(nt)

		#		for evt in t:

		#			tv.load(evt)
		#			tv.applySelection(j)
		#			tv.write()

		#	self.output.file.Write()		
		#	tv.closeTrees()	
		#	sample.close()

		#tv.close()



	## save
	##---------------------------------------------------------------
	def save(self):

		self.vb.call("mypaf", "save", [self], "Saving the not yet saved outputs.")
		self.output.save()


	## saveCanv
	##---------------------------------------------------------------
	def saveCanv(self, name):

		self.vb.call("mypaf", "saveCanv", [self, name], "Saving the current histogram in the canvas.")
		self.canvas.cd()
		self.canvas.SaveAs(self.prodpath + name + ".C")
		self.canvas.SaveAs(self.prodpath + name + ".png")
		self.canvas.SaveAs(self.prodpath + name + ".root")

		self.setMetaData()
		lib.writeMetaData(self.prodpath + name + ".png", self.meta)


	## setGlobalStyle
	##---------------------------------------------------------------
	def setGlobalStyle(self, arglog = "", arggrid = "", argdigits = ""):

		log    = lib.useVal("" , self.input.cfg.getVar("log")   , arglog   )
		grid   = lib.useVal("n", self.input.cfg.getVar("grid")  , arggrid  )
		digits = lib.useVal("3", self.input.cfg.getVar("digits"), argdigits)

		for pad in self.pads:
			pad.SetLogx(0)
			pad.SetLogy(0)
			pad.SetLogz(0)
			pad.SetGrid(0,0)

		if log.find("x") != -1:
			for pad in self.pads:
				pad.SetLogx(1)
		if log.find("y") != -1:
			for pad in self.pads:
				pad.SetLogy(1)
		if log.find("z") != -1:
			for pad in self.pads:
				pad.SetLogz(1)
		if grid == "y":
			for pad in self.pads:
				pad.SetGrid(1,1)

		for pad in self.pads:
			pad.Modified()
			pad.Update()

		ROOT.TGaxis.SetMaxDigits(int(digits))
	

	## setIModule
	##---------------------------------------------------------------
	def setIModule(self):

		self.vb.call("mypaf", "setIModule", [self], "Setting the imodule.")
		if   self.module == "tree": self.imodule = 1
		elif self.module == "draw": self.imodule = 2
		elif self.module == "plot": self.imodule = 3
		elif self.module == "scan": self.imodule = 4
		elif self.module == "stat": self.imodule = 5
		elif self.module == "hist": self.imodule = 6
		elif self.module == "publ": self.imodule = 7


	## setLogCanv
	##---------------------------------------------------------------
	def setLogCanv(self, setlog):
		
		self.vb.call("mypaf", "setLogCanv", [self, setlog], "Setting log scale to the canvas.")
		if self.input.cfg.get("logscale") == "y": self.canvas.SetLogy(1)
		else: self.canvas.SetLogy(0)

		if setlog == True:
			self.canvas.SetLogy(1)


	## setMetaData
	##---------------------------------------------------------------
	def setMetaData(self):

		if hasattr(self, "meta"): return
		self.meta = PngImagePlugin.PngInfo()
		for line in self.prodInfo():
			l = line.split(":")
			self.meta.add_text(l[0].strip(), l[1].strip(), 0)


	## setModule
	##---------------------------------------------------------------
	def setModule(self, module):

		self.vb.call("mypaf", "setModule", [self, module], "Setting the module.")
		module = module.strip().lower()
		if not module in ["tree", "draw", "plot", "scan", "stat", "hist", "publ"]:
			self.error("Cannot initialize module.")

		self.module = module
		self.setIModule()

	
	## newProd
	##---------------------------------------------------------------
	def newProd(self):

		## normal mode
		self.prod     = lib.getTimeStamp()

		if self.title != "":
			self.prod += "_" + self.title

		## test mode
		if self.input.cfg.getVar("mode") == "test":
			self.prod = "test"
			lib.cleanDir(self.outputpath + self.module + "/" + self.prod)
			#lib.rmFile(self.outputpath + self.module + "/" + self.prod + ".zip")

		self.vb.call("mypaf", "newProd", [self], "Reserving a new production, " + self.prod + ".")

		self.prodpath = self.outputpath + self.module + "/" + self.prod + "/"
		self.prodpathmypaf = self.prodpath + "mypaf/"


	## syncWWW
	##---------------------------------------------------------------
	def syncWWW(self):

		self.vb.call("mypaf", "syncWWW", [self], "Synchronizing output directories on WWW space.")

		if self.cfg.getVar("syncwww") != "y": return

		self.vb.talk("Uploading production " + self.prod + " to " + self.url + self.module + ".")

		if hasattr(self, "www"):
			if not os.path.isdir(self.www + self.module + "/" + self.prod):
				lib.cpDir(self.prod, self.prodpath[0:len(self.prodpath)-len(self.prod)-1], self.www + self.module)


	## zip
	##---------------------------------------------------------------
	def zip(self):

		if self.cfg.getVar("zip") != "y": return

		self.vb.call("mypaf", "zip", [self], "Compressing the production directory.")
		lib.cmd("zip -j -r " + self.prodpath + self.prod.rstrip("/") + ".zip " + self.prodpath)
		#lib.cmd("tar f " + self.prodpath + self.prod.rstrip("/") + ".tar.gz -C " + self.outputpath + self.module + " " + self.prodpath)		



