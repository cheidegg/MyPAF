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
import args, clist, lib, hstyle, rstuff, schemes, source


## hist
##------------------------------------------------------------------- 
class hist:



	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, name, binargs, labels, argstring = ""):

		self.name    = name
		self.binargs = binargs
		self.p       = False
		self.built   = False

		self.dlist   = args.args("")
		self.alist   = args.args(argstring)
		self.mypaf   = mypaf
		self.db      = mypaf.db
		self.vb      = mypaf.vb
		self.vb.call("hist", "__init__", [self, mypaf, name, binargs, labels, argstring], "Initializing the hist class.")

		self.setParent()
		self.setLabels(labels)
		self.setD()
		#self.setGen()


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


	## applyArgs
	##---------------------------------------------------------------
	def applyArgs(self, pad = 0):
		self.vb.call("hist", "applyArgs", [self, pad], "Applying the arguments of this instance.")

		## reset source (for hists in schemes, they only have one hist and source)
		if self.alist.has("source") and len(self.sources) == 1:
			self.sources = None
			self.sources = [source.source(self.mypaf, self.alist.get("source"))]

		## load default style if given
		if self.alist.has("style"):
			self.defaults  = self.db.getRow("hstyles", "name == '" + self.alist.get("style") + "'")
			#self.dlist.set("

		## apply style stuff	
		self.applyGrid  ()
		self.applyLog   (pad)
		self.applyErrors()
		self.applyNorm  ()
		self.applyDigits()


	## applyDigits
	##---------------------------------------------------------------
	def applyDigits(self):
		self.vb.call("hist", "applyDigits", [self], "Applying the 'digits' argument to this instance.")

		if self.alist.has("digits") and int(self.alist.get("digits")) > 0:
			ROOT.TGaxis.SetMaxDigits(int(self.alist.get("digits")))
			#ROOT.gPad.Modified()
			#ROOT.gPad.Update()


	## applyErrors
	##---------------------------------------------------------------
	def applyErrors(self):
		self.vb.call("hist", "applyErrors", [self], "Applying the 'errors' argument to this instance.")

		if self.alist.has("errors")                           : errors = self.alist.get("errors")
		elif hasattr(self, "defaults") and self.defaults != []: errors = self.defaults[4]
		else                                                  : errors = "none"

		if errors == "bars":
			self.d += " e"


	## applyGrid
	##---------------------------------------------------------------
	def applyGrid(self):
		self.vb.call("hist", "applyGrid", [self], "Applying the 'grid' argument to this instance.")

		if self.alist.has("grid")                             : grid  = self.alist.get("grid")
		elif hasattr(self, "defaults") and self.defaults != []: grid  = self.defaults[2]
		else                                                  : grid  = "n"

		if grid == "y":
			for pad in self.mypaf.pads:
				pad.SetGrid(1, 1)


	## applyLog
	##---------------------------------------------------------------
	def applyLog(self, pad = 0):
		self.vb.call("hist", "applyLog", [self], "Applying the 'log' argument to this instance.")

		if self.alist.has("log")                              : log = self.alist.get("log")
		elif hasattr(self, "defaults") and self.defaults != []: log = self.defaults[3]
		else                                                  : log = "none"

		pad = self.mypaf.pads[pad]

		if log.find("x") != -1: pad.SetLogx()
		if log.find("y") != -1: pad.SetLogy()
		if log.find("z") != -1: pad.SetLogz()


	## applyNorm
	##---------------------------------------------------------------
	def applyNorm(self):
		self.vb.call("hist", "applyNorm", [self], "Applying the 'norm' argument to this instance.")

		if self.alist.has("norm")                             : norm  = self.alist.get("norm")
		elif hasattr(self, "defaults") and self.defaults != []: norm  = self.defaults[5]
		else                                                  : norm  = "none"


		## scale according to lumi and cross section
		if norm == "lumi":
			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[sidx])):
					self.h[sidx][cidx].Scale(float(self.mypaf.input.cfg.getVar("luminosity")) * float(self.sources[sidx].getXSec()) / float(self.sources[sidx].getNEvts()))
		## where does the xsec and nevts come from?

		## scale all MC to data
		elif norm == "data":
			dids = []
			for sidx in range(len(self.h)):
				if self.sources[sidx].getType() == "d":
					dids.append(sidx)

			ints = [0.0 for cidx in range(len(self.h[sidx]))]
			for cidx in range(len(self.h[0])):
				for sidx in dids:
					ints += self.h[sidx][cidx].Integral()

			for sidx in range(len(self.h)):
				if not sidx in dids:
					for cidx in range(len(self.h[sidx])):
						if self.h[sidx][cidx].Integral() > 0:
							self.h[sidx][cidx].Scale(ints[cidx].Integral() / self.h[sidx][cidx].Integral())


		## scale everything to unity
		elif norm == "unity":
			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[sidx])):
					if self.h[sidx][cidx].Integral() > 0:
						self.h[sidx][cidx].Scale(1.0 / self.h[sidx][cidx].Integral())
	

	## applySourceInfo
	##---------------------------------------------------------------
	def applySourceInfo(self):
		self.vb.call("hist", "applySourceInfo", [self], "Applying the source information (styling, colors, ..) to this instance.")

		for sidx in range(len(self.h)):

			col = eval(self.sources[sidx].color)
			if self.dim == 2 and self.d.find("text") != -1: 
				col = ROOT.kBlack
			acol = ""
			if self.alist.has("color"): 
				acol = str(eval(self.alist.get("color")))

			color       = lib.argsWin(ROOT.kBlack, col                           , acol                         )
			fillstyle   = lib.argsWin(1001       , self.sources[sidx].fillstyle  , self.alist.get("fillstyle"  ))
			linestyle   = lib.argsWin(1          , self.sources[sidx].linestyle  , self.alist.get("linestyle"  ))
			linewidth   = lib.argsWin(2          , self.sources[sidx].linewidth  , self.alist.get("linewidth"  ))
			markerstyle = lib.argsWin(8          , self.sources[sidx].markerstyle, self.alist.get("markerstyle"))
			markersize  = lib.argsWin(1.8        , self.sources[sidx].markersize , self.alist.get("markersize" ))

			for cidx in range(len(self.h[sidx])):
				self.h[sidx][cidx].SetFillColor(color)
				self.h[sidx][cidx].SetFillStyle(fillstyle)
				self.h[sidx][cidx].SetLineColor(color)
				self.h[sidx][cidx].SetLineStyle(linestyle)
				self.h[sidx][cidx].SetLineWidth(linewidth)
				self.h[sidx][cidx].SetMarkerColor(color)
				self.h[sidx][cidx].SetMarkerStyle(markerstyle)
				self.h[sidx][cidx].SetMarkerSize(markersize)


	## applyStats
	##---------------------------------------------------------------
	def applyStats(self):
		## activates the stats box for the histogram
		self.vb.call("hist", "applyStats", [self], "Applying the 'stats' argument to this instance.")

		si = self.alist.get("stats").split(",")

		if not self.alist.has("stats") or si[0] == "n": 
			for sidx in range(len(self.h)):
				for cidx in range(len(self.h[0])):
					self.h[sidx][cidx].SetStats(0)


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
				hc.SetName(s.name + ":=" + c + ":=" + self.name)
				appender.append(hc)

			self.h.append(appender)

		self.built = True	
		

	## check
	##---------------------------------------------------------------
	def check(self, dim):
		self.vb.call("hist", "check", [self], "Performing basic dimension checks.")

		if not hasattr(self, "dim"): 
			self.dim = dim
		else: 
			if self.dim != dim: 
				self.vb.error("Trying to re-initialize a histogram of wrong dimension.")


	## detachArgs
	##---------------------------------------------------------------
	def detachArgs(self):
		## need to reset default status of canvas and pad after plotting
		self.vb.call("hist", "detachArgs", [self], "Resetting certain argument values.")

		self.detachGrid()
		self.detachLog()
		self.detachDigits()


	## detachDigits
	##---------------------------------------------------------------
	def detachDigits(self):
		self.vb.call("hist", "detachDigits", [self], "Resetting the 'digits' argument.")
		self.mypaf.applyDigits()


	## detachGrid
	##---------------------------------------------------------------
	def detachGrid(self):
		self.vb.call("hist", "detachGrid", [self], "Resetting the 'grid' argument.")
		self.mypaf.applyGrid()


	## detachLog	
	##---------------------------------------------------------------
	def detachLog(self):
		self.vb.call("hist", "detachLog", [self], "Resetting the 'log' argument.")
		self.mypaf.applyLog()


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

		self.prepareDraw(pad)

		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				self.mypaf.pads[pad].cd()
				self.drawH(sidx, cidx, option, plot, save)

		self.detachArgs()



	## drawArrow
	##---------------------------------------------------------------
	def drawArrow(self):
		## takes all drawarrow arguments and draws an arrows to the histogram
		## for all of them
		## format of drawlatex argument is x1,y1,x2,y2,strength,color

		self.vb.call("hist", "drawArrow", [self], "Drawing an arrow.")
		if self.alist.has("drawarrow"):
			li = [l.split(",") for l in self.alist.getAll("drawarrow")]
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
		if self.alist.has("drawbox"):
			print "draw a box"


	## drawCircle
	##---------------------------------------------------------------
	def drawCircle(self):
	
		self.vb.call("hist", "drawCircle", [self], "Drawing a circle.")
		if self.alist.has("drawcircle"):

			li = [l.split(",") for l in self.alist.getAll("drawcircle")]
			ci = []



	## drawErrorBand
	##---------------------------------------------------------------
	def drawErrorBand(self, sidx, cidx):

		self.vb.call("hist", "drawErrorBand", [self, sidx, cidx], "Drawing error bands.")
		errors = lib.useVal("none", self.dlist.get("errors"), self.alist.get("errors"))

		if errors == "band":
			hband = copy.deepcopy(self.h[sidx][cidx])
			hband.SetFillColor(ROOT.kGray)
			hband.SetFillStyle(3001)
			hband.SetLineColor(ROOT.kGray)
			#hband.Draw("e2 same")


	## drawH
	##---------------------------------------------------------------
	def drawH(self, sidx, cidx, option = "", plot = True, save = True):

		self.vb.call("hist", "drawH", [self, sidx, cidx, option, plot, save], "Drawing a histogram from this instance.")
		self.vb.talk("Drawing histogram " + self.name + " with " + str(self.h[sidx][cidx].GetEntries()) + " entries for source " + self.sources[sidx].name + " and category " + self.categs[cidx] + ".", 1)

		self.runPreDraw(sidx, cidx)

		self.drawRange(sidx, cidx)
		self.h[sidx][cidx].Draw(self.d + option)
		ROOT.gPad.Update()
		if save:
			self.saveHist(sidx, cidx)
		if self.p and plot:
			self.drawArrow()
			self.drawBox()
			self.drawCircle()
			self.drawErrorBand(sidx, cidx)
			self.drawLatex()
			self.drawLine()
			self.drawNote()
			ROOT.gPad.RedrawAxis()
			self.drawStats(sidx, cidx, self.d + option)
			self.mypaf.saveCanv(self.name + "_" + self.sources[sidx].name + "_" + self.categs[cidx])


	## drawLabels
	##---------------------------------------------------------------
	def drawLabels(self):

		self.vb.call("hist", "drawLabels", [self], "Drawing labels.")
		pad = ROOT.gPad
		factor = lib.getPadSize(pad)

		##print "drawing labels for " + self.name + " (" + str(self.labels) + ")"	
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				self.h[sidx][cidx].SetTitle("")
				self.h[sidx][cidx].GetXaxis().SetTitle(self.labels[0])
				self.h[sidx][cidx].GetXaxis().SetLabelSize(0.045 / factor)
				self.h[sidx][cidx].GetXaxis().SetTitleSize(0.045 / factor)
				self.h[sidx][cidx].GetXaxis().SetNdivisions(505)
				self.h[sidx][cidx].GetYaxis().SetTitle(self.labels[1])
				self.h[sidx][cidx].GetYaxis().SetLabelSize(0.045 / factor)
				self.h[sidx][cidx].GetYaxis().SetTitleSize(0.045 / factor)
				self.h[sidx][cidx].GetYaxis().SetTitleOffset(factor)
				self.h[sidx][cidx].GetYaxis().SetNdivisions(505)
				if len(self.labels) > 2: 
					self.h[sidx][cidx].GetZaxis().SetTitle(self.labels[2])
					self.h[sidx][cidx].GetZaxis().SetLabelSize(0.045 / factor)
					self.h[sidx][cidx].GetZaxis().SetTitleSize(0.045 / factor)
					self.h[sidx][cidx].GetZaxis().SetTitleOffset(factor)
					self.h[sidx][cidx].GetZaxis().SetNdivisions(505)


	## drawLatex
	##---------------------------------------------------------------
	def drawLatex(self):
		## takes all drawlatex arguments and draws a text to the histogram
		## for all of them
		## format of drawlatex argument is x,y,align,textfont,textsize,textcolor,text(_)

		self.vb.call("hist", "drawLatex", [self], "Drawing latex objects.")
		if self.alist.has("drawlatex"):

			li = [l.split(",") for l in self.alist.getAll("drawlatex")]
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
		if self.alist.has("drawline"):
			li = [l.split(",") for l in self.alist.getAll("drawline")]
			ln = []
			for ii, l in enumerate(li):
				ln.append(rstuff.line(int(lib.useVal("2", l[4])), int(lib.useVal("7", l[5])), eval(lib.useVal(str(ROOT.kBlack), l[6]))))
				ln[ii].DrawLine(float(l[0]) * self.parent.GetXaxis().GetXmin(), \
				                float(l[1]) * self.parent.GetYaxis().GetXmin(), \
				                float(l[2]) * self.parent.GetXaxis().GetXmax(), \
				                float(l[3]) * self.parent.GetYaxis().GetXmax())


	## drawRange
	##---------------------------------------------------------------
	def drawRange(self, sidx, cidx):

		## check if
		## - need min to be set to 0
		## - if using log scale, then set to 0.001 instead
		## - etc

		print "drawing range with " + self.alist.argstring	
		print "min = " + self.alist.get("min")
		self.vb.call("hist", "drawRange", [self, sidx, cidx], "Drawing the histogram ranges.")

		if self.dim == 1:
			dim = "y"
			axis = self.h[sidx][cidx].GetYaxis()
		else:
			dim = "z"
			axis = self.h[sidx][cidx].GetZaxis()

		range = lib.findHistRange(self.h[sidx][cidx], dim, self.hasLogScale(dim))
		min = float(lib.useVal(str(range[0]), self.alist.get(dim + "min"), self.alist.get("min")))
		max = float(lib.useVal(str(range[1]), self.alist.get(dim + "max"), self.alist.get("max")))

		print dim
		print axis
		print range
		print min
		print max

		axis.SetRangeUser(min, max)
		

	## drawNote
	##---------------------------------------------------------------
	def drawNote(self):

		self.vb.call("hist", "drawNote", [self], "Drawing lumi or CMS notes.")
		note = lib.useVal("none", self.mypaf.cfg.getVar("note"), self.dlist.get("note"), self.alist.get("note"))

		if note == "cms":
			mcOnly = True
			rstuff.cms(self.mypaf.canvas, float(self.mypaf.input.cfg.getVar("luminosity")), float(self.mypaf.input.cfg.getVar("energy")), mcOnly)


	## drawStats
	##---------------------------------------------------------------
	def drawStats(self, sidx, cidx, drawmode):
		## draws the stats box for the histogram

		self.vb.call("hist", "drawStats", [self, sidx, cidx, drawmode], "Drawing the stats box.")
		if not self.alist.has("stats"): return
		si = self.alist.get("stats").split(",")

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


	## getBinArgs
	##---------------------------------------------------------------
	def getBinArgs(self, dim = "x"):

		self.vb.call("hist", "getBinArgs", [self, dim], "Retrieving the bin arguments of a histogram.")
		if self.alist.has("n" + dim + "bins") and self.alist.has(dim + "bins"):
			eval("bins = [" + self.args.get(dim + "bins") + "]")
			return int(self.alist.get("n" + dim + "bins")), array.array('d', bins)

		if self.alist.has("n" + dim + "bins") and self.alist.has(dim + "min") and self.alist.has(dim + "max"):

			return int(self.alist.get("n" + dim + "bins")), lib.bins(int(self.alist.get("n" + dim + "bins")), float(self.alist.get(dim + "min")), float(self.alist.get(dim + "max")))

		return 0, []


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
	def inject(self, hist, sidx, cidx):

		self.vb.call("hist", "inject", [self, hist, sidx, cidx], "Injecting a histogram to this instance.")
		if self.alist.get("profile") == "y":
			self.h[sidx][cidx] = copy.deepcopy(hist)
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
			self.applyArgs()

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


	## prepareDraw
	##---------------------------------------------------------------
	def prepareDraw(self, pad):

		self.vb.call("hist", "prepareDraw", [self, pad], "Preparing the instance for drawing.")
		self.applyArgs(pad)
		self.applySourceInfo()
		self.applyStats()
		self.drawLabels()
		self.setD()


	
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


	## reinit
	##---------------------------------------------------------------
	def reinit(self, hist):
		## re-initialize this hist instance from another instance
		## this basically is a copy of the hist instance hist into this one

		self.vb.call("hist", "reinit", [self, hist], "Reinitializing this instance using the settings of another hist.")

		self.binargs = hist.binargs

		self.alist.reinit(hist.alist)

		self.parent = None
		self.setParent()
		self.setLabels(hist.labels)
		self.setD()
		self.setP(hist.p)

		self.build([s.name for s in hist.sources], hist.categs)


	## resetArgs
	##---------------------------------------------------------------
	def resetArgs(self, argstring = ""):
		## old arguments are overwritten by new ones

		self.vb.call("hist", "resetArgs", [self, argstring], "Resetting the arguments of this instance.")
		self.alist.resetArgs(argstring)


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


	## setBinContent
	##---------------------------------------------------------------
	def setBinContent(self, sidx, cidx, bin, value):
		self.vb.call("hist", "setBinContent", [self, sidx, cidx, bin, value], "Setting the bin content in a histogram.")
		self.h[sidx][cidx].SetBinContent(bin, value)


	## setD
	##---------------------------------------------------------------
	def setD(self):
	
		self.vb.call("hist", "setD", [self], "Setting the draw mode from the arguments.")
		self.d = ""
	
		if self.dim == 1:
			if self.alist.has("draw1mode"): self.d = self.alist.get("draw1mode").replace("_", " ")
			else                          : self.d = "hist"
	
		elif self.dim == 2:
			if self.alist.has("draw2mode"): self.d = self.alist.get("draw2mode").replace("_", " ")
			else                          : self.d = "colz text e"
	
		elif self.dim == 3:
			if self.alist.has("draw3mode"): self.d = self.alist.get("draw3mode").replace("_", " ")
			else                          : self.d = "iso"


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
	def setLabels(self, labels):

		self.vb.call("hist", "setLabels", [self, labels], "Setting the labels.")
		self.labels = labels
		if   self.dim == 1 and len(self.labels[1]) > 4 and self.labels[1][-4:] != "/bin": self.labels[1] += "/bin"
		##elif self.dim == 2 and len(self.labels[2]) > 4 and self.labels[2][-4:] != "/bin": self.labels[2] += "/bin"
		## no label for color axis?
	

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
		binargs = self.binargs
		self.parent = None
	
		## 1d histogram
		if   len(binargs) == 1:
			self.check(1)
			nxbins, xbins = self.getBinArgs("x")
			if nxbins == 0: 
				xbins = array.array('d', binargs[0].list)
				nxbins = int(binargs[0].len) - 1
			self.parent = ROOT.TH1F(self.name, "", nxbins, xbins)

		## 1d histogram
		elif len(binargs) == 3: 
			self.check(1)
			nxbins, xbins = self.getBinArgs("x")
			if nxbins == 0: 
				nxbins = int(binargs[0])
				xbins = lib.bins(nxbins, binargs[1], binargs[2])
			self.parent = ROOT.TH1F(self.name, "", nxbins, xbins)

		## 2d histogram
		elif len(binargs) == 2:
			self.check(2)
			nxbins, xbins = self.getBinArgs("x")
			nybins, ybins = self.getBinArgs("y")
			if nxbins == 0: 
				xbins = array.array('d', binargs[0].list)
				nxbins = int(binargs[0].len) - 1
			if nybins == 0: 
				ybins = array.array('d', binargs[1].list)
				nybins = int(binargs[1].len) - 1
			if self.alist.get("profile") == "y": self.parent = ROOT.TProfile2D(self.name, "", nxbins, xbins, nybins, ybins)
			else                               : self.parent = ROOT.TH2F      (self.name, "", nxbins, xbins, nybins, ybins)

		## 2d histogram
		elif len(binargs) == 6:
			self.check(2)
			nxbins, xbins = self.getBinArgs("x")
			nybins, ybins = self.getBinArgs("y")
			if nxbins == 0: 
				nxbins = int(binargs[0])
				xbins = lib.bins(nxbins, binargs[1], binargs[2])
			if nybins == 0: 
				nybins = int(binargs[3])
				ybins = lib.bins(nybins, binargs[4], binargs[5])
			if self.alist.get("profile") == "y": self.parent = ROOT.TProfile2D(self.name, "", nxbins, xbins, nybins, ybins)
			else                               : self.parent = ROOT.TH2F      (self.name, "", nxbins, xbins, nybins, ybins)

		## 3d histogram
		elif len(binargs) == 7:
			self.check(3)
			nxbins, xbins = self.getBinArgs("x")
			nybins, ybins = self.getBinArgs("y")
			nzbins, zbins = self.getBinArgs("z")
			if nxbins == 0: 
				nxbins = int(binargs[0])
				xbins  = array.array('d', binargs[1].list)
			if nybins == 0: 
				nybins = int(binargs[2])
				ybins  = array.array('d', binargs[3].list)
			if nzbins == 0: 
				nzbins = int(binargs[4])
				zbins  = array.array('d', binargs[5].list)
			self.parent = ROOT.TH3F(self.name, "", nxbins, xbins, nybins, ybins, nzbins, zbins)

		## 3d histogram
		elif len(binargs) == 9:
			self.check(3)
			nxbins, xbins = self.getBinArgs("x")
			nybins, ybins = self.getBinArgs("y")
			nzbins, zbins = self.getBinArgs("z")
			if nxbins == 0: 
				nxbins = int(binargs[0])
				xbins = lib.bins(nxbins, binargs[1], binargs[2])
			if nybins == 0: 
				nybins = int(binargs[3])
				ybins = lib.bins(nybins, binargs[4], binargs[5])
			if nzbins == 0: 
				nzbins = int(args[6])
				zbins = lib.bins(nzbins, binargs[7], binargs[8])
			self.parent = ROOT.TH3F(self.name, "", nxbins, xbins, nybins, ybins, nzbins, zbins)

		## options are bad
		else:
			self.vb.error("trying to initialize a histogram with unknown set of arguments")


	### setStyle
	###---------------------------------------------------------------
	#def setStyle(self):

	#	name = "custom"
	#	if self.alist.has("style"): name = self.alist.get("style")

	#	hs = hstyle.hstyle(self.db, name, self.alist)		
	#	self.parent = hs.build(self.parent)

	#	for sidx in range(len(self.h)):
	#		for cidx in range(len(self.h[0])):
	#			self.h[sidx][cidx] = hs.build(self.h[sidx][cidx])


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


