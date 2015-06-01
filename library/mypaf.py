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

import array, datetime, inspect, ROOT
import cfg, clist, dbreader, input, lib, objcoll, output, rstuff, parser, vb


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

	imodule    = -1
	module     = ""
	path       = "/Users/conni/Computing/MyPAF/"
	#path       = "/shome/cheidegg/d/MyPAF/"
	prod       = ""

	cfgpath    = path + "cfg/"
	dbpath     = path + "db/"
	inputpath  = path + "input/"
	outputpath = path + "output/"
	prodpath   = path + "output/" 
	temppath   = path + "temp/"


	## __init__
	##---------------------------------------------------------------
	def __init__(self, module, cfgfile):

		cfgfile     = cfgfile.strip()
		self.module = module.strip()
		self.setIModule()

		self.vb     = vb.vb(self, 1) 
		self.db     = dbreader.dbreader(self)
		self.input  = input.input  (self, cfgfile)
		self.cfg    = self.input.cfg

		self.newProd()
		self.createEnvironment()
		self.createOutputStruct()

		self.output = output.output(self)


	## applyGrid
	##---------------------------------------------------------------
	def applyGrid(self):

		if self.input.cfg.getVar("grid") == "y":
			for pad in self.pads:
				pad.SetGrid(1, 1)
		else:
			for pad in self.pads:
				pad.SetGrid(0, 0)


	## applyLog
	##---------------------------------------------------------------
	def applyLog(self):
		log = self.input.cfg.getVar("log")

		for pad in self.pads:
			if log.find("x") != -1:
				pad.SetLogx(1)
			else:
				pad.SetLogx(0)

			if log.find("y") != -1:
				pad.SetLogy(1)
			else:
				pad.SetLogy(0)

			if log.find("z") != -1:
				pad.SetLogz(1)
			else:
				pad.SetLogz(0)


	## close
	##---------------------------------------------------------------
	def close(self):

		lib.copyFile(self.input.cfg.path, self.prodpath)
		lib.cleanDir(self.temppath)
		self.vb.end()


	## createEnvironment
	##---------------------------------------------------------------
	def createEnvironment(self):

		for attr in dir(self):
			if attr.find("path") != -1:
				lib.makeDir(getattr(self, attr))
		

	## createOutputStruct
	##---------------------------------------------------------------
	def createOutputStruct(self):

		lib.makeDir(self.outputpath)
		lib.makeDir(self.outputpath + self.module)
		lib.makeDir(self.prodpath)


	## divideCanv
	##---------------------------------------------------------------
	def divideCanv(self, nx, ny, ratio = False):
		## divides the canvas into several pads
		## nx ... number of pads on top of each other (rows)
		## ny ... number of pads next to each other (columns)

		## the rule always is: first fill up the columns of that row, then go to the next row

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



	## resetCanv
	##---------------------------------------------------------------
	def resetCanv(self, padstring = "rstuff.pad()"):

		self.canvas.Clear()
		self.pads = None
		self.pads = [eval(s.strip()) for s in padstring.split(",")]
		self.canvas.Update()
		self.pads[0].cd()

	
	## resizeCanv
	##---------------------------------------------------------------
	def resizeCanv(self, x, y):
		self.canvas.SetWindowSize(x, y)


	## finalize
	##---------------------------------------------------------------
	def finalize(self):

 		self.output.finalize()


	## inputfile
	##---------------------------------------------------------------
	def inputfile(self, headpath, inputpath):
	        
		if inputpath != "" and inputpath[0] == "/":
			return inputpath
		else:
			if headpath != "" and headpath[0] == "/":
				return headpath.rstrip("/") + "/" + inputpath
			else:
				return self.inputpath + headpath.rstrip("/") + "/" + inputpath
		    
		return inputpath
        

	## inputobject
	##---------------------------------------------------------------
	def inputobject(self, headobject, inputobject):
	        
		if inputobject != "": 
			return inputobject
		return headobject


	## restart
	##---------------------------------------------------------------
	def restart(self, module):

		cfgfile = self.cfg.path

		self.module = module.strip()
		self.setIModule()
		self.createEnvironment()
		self.createOutputStruct()
		
		self.vb     = vb.vb(self, 1) 
		self.db     = dbreader.dbreader(self)
		
		self.input  = input.input  (self, cfgfile)
		self.output = output.output(self)
		self.cfg    = self.input.cfg


	## run
	##---------------------------------------------------------------
	def run(self):

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
	def runDraw(self):

		for i, sample in enumerate(self.input.samples):

			sample.load()
			t = sample.tree

			sidx = i
			if self.input.cfg.getVar("head", "dataset") == "y":
				sidx = lib.findElmAttr(self.input.datasets, \
				                       "name", \
				                       self.db.getColumn("samples", "name=='" + sample.name + "'", "dataset"))

			for var in self.input.output:
				for cidx, sel in enumerate(self.input.selection):

					dim  = self.output.objcoll.getHistDim(var[1])
					bins = self.output.objcoll.getHistBins(var[1])
					      
					if   dim == 2: htemp = ROOT.TH2F("htemp", "htemp", len(bins[0].list)-1, array.array('d', bins[0].list), \
					                                                   len(bins[1].list)-1, array.array('d', bins[1].list))
					elif dim == 3: htemp = ROOT.TH3F("htemp", "htemp", len(bins[0].list)-1, array.array('d', bins[0].list), \
					                                                   len(bins[1].list)-1, array.array('d', bins[1].list), \
					                                                   len(bins[2].list)-1, array.array('d', bins[2].list))
					else:          htemp = ROOT.TH1F("htemp", "htemp", len(bins[0].list)-1, array.array('d', bins[0].list))

					t.Draw(var[2] + ">>htemp", sel[2])
					#htemp.Print()
					self.output.objcoll.injectHist(var[1], htemp, sidx, cidx)
					htemp.Delete()
					del htemp

		self.output.objcoll.setInitial()


	## runHist
	##---------------------------------------------------------------
	def runHist(self):

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
	def runPlot(self):

		for var in self.input.output:
			sdefs = var[2].split()
			for sdef in sdefs:
				htemp = parser.access(self, self.input.files, 1, sdef)	
				htemp = lib.setProperBinning(htemp)
				htemp = lib.rebin(htemp, self.output.objcoll.getHistBins(var[1]))
				self.output.objcoll.injectHist(var[1], htemp)
				htemp.Delete()	
				del htemp

		self.output.objcoll.setInitial()


	## runScan
	##---------------------------------------------------------------
	def runScan(self):

		allvars = []
		for var in self.input.output:
			allvars.append(var[2])

		for i, sample in enumerate(self.input.samples):

			sample.load()
			t = sample.tree

			sidx = i
			if self.input.cfg.getVar("head", "dataset") == "y":
				sidx = lib.findElmAttr(self.input.datasets, \
				                       "name", \
				                       self.db.getColumn("samples", "name=='" + sample.name + "'", "dataset"))

				
			for cidx, sel in enumerate(self.input.selection):
				t.GetPlayer().SetScanRedirect(True)
				t.GetPlayer().SetScanFileName(self.temppath + "templist.txt")
				self.objcoll.getEvList().injectScanFile(sidx, cidx, self.temppath + "templist.txt")
				lib.rmFile(self.temppath + "templist.txt")
				self.objcoll.getEvYield().inject(sidx, cidx, int(t.GetEntries(sel[2])))


	## runStat
	##---------------------------------------------------------------
	def runStat(self):

		for i, sample in enumerate(self.input.samples):

			sample.load()
			t = sample.tree

			sidx = i
			if self.input.cfg.getVar("head", "dataset") == "y":
				sidx = lib.findElmAttr(self.input.datasets, \
				                       "name", \
				                       self.db.getColumn("samples", "name=='" + sample.name + "'", "dataset"))

			for cidx, sel in enumerate(self.input.selection):
				sels = parser.getSelSteps(sel[2])
				for selection in sels:
					self.objcoll.getEvYield().inject(sidx, cidx, int(t.GetEntries(sel[2])))
				
				nevts = int(t.GetEntries(sel[2]))


	## runTier2Modules
	##---------------------------------------------------------------
	def runTier2Modules(self, modulelist):

		for module in modulelist:
			if module == "draw":
				self.input.buildDraw()
				self.output.buildDraw()
				self.runDraw()
			elif module == "plot":
				self.input.buildPlot()
				self.output.buildPlot()
				self.runPlot()
			elif module == "scan":
				self.input.buildScan()
				self.output.buildScan()
				self.runScan()
			elif module == "stat":
				self.input.buildStat()
				self.output.buildStat()
				self.runStat()


	## runTree
	##---------------------------------------------------------------
	def runTree(self):
		## implements the tier1 module "tree"
		## event-by-event loop over tree
		## compute variables and write them to the tree
		## always writes an unskimmed tree
		## also writes a skimmed tree for every selection


		tv = tvars.tvars(self, lib.column(self.input.output, 1), lib.column(self.input.output, 2), lib.column(self.input.selection,3))

		## read tree, fill objects, apply selection and write to new tree
		for i, sample in enumerate(self.input.samples):
			sample.load()
			t = sample.tree
			tv.setOldTree(t)
			
			for j, sel in enumerate(self.input.selection):

				nt = self.output.openTree(sample.name + "_tree", sample.name + "_" + sel[1])
				tv.setNewTree(nt)

				for evt in t:

					tv.load(evt)
					tv.applySelection(j)
					tv.write()

			self.output.file.Write()		
			tv.closeTrees()	
			sample.close()

		tv.close()


	## save
	##---------------------------------------------------------------
	def save(self):

		self.output.save()


	## saveCanv
	##---------------------------------------------------------------
	def saveCanv(self, name):

		self.canvas.cd()
		self.canvas.SaveAs(self.prodpath + name + ".C")
		self.canvas.SaveAs(self.prodpath + name + ".png")
		self.canvas.SaveAs(self.prodpath + name + ".root")
		

	## setIModule
	##---------------------------------------------------------------
	def setIModule(self):

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
		
		if self.input.cfg.get("logscale") == "y": self.canvas.SetLogy(1)
		else: self.canvas.SetLogy(0)

		if setlog == True:
			self.canvas.SetLogy(1)

	
	## newProd
	##---------------------------------------------------------------
	def newProd(self):

		## normal mode
		self.prod     = lib.getTimeStamp()

		## test mode
		if self.input.cfg.getVar("mode") == "test":
			self.prod = "test"
			lib.cleanDir(self.outputpath + self.module + "/" + self.prod)

		self.prodpath = self.outputpath + self.module + "/" + self.prod + "/"


