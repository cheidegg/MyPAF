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

import array, copy, ROOT
import args, clist, lib, hstyle, rstuff, schemes, source, styleargs


## hist
##------------------------------------------------------------------- 
class hist:



	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, name, dim = 1, argstring = ""):

		self.name    = name
		self.dim     = dim
		self.p       = False
		self.built   = False

		self.alist   = args.args(argstring)
		self.salist  = styleargs.styleargs(self.alist.get("style"), "1", lib.useVal("ROOT.kBlack", self.alist.get("color")))
		self.mypaf   = mypaf
		self.db      = mypaf.db
		self.vb      = mypaf.vb
		self.vb.call("hist", "__init__", [self, mypaf, name, dim, argstring], "Initializing the hist class.")

		self.setBinArgs()
		self.setParent()
		self.setLabels()


	## addHist
	##---------------------------------------------------------------
	def addHist(self, hist, coeffs = []):
		self.vb.call("hist", "addHist", [self, hist, coeffs], "Adding a hist to this instance.")
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = 1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Add(hist.getH(sidx, cidx), coeff)


	## build
	##---------------------------------------------------------------
	def build(self, setsources, setcategs):
		self.vb.call("hist", "build", [self], "Building the histograms.")

		self.sources = [source.source(self.mypaf, s) for s in setsources]
		self.categs  = setcategs
		self.h       = []

		for s in self.sources:
			appender = []
			for c in self.categs:
				hc = copy.deepcopy(self.parent)
				#hc = rstuff.copyTH1(self.parent)
				hc.SetName(s.name + ":=" + c + ":=" + self.name)
				appender.append(hc)

			self.h.append(appender)

		self.built = True	
		self.normalized = [[False for cidx in range(len(self.categs))] for sidx in range(len(self.sources))]
		self.drawn      = [[False for cidx in range(len(self.categs))] for sidx in range(len(self.sources))]
	

	## check
	##---------------------------------------------------------------
	def check(self, dim):
		self.vb.call("hist", "check", [self], "Performing basic dimension checks.")

		if not hasattr(self, "dim"): 
			self.dim = dim
		else: 
			if self.dim != dim: 
				self.vb.error("Trying to re-initialize a histogram of wrong dimension.")


	## divHist
	##---------------------------------------------------------------
	def divHist(self, hist, coeffs = [], error = ''):
		self.vb.call("hist", "divHist", [self, hist, coeffs, error], "Dividing this hist instance by another hist.")
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = 1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Divide(self.h[sidx][cidx], hist.getH(sidx, cidx), 1.0, coeff, error)


	## draw
	##---------------------------------------------------------------
	def draw(self, option = "", pad = 0, plot = True, save = True):

		self.vb.call("hist", "drawing", [self, option, pad, plot, save], "Drawing the histograms in this instance.")
		if option != "": option = " " + option

		self.runPreDraw(pad)

		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				self.drawH(sidx, cidx, pad, option, plot, save)

		self.mypaf.setGlobalStyle()


	## drawArrow
	##---------------------------------------------------------------
	def drawArrow(self):
		## takes all drawarrow arguments and draws an arrows to the histogram
		## for all of them
		## format of drawlatex argument is x1,y1,x2,y2,strength,color

		self.vb.call("hist", "drawArrow", [self], "Drawing an arrow.")
		arrows = lib.useArr([""], self.mypaf.input.cfg.getVars("drawarrow"), self.salist.getAll("drawarrow"), self.alist.getAll("drawarrow")) 

		if arrows != [""]:
			li = [l.split(",") for l in arrows]
			ln = []
			for ii, l in enumerate(li):
				ln.append(rstuff.arrow(int(lib.useVal("2", l[4])), int(lib.useVal("7", l[5])), eval(lib.useVal(str(ROOT.kBlack), l[6]))))
				ln[ii].DrawArrow(float(l[0]) * self.parent.GetXaxis().GetXmin(), \
				                 float(l[1]) * self.parent.GetYaxis().GetXmin(), \
				                 float(l[2]) * self.parent.GetXaxis().GetXmax(), \
				                 float(l[3]) * self.parent.GetYaxis().GetXmax())

	
	## drawBox
	##---------------------------------------------------------------
	def drawBox(self):

		self.vb.call("hist", "drawBox", [self], "Drawing a box.")
		boxes = lib.useArr([""], self.mypaf.input.cfg.getVars("drawbox"), self.salist.getAll("drawbox"), self.alist.getAll("drawbox")) 

		if boxes != [""]:
			print "draw a box"


	## drawCircle
	##---------------------------------------------------------------
	def drawCircle(self):
	
		self.vb.call("hist", "drawCircle", [self], "Drawing a circle.")
		circles = lib.useArr([""], self.mypaf.input.cfg.getVars("drawcircle"), self.salist.getAll("drawcircle"), self.alist.getAll("drawcircle")) 

		if circles != [""]:

			li = [l.split(",") for l in self.alist.getAll("drawcircle")]
			ci = []



	## drawErrorBand
	##---------------------------------------------------------------
	def drawErrorBand(self, sidx, cidx):

		self.vb.call("hist", "drawErrorBand", [self, sidx, cidx], "Drawing error bands.")
		errors = lib.useVal("none", self.mypaf.input.cfg.getVar("errors"), self.salist.get("errors"), self.alist.get("errors"))

		if errors == "band":
			hband = copy.deepcopy(self.h[sidx][cidx])
			#hband = rstuff.copyTH1(self.h[sidx][cidx])
			hband.SetFillColor(ROOT.kGray)
			hband.SetFillStyle(3001)
			hband.SetLineColor(ROOT.kGray)
			#hband.Draw("e2 same")


	## drawH
	##---------------------------------------------------------------
	def drawH(self, sidx, cidx, pad = 0, option = "", plot = True, save = True):

		self.vb.call("hist", "drawH", [self, sidx, cidx, pad, option, plot, save], "Drawing a histogram from this instance.")

		if self.drawn[sidx][cidx] == True: return

		self.vb.talk("Drawing histogram " + self.name + " with " + str(self.h[sidx][cidx].GetEntries()) + " entries for source " + self.sources[sidx].name + " and category " + self.categs[cidx] + ".", 1)

		self.mypaf.pads[pad].cd()
		self.h[sidx][cidx].Draw(self.d + " " + option)
		ROOT.gPad.Update()
		if save:
			self.saveHist(sidx, cidx)
		self.runPostDraw(sidx, cidx, option)
		if self.p and plot:
			self.mypaf.saveCanv(self.name + "_" + self.sources[sidx].name + "_" + self.categs[cidx])
		self.drawn[sidx][cidx] = True


	## drawLatex
	##---------------------------------------------------------------
	def drawLatex(self):
		## takes all drawlatex arguments and draws a text to the histogram
		## for all of them
		## format of drawlatex argument is x,y,align,textfont,textsize,textcolor,text(_)

		self.vb.call("hist", "drawLatex", [self], "Drawing latex objects.")
		latexes = lib.useArr([""], self.mypaf.input.cfg.getVars("drawlatex"), self.salist.getAll("drawlatex"), self.alist.getAll("drawlatex")) 

		if latexes != [""]:

			li = [l.split(",") for l in latexes]
			lx = []

			for ii, l in enumerate(li):
				lx.append(ROOT.TLatex())
				lx[ii].SetTextAlign(int(l[2])) 
				lx[ii].SetTextFont (int(l[3]))
				lx[ii].SetTextSize (int(l[4]))
				lx[ii].SetTextColor(int(l[5]))
				lx[ii].DrawLatex(float(l[0]), float(l[1]), l[6].replace("_", " "))


	## drawLine
	##---------------------------------------------------------------
	def drawLine(self):

		self.vb.call("hist", "drawLine", [self], "Drawing lines.")
		lines = lib.useArr([""], self.mypaf.input.cfg.getVars("drawline"), self.salist.getAll("drawline"), self.alist.getAll("drawline")) 

		if lines != [""]:
			li = [l.split(",") for l in lines]
			ln = []
			for ii, l in enumerate(li):
				ln.append(rstuff.line(int(lib.useVal("2", l[4])), int(lib.useVal("7", l[5])), eval(lib.useVal(str(ROOT.kBlack), l[6]))))
				ln[ii].DrawLine(float(l[0]) * self.parent.GetXaxis().GetXmin(), \
				                float(l[1]) * self.parent.GetYaxis().GetXmin(), \
				                float(l[2]) * self.parent.GetXaxis().GetXmax(), \
				                float(l[3]) * self.parent.GetYaxis().GetXmax())
		

	## drawNote
	##---------------------------------------------------------------
	def drawNote(self):

		self.vb.call("hist", "drawNote", [self], "Drawing lumi or CMS notes.")
		note = lib.useVal("", self.mypaf.input.cfg.getVar("note"), self.salist.get("note"), self.alist.get("note")) 

		if note == "cms":
			mcOnly = True
			rstuff.cms(self.mypaf.canvas, float(self.mypaf.input.cfg.getVar("luminosity")), float(self.mypaf.input.cfg.getVar("energy")), mcOnly)


	## drawSingle
	##---------------------------------------------------------------
	def drawSingle(self, sidx, cidx, pad, option = "", plot = True, save = True):

		self.runPreDraw(pad)
		self.drawH(sidx, cidx, pad, option, plot, save)
		self.mypaf.setGlobalStyle()


	## drawStats
	##---------------------------------------------------------------
	def drawStats(self, sidx, cidx, drawmode):
		## draws the stats box for the histogram

		self.vb.call("hist", "drawStats", [self, sidx, cidx, drawmode], "Drawing the stats box.")
		stats = lib.useVal("n", self.mypaf.cfg.getVar("stats"), self.salist.get("stats"), self.alist.get("stats")) 

		if stats == "n": return
		si = stats.split(",")

		mode = 111100
		if lib.isInt(si[0]): mode = int(si[0])

		ps = self.h[sidx][cidx].FindObject("stats")
		ps.SetX1NDC(float(si[1]))
		ps.SetY1NDC(float(si[2]))
		ps.SetOptStat(mode)


	## fill
	##---------------------------------------------------------------
	def fill(self, sidx, cidx, value):
		self.vb.call("hist", "fill", [self, sidx, cidx, value], "Filling a histogram.")
		self.h[sidx][cidx].fill(value)


	## getBins
	##---------------------------------------------------------------
	def getBins(self):

		self.vb.call("hist", "getBins", [self], "Retrieving the bins of a histogram.")
		bins = [clist.clist(lib.toList(self.parent.GetXaxis().GetXbins()))]
		if self.dim == 2:
			bins.append(clist.clist(lib.toList(self.parent.GetYaxis().GetXbins())))
		if self.dim == 3:
			bins.append(clist.clist(lib.toList(self.parent.GetZaxis().GetXbins())))

		return bins


	## getDim
	##---------------------------------------------------------------
	def getDim(self):
		self.vb.call("hist", "getDim", [self], "Retrieving the dimension of a histogram.")
		return self.dim


	## getH
	##---------------------------------------------------------------
	def getH(self, sidx, cidx):
		self.vb.call("hist", "getH", [self, sidx, cidx], "Retrieving a histogram.")
		return self.h[sidx][cidx]


	## getLName
	##---------------------------------------------------------------
	def getLName(self, sidx, cidx):
		self.vb.call("hist", "getLName", [self, sidx, cidx], "Retrieving the legend name.")
		return self.sources[sidx].lname


	## getParent
	##---------------------------------------------------------------
	def getParent(self):
		self.vb.call("hist", "getParent", [self], "Retrieving the parent of this instance.")
		return self.parent


	## hasLogScale
	##---------------------------------------------------------------
	def hasLogScale(self, dim = "y"):
		self.vb.call("hist", "hasLogScale", [self, dim], "Checking if the current pad has log scale.")

		if   dim == "x" and ROOT.gPad.GetLogx() == 1: return True
		elif dim == "y" and ROOT.gPad.GetLogy() == 1: return True
		elif dim == "z" and ROOT.gPad.GetLogz() == 1: return True

		return False


	## inject
	##---------------------------------------------------------------
	def inject(self, hist, sidx, cidx, sample = ""):

		self.vb.call("hist", "inject", [self, hist, sidx, cidx], "Injecting a histogram to this instance.")
		if self.alist.get("profile") == "y":
			self.h[sidx][cidx] = copy.deepcopy(hist)
			#self.h[sidx][cidx] = rstuff.copyTH1(hist)
		else:
			self.check(hist.GetDimension())
			self.h[sidx][cidx].Add(hist)


	## injectHist
	##---------------------------------------------------------------
	def injectHist(self, hist):

		self.vb.call("hist", "injectHist", [self, hist], "Injecting another hist to this instance.")
		self.check(hist.dim)

		if len(self.sources) == len(hist.sources) and len(self.categs) == len(hist.categs):
			for sidx in range(len(self.sources)):
				for cidx in range(len(self.categs)):
					self.h[sidx][cidx].Reset()
					self.h[sidx][cidx].Add(hist.getH(sidx, cidx))


	## loadInitial
	##---------------------------------------------------------------
	def loadInitial(self):

		self.vb.call("hist", "loadInitial", [self], "Loading the initial configuration of this instance.")
		if hasattr(self, "i_argstring") and hasattr(self, "i_ints"):

			self.alist.resetArgs(self.i_argstring)
			self.runPreDraw()

			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[0])):
					if self.h[sidx][cidx].Integral() == 0: continue		
					self.h[sidx][cidx].Scale(self.i_ints[sidx][cidx] / self.h[sidx][cidx].Integral())

		else:
			self.vb.warning("no initial data available, cannot load initial.")			


	## multHist
	##---------------------------------------------------------------
	def multHist(self, hist, coeffs = [], error = ''):
		self.vb.call("hist", "multHist", [self, hist, coeffs, error], "Multiply this instance by another hist.")
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = -1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Multiply(self.h[sidx][cidx], hist.getH(sidx, cidx), 1.0, coeff, error)


	## normalize
	##---------------------------------------------------------------
	def normalize(self):
		self.vb.call("hist", "normalize", [self], "Normalize the histograms in this instance according to the 'norm' argument.")

		norm =       lib.useVal("none", self.mypaf.input.cfg.getVar("norm")      , self.alist.get("norm"))
		lumi = float(lib.useVal("0"   , self.mypaf.input.cfg.getVar("luminosity"), self.alist.get("luminosity")))

		## scale according to lumi and cross section => already done in mypaf

		## scale all MC to data
		if norm == "data":
			dids = []
			for sidx in range(len(self.h)):
				if self.sources[sidx].dstype == "d":
					dids.append(sidx)

			ints = [0.0 for cidx in range(len(self.h[sidx]))]
			for cidx in range(len(self.h[0])):
				for sidx in dids:
					ints[cidx] += self.h[sidx][cidx].Integral()

			for sidx in range(len(self.h)):
				if not sidx in dids:
					for cidx in range(len(self.h[sidx])):
						if self.normalized[sidx][cidx]: continue
						self.h[sidx][cidx] = lib.normalizeHistInt(self.h[sidx][cidx], ints[cidx])
						self.normalized[sidx][cidx] = True


		## scale everything to unity
		elif norm == "unity":
			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[sidx])):
					if self.normalized[sidx][cidx]: continue
					self.h[sidx][cidx] = lib.normalizeHistInt(self.h[sidx][cidx])
					self.normalized[sidx][cidx] = True

	
	## rebin
	##---------------------------------------------------------------
	def rebin(self, hist, xbins, ybins = [], zbins = []):

		self.vb.call("hist", "rebin", [self, hist, xbins, ybins, zbins], "Rebinning a histogram.")
		## CH: only 1dim histograms to be rebinned??
		#if self.dim == 3:
		#	hist = hist.RebinAxis(array.array('d', xbins), hist.GetXaxis())
		#	hist = hist.RebinAxis(array.array('d', ybins), hist.GetYaxis())
		#	hist = hist.RebinAxis(array.array('d', zbins), hist.GetZaxis())
		#	#hist = hist.RebinX(len(xbins)-1, array.array('d', xbins))
		#	#hist = hist.RebinY(len(ybins)-1, array.array('d', ybins))
		#	#hist = hist.RebinZ(len(zbins)-1, array.array('d', zbins))
		#elif self.dim == 2: 
		#	hist = hist.RebinAxis(array.array('d', xbins), hist.GetXaxis())
		#	hist = hist.RebinAxis(array.array('d', ybins), hist.GetYaxis())
		#	#hist = hist.RebinX(len(xbins)-1, array.array('d', xbins))
		#	#hist = hist.RebinY(len(ybins)-1, array.array('d', ybins))
		#else:
		if self.dim == 1:
			hist = hist.Rebin(len(xbins)-1, "", array.array('d', xbins))

		return hist


	## rebinByParent
	##---------------------------------------------------------------
	def rebinByParent(self, hist):

		self.vb.call("hist", "rebinByParent", [self, hist], "Rebinning a histogram using the bin spacing of the parent.")
		rebin = False
		if lib.toList(self.parent.GetXaxis().GetXbins()) != lib.toList(hist.GetXaxis().GetXbins()): rebin = True
		if self.dim == 2 and \
		   lib.toList(self.parent.GetYaxis().GetXbins()) != lib.toList(hist.GetYaxis().GetXbins()): rebin = True
		elif self.dim == 3 and \
		   lib.toList(self.parent.GetZaxis().GetXbins()) != lib.toList(hist.GetZaxis().GetXbins()): rebin = True

		if rebin:
			hist = self.rebin(hist, lib.toList(self.parent.GetXaxis().GetXbins()), \
			                        lib.toList(self.parent.GetYaxis().GetXbins()), \
			                        lib.toList(self.parent.GetZaxis().GetXbins()))

		return hist


	## redraw
	##---------------------------------------------------------------
	def redraw(self, option = "", pad = 0, plot = True, save = True):

		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				self.drawn[sidx][cidx] = False

		self.draw(option, pad, plot, save)


	## redrawH
	##---------------------------------------------------------------
	def redrawH(self, sidx, cidx, pad = 0, option = "", plot = True, save = True):

		self.drawn[sidx][cidx] = False
		self.drawH(sidx, cidx, pad, option, plot, save)


	## redrawSingle
	##---------------------------------------------------------------
	def redrawSingle(self, sidx, cidx, pad, option = "", plot = True, save = True):

		self.drawn[sidx][cidx] = False
		self.drawSingle(sidx, cidx, pad, option, plot, save)


	## reinit
	##---------------------------------------------------------------
	def reinit(self, hist):
		## re-initialize this hist instance from another instance
		## this basically is a copy of the hist instance hist into this one

		self.vb.call("hist", "reinit", [self, hist], "Reinitializing this instance using the settings of another hist.")

		self.check(hist.getDim())

		self.p       = hist.p
		self.built   = False

		self.alist.reinit(hist.alist)
		self.salist.reinit(self.alist.get("style"), "1", lib.useVal("ROOT.kBlack", self.alist.get("color")))

		self.setBinArgs()
		self.setParent()
		self.setLabels()

		self.build([s.name for s in hist.sources], hist.categs)


	## runPostDraw
	##---------------------------------------------------------------
	def runPostDraw(self, sidx, cidx, option = ""):

		self.vb.call("hist", "runPostDraw", [self, sidx, cidx, option], "Run post draw functions that add additional content to the histogram.")
		self.drawArrow()
		self.drawBox()
		self.drawCircle()
		self.drawErrorBand(sidx, cidx)
		self.drawLatex()
		self.drawLine()
		self.drawNote()
		ROOT.gPad.RedrawAxis()
		self.drawStats(sidx, cidx, self.d + " " + option)


	## runPreDraw
	##---------------------------------------------------------------
	def runPreDraw(self, pad = 0):

		self.vb.call("hist", "runPreDraw", [self], "Run pre draw functions that prepare the instance for drawing.")
		self.mypaf.pads[pad].cd()
		self.mypaf.setGlobalStyle(self.alist.get("log"), self.alist.get("grid"), self.alist.get("digits"))
		self.setD()
		self.normalize()
		self.setHistLabels(pad)
		self.setRange()
		self.setStats()
		self.setStyle()


	## saveHist
	##---------------------------------------------------------------
	def saveHist(self, sidx, cidx):

		self.vb.call("hist", "saveHist", [self, sidx, cidx], "Saving a histogram.")
		self.h[sidx][cidx] = lib.saveHist(self.mypaf.output.file, self.h[sidx][cidx], self.sources[sidx].name + "/" + self.categs[cidx] + "/" + self.name)


	## setArgs
	##---------------------------------------------------------------
	def setArgs(self, argstring = ""):
		## old arguments are added to new ones

		self.vb.call("hist", "setArgs", [self, argstring], "Setting the arguments of this instance.")
		self.alist.setArgs(argstring)


	## setBinArgs
	##---------------------------------------------------------------
	def setBinArgs(self):

		self.vb.call("hist", "setBinArgs", [self], "Setting the binargs of this instance.")
		self.binargs = []

		## 1d histogram
		if self.dim >= 1:
			oname = lib.useVal("var", self.alist.get("obs"), self.alist.get("obsx"))
			obs   = self.db.getRow("observables", "name=='" + oname + "'")
			if obs[7].strip() == "[]": bins = list(lib.bins(int(obs[4]), float(obs[5]), float(obs[6])))
			else                     : bins = eval(obs[7])
			self.binargs.append(clist.clist(lib.useArr(bins, lib.getBinArgs(self.alist, "x"))))

		## 2d histogram
		if self.dim >= 2:
			obs2 = self.db.getRow("observables", "name=='" + self.alist.get("obsy") + "'")			
			if obs2[7].strip() == "[]": bins = list(lib.bins(int(obs2[4]), float(obs2[5]), float(obs2[6])))
			else                      : bins = eval(obs2[7])
			self.binargs.append(clist.clist(lib.useArr(bins, lib.getBinArgs(self.alist, "y"))))

		## 2d histogram
		if self.dim == 3:
			obs3 = self.db.getRow("observables", "name=='" + self.alist.get("obsz") + "'")			
			if obs3[7].strip() == "[]": bins = list(lib.bins(int(obs3[4]), float(obs3[5]), float(obs3[6])))
			else                      : bins = eval(obs3[7])
			self.binargs.append(clist.clist(lib.useArr(bins, lib.getBinArgs(self.alist, "z"))))


	## setBinContent
	##---------------------------------------------------------------
	def setBinContent(self, sidx, cidx, bin, value):
		self.vb.call("hist", "setBinContent", [self, sidx, cidx, bin, value], "Setting the bin content in a histogram.")
		self.h[sidx][cidx].SetBinContent(bin, value)


	## setD
	##---------------------------------------------------------------
	def setD(self):
	
		self.vb.call("hist", "setD", [self], "Setting the draw mode from the arguments.")

		default = ["hist", "colz text e", "iso"]
		self.d = lib.useVal(default[self.dim - 1], self.mypaf.input.cfg.getVar("draw" + str(self.dim) + "mode").replace("_", " "), 
		                                           self.alist.get("draw" + str(self.dim) + "mode").replace("_", " "))
	
		errors = lib.useVal("none", self.mypaf.input.cfg.getVar("errors"), self.alist.get("errors"))
		if errors == "bars":
			self.d += " e"


	## setHistLabels
	##---------------------------------------------------------------
	def setHistLabels(self, pad = 0):

		self.vb.call("hist", "setLabels", [self], "Setting the axis labels.")
		factor     = lib.getPadSize(self.mypaf.pads[pad])
		labelsizex = eval(lib.useVal("0.045 / " + str(factor), self.alist.get("labelsize"), self.alist.get("labelsizex")))
		labelsizey = eval(lib.useVal("0.045 / " + str(factor), self.alist.get("labelsize"), self.alist.get("labelsizey")))
		labelsizez = eval(lib.useVal("0.045 / " + str(factor), self.alist.get("labelsize"), self.alist.get("labelsizez")))

		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				self.h[sidx][cidx].SetTitle("")
				self.h[sidx][cidx].GetXaxis().SetTitle(self.labels[0])
				self.h[sidx][cidx].GetXaxis().SetLabelSize(labelsizex)
				self.h[sidx][cidx].GetXaxis().SetTitleSize(labelsizex)
				self.h[sidx][cidx].GetXaxis().SetNdivisions(505)
				self.h[sidx][cidx].GetYaxis().SetTitle(self.labels[1])
				self.h[sidx][cidx].GetYaxis().SetLabelSize(labelsizey)
				self.h[sidx][cidx].GetYaxis().SetTitleSize(labelsizey)
				self.h[sidx][cidx].GetYaxis().SetTitleOffset(factor*1.15)
				self.h[sidx][cidx].GetYaxis().SetNdivisions(505)
				if len(self.labels) > 2: 
					self.h[sidx][cidx].GetZaxis().SetTitle(self.labels[2])
					self.h[sidx][cidx].GetZaxis().SetLabelSize(labelsizez)
					self.h[sidx][cidx].GetZaxis().SetTitleSize(labelsizez)
					self.h[sidx][cidx].GetZaxis().SetTitleOffset(factor)
					self.h[sidx][cidx].GetZaxis().SetNdivisions(505)


	## setInitial
	##---------------------------------------------------------------
	def setInitial(self):

		self.vb.call("hist", "setInitial", [self], "Setting the initial configuration.")
		self.i_argstring = self.alist.argstring
		self.i_ints      = [[1. for cidx in range(len(self.h[0]))] for sidx in range(len(self.h))]

		if self.alist.get("profile") != "y":
			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[0])):
					self.i_ints[sidx][cidx] = self.h[sidx][cidx].Integral()
	

	## setLabels
	##---------------------------------------------------------------
	def setLabels(self):

		self.vb.call("hist", "setLabels", [self], "Setting the labels of this instance.")
		self.labels = []

		## 1d histogram
		if self.dim >= 1:
			oname = lib.useVal("var", self.alist.get("obs"), self.alist.get("obsx"))
			obs1 = self.db.getRow("observables", "name=='" + oname + "'")
			self.labels.append(obs1[1])

		if self.dim == 1:
			spacing = lib.equalBinSpacing(self.binargs[0].list)
			add = "/" + str(spacing) + obs1[2] if spacing > 0 else "/bin"
			self.labels.append(lib.getObjFullName(obs1[3].strip() + add))
			return

		## 2d histogram
		if self.dim >= 2:
			obs2 = self.db.getRow("observables", "name=='" + self.alist.get("obsy") + "'")			
			self.labels.append(obs2[1])

		if self.dim == 2:
			self.labels.append(lib.getObjFullName(obs2[3].strip()))
			return

		## 3d histogram
		if self.dim == 3:
			obs3 = self.db.getRow("observables", "name=='" + self.alist.get("obsz") + "'")			
			self.labels.append(obs3[1])


	## setNormalizedLumi
	##---------------------------------------------------------------
	def setNormalizedLumi(self):
		self.vb.call("hist", "setNormalizedLumi", [self], "Setting the normalized parameter to True in case of normalization to luminosity.")

		norm = lib.useVal("none", self.mypaf.input.cfg.getVar("norm"), self.alist.get("norm"))

		if norm == "lumi":
			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[0])):
					self.normalized[sidx][cidx] = True


	## setP
	##---------------------------------------------------------------
	def setP(self, pvalue = False):
	
		self.vb.call("hist", "setP", [self, pvalue], "Setting the plot mode.")
		self.p = pvalue


	## setParent
	##---------------------------------------------------------------
	def setParent(self):
		## creates the parent histogram

		self.vb.call("hist", "setParent", [self], "Setting the parent histogram.")
		self.parent = None
	
		## 1d histogram
		if   self.dim == 1:
			self.parent = ROOT.TH1F(self.name, "", int(self.binargs[0].len) - 1, array.array('d', self.binargs[0].list))		

		## 1d profile histogram
		elif self.dim == 2 and self.alist.get("profile") == "y":
			self.parent = ROOT.TProfile2D(self.name, "", int(self.binargs[0].len) - 1, array.array('d', self.binargs[0].list), \
			                                             int(self.binargs[1].len) - 1, array.array('d', self.binargs[1].list))
		## 2d histogram
		elif self.dim == 2:
			self.parent = ROOT.TH2F      (self.name, "", int(self.binargs[0].len) - 1, array.array('d', self.binargs[0].list), \
			                                             int(self.binargs[1].len) - 1, array.array('d', self.binargs[1].list))
		## 3d histogram
		elif self.dim == 3:
			self.parent = ROOT.TH3F(self.name, "", int(self.binargs[0].len) - 1, array.array('d', self.binargs[0].list), \
			                                       int(self.binargs[1].len) - 1, array.array('d', self.binargs[1].list), \
			                                       int(self.binargs[2].len) - 1, array.array('d', self.binargs[2].list))



	## setRange
	##---------------------------------------------------------------
	def setRange(self):

		## check if
		## - need min to be set to 0
		## - if using log scale, then set to 0.001 instead
		## - etc

		self.vb.call("hist", "setRange", [self], "Setting the histogram ranges.")

		if self.dim == 1: dim = "y"
		else            : dim = "z"

		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):

				if self.dim == 1: axis = self.h[sidx][cidx].GetYaxis()
				else            : axis = self.h[sidx][cidx].GetZaxis()

				hrange = lib.findHistRange(self.h[sidx][cidx], dim, self.hasLogScale(dim))
				min = float(lib.useVal(str(hrange[0]), self.salist.get("min"), self.alist.get(dim + "min"), self.alist.get("min")))
				max = float(lib.useVal(str(hrange[1]), self.salist.get("max"), self.alist.get(dim + "max"), self.alist.get("max")))

				axis.SetRangeUser(min, max)


	## setStats
	##---------------------------------------------------------------
	def setStats(self):
		## activates or deactivates the stats box for the histogram

		self.vb.call("hist", "setStats", [self], "Applying the 'stats' argument to this instance.")

		stats = lib.useVal("n", self.mypaf.input.cfg.getVar("stats"), self.alist.get("stats"))
		si    = stats.split(",")

		if si[0] == "n":
			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[0])):
					self.h[sidx][cidx].SetStats(0)
	

	## setStyle
	##---------------------------------------------------------------
	def setStyle(self):
		self.vb.call("hist", "setStyle", [self], "Applying the source information (styling, colors, ..) to this instance.")


		for sidx in range(len(self.h)):

			col = self.sources[sidx].color
			if self.dim == 2 and self.d.find("text") != -1: 
				col = "ROOT.kBlack"

			color       = eval (lib.useVal("ROOT.kBlack", col                                , self.salist.get("color"      ), self.alist.get("color"      )))
			fillstyle   = int  (lib.useVal("1001"       , str(self.sources[sidx].fillstyle)  , self.salist.get("fillstyle"  ), self.alist.get("fillstyle"  )))
			linestyle   = int  (lib.useVal("1"          , str(self.sources[sidx].linestyle)  , self.salist.get("linestyle"  ), self.alist.get("linestyle"  )))
			linewidth   = int  (lib.useVal("2"          , str(self.sources[sidx].linewidth)  , self.salist.get("linewidth"  ), self.alist.get("linewidth"  )))
			markerstyle = int  (lib.useVal("8"          , str(self.sources[sidx].markerstyle), self.salist.get("markerstyle"), self.alist.get("markerstyle")))
			markersize  = float(lib.useVal("1.8"        , str(self.sources[sidx].markersize) , self.salist.get("markersize" ), self.alist.get("markersize" )))

			for cidx in range(len(self.h[sidx])):
				self.h[sidx][cidx].SetFillColor(color)
				self.h[sidx][cidx].SetFillStyle(fillstyle)
				self.h[sidx][cidx].SetLineColor(color)
				self.h[sidx][cidx].SetLineStyle(linestyle)
				self.h[sidx][cidx].SetLineWidth(linewidth)
				self.h[sidx][cidx].SetMarkerColor(color)
				self.h[sidx][cidx].SetMarkerStyle(markerstyle)
				self.h[sidx][cidx].SetMarkerSize(markersize)


	## subHist
	##---------------------------------------------------------------
	def subHist(self, hist, coeffs = []):
		self.vb.call("hist", "subHist", [self, hist, coeffs], "Subtracting another hist from this instance.")
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = -1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Add(hist.getH(sidx, cidx), coeff)


