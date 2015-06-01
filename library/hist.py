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

	#dim     = 0
	#var     = "zombie"
	#binargs = None

	#d       = ""
	#h       = []
	#p       = False
	#parent  = None

	#alist   = None
	mypaf   = None
	db      = None
	vb      = None


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, var, binargs, labels, arglist = ""):

		self.var     = var
		self.binargs = binargs
		self.p       = False
		self.built   = False

		self.alist   = args.args(arglist)
		self.mypaf   = mypaf
		self.db      = mypaf.db
		self.vb      = mypaf.vb

		self.setParent()
		self.setLabels(labels)
		self.setD()
		#self.setGen()


	## addHist
	##---------------------------------------------------------------
	def addHist(self, hist, coeffs = []):
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = 1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Add(hist.getH(sidx, cidx), coeff)


	## applyArgs
	##---------------------------------------------------------------
	def applyArgs(self):


		## reset source (for hists in schemes, they only have one hist and source)
		if self.alist.has("source") and len(self.sources) == 1:
			self.sources = None
			self.sources = [source.source(self.mypaf, self.alist.get("source"))]

		## load default style if given
		self.defaults = []
		if self.alist.has("style"):
			self.defaults  = self.db.getRow("hstyles", "name == '" + self.alist.get("style") + "'")

		## apply style stuff	
		self.applyGrid  ()
		self.applyLog   ()
		self.applyErrors()
		self.applyNorm  ()


	## applyErrors
	##---------------------------------------------------------------
	def applyErrors(self):

		if self.alist.has("errors")                           : errors = self.alist.get("errors")
		elif hasattr(self, "defaults") and self.defaults != []: errors = self.defaults[4]
		else                                                  : errors = "none"

		if errors == "bars":
			self.d += " e"


	## applyGrid
	##---------------------------------------------------------------
	def applyGrid(self):

		if self.alist.has("grid")                             : grid  = self.alist.get("grid")
		elif hasattr(self, "defaults") and self.defaults != []: grid  = self.defaults[2]
		else                                                  : grid  = "n"

		if grid == "y":
			for pad in self.mypaf.pads:
				pad.SetGrid(1, 1)


	## applyLog
	##---------------------------------------------------------------
	def applyLog(self):

		if self.alist.has("log")                              : log = self.alist.get("log")
		elif hasattr(self, "defaults") and self.defaults != []: log = self.defaults[3]
		else                                                  : log = "none"

		if log.find("x") != -1:
			ROOT.gPad.SetLogx()
		if log.find("y") != -1:
			ROOT.gPad.SetLogy()
		if log.find("z") != -1:
			ROOT.gPad.SetLogz()


	## applyNorm
	##---------------------------------------------------------------
	def applyNorm(self):

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

		for sidx in range(len(self.h)):

			col = eval(self.sources[sidx].color)
			if self.dim == 2 and self.d.find("colz") != -1 and self.d.find("text") != -1: 
				col = ROOT.kBlack

			color       = lib.argsWin(ROOT.kBlack, col                           , self.alist.get("color"      ))
			fillstyle   = lib.argsWin(1001       , self.sources[sidx].fillstyle  , self.alist.get("fillstyle"  ))
			linestyle   = lib.argsWin(1          , self.sources[sidx].linestyle  , self.alist.get("linestyle"  ))
			linewidth   = lib.argsWin(2          , self.sources[sidx].linestyle  , self.alist.get("linewidth"  ))
			markerstyle = lib.argsWin(8          , self.sources[sidx].markerstyle, self.alist.get("markerstyle"))
			markersize  = lib.argsWin(1.8        , self.sources[sidx].markerstyle, self.alist.get("markersize" ))

			for cidx in range(len(self.h[sidx])):
				self.h[sidx][cidx].SetMaximum(0.7)
				self.h[sidx][cidx].SetMinimum(0.0)
				self.h[sidx][cidx].SetFillColor(color)
				self.h[sidx][cidx].SetFillStyle(fillstyle)
				self.h[sidx][cidx].SetLineColor(color)
				self.h[sidx][cidx].SetLineStyle(linestyle)
				self.h[sidx][cidx].SetLineWidth(2)
				self.h[sidx][cidx].SetMarkerColor(color)
				self.h[sidx][cidx].SetMarkerStyle(markerstyle)
				self.h[sidx][cidx].SetMarkerSize(1.8)


	## build
	##---------------------------------------------------------------
	def build(self, setsources, setcategs):

		self.sources = [source.source(self.mypaf, s) for s in setsources]
		self.categs  = setcategs
		self.h       = []

		for s in self.sources:
			appender = []
			for c in self.categs:
				hc = copy.deepcopy(self.parent)
				hc.SetName(s.name + ":=" + c + ":=" + self.var)
				appender.append(hc)

			self.h.append(appender)

		self.built = True	
		

	## check
	##---------------------------------------------------------------
	def check(self, dim):

		if not hasattr(self, "dim"): 
			self.dim = dim
		else: 
			if self.dim != dim: 
				self.vb.error("trying to re-initialize a histogram of wrong dimension")


	## detachArgs
	##---------------------------------------------------------------
	def detachArgs(self):
		## need to reset default status of canvas and pad after plotting

		self.detachGrid()
		self.detachLog()


	## detachGrid
	##---------------------------------------------------------------
	def detachGrid(self):
		self.mypaf.applyGrid()


	## detachLog	
	##---------------------------------------------------------------
	def detachLog(self):
		self.mypaf.applyLog()


	## divHist
	##---------------------------------------------------------------
	def divHist(self, hist, coeffs = [], error = ''):
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = 1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Divide(self.h[sidx][cidx], hist.getH(sidx, cidx), 1.0, coeff, error)


	## draw
	##---------------------------------------------------------------
	def draw(self, option = "", pad = 0):

		if option != "": option = " " + option

		self.prepareDraw()

		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				self.mypaf.pads[pad].cd()
				self.drawH(sidx, cidx, option)

		self.detachArgs()


	## drawArrow
	##---------------------------------------------------------------
	def drawArrow(self):
		## takes all drawarrow arguments and draws an arrows to the histogram
		## for all of them
		## format of drawlatex argument is x1,y1,x2,y2,strength,color

		if self.alist.has("drawarrow"):

			li = [l.split(",") for l in self.alist.getAll("drawarrow")]
			lx = []

			for ii, l in enumerate(li):
				lx.append(ROOT.Tlatex())
				lx[ii].SetTextAlign(int(l[2])) 
				lx[ii].SetTextFont (int(l[3]))
				lx[ii].SetTextSize (int(l[4]))
				lx[ii].SetTextColor(int(l[5]))
				lx[ii].DrawLatex(float(l[0]), float(l[1]), l[6].replace("_", " "))


	
	## drawBox
	##---------------------------------------------------------------
	def drawBox(self):

		if self.alist.has("drawbox"):
			print "draw a box"


	## drawCircle
	##---------------------------------------------------------------
	def drawCircle(self):
	
		if self.alist.has("drawcircle"):
			print "draw a circle"


	## drawErrorBand
	##---------------------------------------------------------------
	def drawErrorBand(self, sidx, cidx):

		if self.alist.has("errors")                           : errors = self.alist.get("errors")
		elif hasattr(self, "defaults") and self.defaults != []: errors = self.defaults[4]
		else                                                  : errors = "none"

		if errors == "band":
			hband = copy.deepcopy(self.h[sidx][cidx])
			hband.SetFillColor(ROOT.kGray)
			hband.SetFillStyle(3001)
			hband.SetLineColor(ROOT.kGray)
			#hband.Draw("e2 same")


	## drawH
	##---------------------------------------------------------------
	def drawH(self, sidx, cidx, option = "", direct = False):

		self.drawRange(sidx, cidx)
		self.h[sidx][cidx].Draw(self.d + option)
		if not direct:
			self.saveHist(sidx, cidx)
		if self.p:
			self.drawArrow()
			self.drawBox()
			self.drawCircle()
			self.drawErrorBand(sidx, cidx)
			self.drawLatex()
			self.drawLine()
			self.drawNote()
			if not direct:
				self.mypaf.saveCanv(self.var + "_" + self.sources[sidx].name + "_" + self.categs[cidx])


	## drawLabels
	##---------------------------------------------------------------
	def drawLabels(self):

		pad = ROOT.gPad
		factor = lib.getPadSize(pad)

		##print "drawing labels for " + self.var + " (" + str(self.labels) + ")"	
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

		if self.alist.has("drawlatex"):

			li = [l.split(",") for l in self.alist.getAll("drawlatex")]
			lx = []

			for ii, l in enumerate(li):
				lx.append(ROOT.Tlatex())
				lx[ii].SetTextAlign(int(l[2])) 
				lx[ii].SetTextFont (int(l[3]))
				lx[ii].SetTextSize (int(l[4]))
				lx[ii].SetTextColor(int(l[5]))
				lx[ii].DrawLatex(float(l[0]), float(l[1]), l[6].replace("_", " "))


	## drawLine
	##---------------------------------------------------------------
	def drawLine(self):

		if self.alist.has("drawline"):
			print "draw a line"


	## drawRange
	##---------------------------------------------------------------
	def drawRange(self, sidx, cidx):
	
		mm = self.getMinMax(self.h[sidx][cidx])

		#xmin, xmax = lib.getHistMinMax(mm[0][0], mm[0][1], self.hasLogScale("x"))
		#self.h[sidx][cidx].GetXaxis().SetRangeUser(xmin, xmax)

		if self.alist.has("ymin") and self.alist.has("ymax"):
			ymin = float(self.alist.get("ymin"))
			ymax = float(self.alist.get("ymax"))
		else: 
			ymin, ymax = lib.getHistMinMax(mm[1][0], mm[1][1], self.hasLogScale("y")) 
		self.h[sidx][cidx].GetYaxis().SetRangeUser(ymin, ymax)

		#if len(mm) > 4:
		#	zmin, zmax = lib.getHistMinMax(mm[2][0], mm[2][1], self.hasLogScale("z"))
		#	self.h[sidx][cidx].GetZaxis().SetRangeUser(zmin, zmax)


	## drawNote
	##---------------------------------------------------------------
	def drawNote(self):

		if self.alist.has("note")                             : note  = args.get("note")
		elif hasattr(self, "defaults") and self.defaults != []: note  = self.defaults[1]
		else                                                  : note  = "cms"

		if note == "cms":
			mcOnly = True
			rstuff.cms(self.mypaf.canvas, float(self.mypaf.input.cfg.getVar("luminosity")), float(self.mypaf.input.cfg.getVar("energy")), mcOnly)


	## fill
	##---------------------------------------------------------------
	def fill(self, sidx, cidx, value):
		self.h[sidx][cidx].fill(value)


	## getBinArgs
	##---------------------------------------------------------------
	def getBinArgs(self, dim = "x"):

		if self.alist.has("n" + dim + "bins") and self.args.has(dim + "bins"):
			eval("bins = [" + self.args.get(dim + "bins") + "]")
			return int(self.alist.get("n" + dim + "bins")), array.array('d', bins)

		if self.alist.has("n" + dim + "bins") and self.args.has(dim + "min") and self.args.has(dim + "max"):

			return int(self.alist.get("n" + dim + "bins")), lib.bins(int(self.alist.get("n" + dim + "bins")), float(self.alist.get(dim + "min")), float(self.alist.get(dim + "max")))

		return 0, []


	## getBins
	##---------------------------------------------------------------
	def getBins(self):

		bins = [clist.clist(list(self.parent.GetXaxis().GetXbins()))]
		if self.dim == 2:
			bins.append(clist.clist(list(self.parent.GetYaxis().GetXbins())))
		if self.dim == 3:
			bins.append(clist.clist(list(self.parent.GetZaxis().GetXbins())))

		return bins


	## getDim
	##---------------------------------------------------------------
	def getDim(self):
		return self.dim


	## getH
	##---------------------------------------------------------------
	def getH(self, sidx, cidx):
		return self.h[sidx][cidx]


	## getLName
	##---------------------------------------------------------------
	def getLName(self, sidx, cidx):
		return self.sources[sidx].lname


	## getMinMax
	##---------------------------------------------------------------
	def getMinMax(self, hist):

		mins = []
		maxs = []	
	
		mins.append(hist.GetXaxis().GetXmin())
		if self.dim >= 2:
			mins.append(hist.GetYaxis().GetXmin())
		else:	
			mins.append(hist.GetMinimum())
		if self.dim == 3:
			mins.append(hist.GetZaxis().GetXmin())
		else:
			mins.append(hist.GetMinimum())

		maxs.append(hist.GetXaxis().GetXmax())
		if self.dim >= 2:
			maxs.append(hist.GetYaxis().GetXmax())
		else:	
			maxs.append(hist.GetMaximum())
		if self.dim == 3:
			maxs.append(hist.GetZaxis().GetXmax())
		else:
			maxs.append(hist.GetMaximum())
	
		return [mins, maxs]


	## getParent
	##---------------------------------------------------------------
	def getParent(self):
		return self.parent


	## hasLogScale
	##---------------------------------------------------------------
	def hasLogScale(self, dim = "y"):

		if   dim == "x" and ROOT.gPad.GetLogx() == 1: return True
		elif dim == "y" and ROOT.gPad.GetLogy() == 1: return True
		elif dim == "z" and ROOT.gPad.GetLogz() == 1: return True

		return False


	## inject
	##---------------------------------------------------------------
	def inject(self, hist, sidx, cidx):

		self.check(hist.GetDimension())
		self.h[sidx][cidx].Add(hist) 


	## injectHist
	##---------------------------------------------------------------
	def injectHist(self, hist):

		self.check(hist.dim)
		if len(self.sources) == len(hist.sources) and len(self.categs) == len(hist.categs):
			for sidx in range(len(self.sources)):
				for cidx in range(len(self.categs)):
					self.h[sidx][cidx].Reset()
					self.h[sidx][cidx].Add(hist.getH(sidx, cidx))


	## loadInitial
	##---------------------------------------------------------------
	def loadInitial(self):

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
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = -1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Multiply(self.h[sidx][cidx], hist.getH(sidx, cidx), 1.0, coeff, error)


	## prepareDraw
	##---------------------------------------------------------------
	def prepareDraw(self):

		self.applyArgs()
		self.applySourceInfo()
		self.drawLabels()

	
	## rebin
	##---------------------------------------------------------------
	def rebin(self, hist, xbins, ybins = [], zbins = []):

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

		rebin = False
		if self.parent.GetXaxis().GetXbins() != hist.GetXaxis().GetXbins(): rebin = True
		if self.dim == 2 and \
		   self.parent.GetYaxis().GetXbins() != hist.GetYaxis().GetXbins(): rebin = True
		elif self.dim == 3 and \
		   self.parent.GetZaxis().GetXbins() != hist.GetZaxis().GetXbins(): rebin = True

		if rebin:
			hist = self.rebin(hist, list(self.parent.GetXaxis().GetXbins()), list(self.parent.GetYaxis().GetXbins()), list(self.parent.GetZaxis().GetXbins()))

		return hist


	## reinit
	##---------------------------------------------------------------
	def reinit(self, hist):
		## re-initialize this hist instance from another instance
		## this basically is a copy of the hist instance hist into this one

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

		self.alist.resetArgs(argstring)


	## saveHist
	##---------------------------------------------------------------
	def saveHist(self, sidx, cidx):

		self.h[sidx][cidx] = lib.saveHist(self.mypaf.output.file, self.h[sidx][cidx], self.sources[sidx].name + "/" + self.categs[cidx] + "/" + self.var)



	## setArgs
	##---------------------------------------------------------------
	def setArgs(self, argstring = ""):
		## old arguments are added to new ones

		self.alist.setArgs(argstring)


	## setBinContent
	##---------------------------------------------------------------
	def setBinContent(self, sidx, cidx, bin, value):
		self.h[sidx][cidx].SetBinContent(bin, value)


	## setD
	##---------------------------------------------------------------
	def setD(self):
	
		self.d = ""
	
		if self.dim == 1:
			if self.alist.has("draw1mode"): self.d = self.alist.get("draw1mode")
			else                          : self.d = "hist"
	
		elif self.dim == 2:
			if self.alist.has("draw2mode"): self.d = self.alist.get("draw2mode")
			else                          : self.d = "colz text e"
	
		elif self.dim == 3:
			if self.alist.has("draw3mode"): self.d = self.alist.get("draw3mode")
			else                          : self.d = "iso"


	## setInitial
	##---------------------------------------------------------------
	def setInitial(self):

		self.i_argstring = self.alist.argstring
		self.i_ints      = []

		for sidx in range(len(self.h)):
			self.i_ints.append([self.h[sidx][cidx].Integral() for cidx in range(len(self.h[0]))])


	## setLabels
	##---------------------------------------------------------------
	def setLabels(self, labels):

		self.labels = labels
		if   self.dim == 1 and len(self.labels[1]) > 4 and self.labels[1][-4:] != "/bin": self.labels[1] += "/bin"
		##elif self.dim == 2 and len(self.labels[2]) > 4 and self.labels[2][-4:] != "/bin": self.labels[2] += "/bin"
		## no label for color axis?
	

	## setP
	##---------------------------------------------------------------
	def setP(self, pvalue = False):
	
		self.p = pvalue


	## setParent
	##---------------------------------------------------------------
	def setParent(self):
		## creates the parent histogram

		binargs = self.binargs
		self.parent = None
	
		## 1d histogram
		if   len(binargs) == 1:
			self.check(1)
			nxbins, xbins = self.getBinArgs("x")
			if nxbins == 0: 
				xbins = array.array('d', binargs[0].list)
				nxbins = int(binargs[0].len) - 1
			self.parent = ROOT.TH1F(self.var, "", nxbins, xbins)

		## 1d histogram
		elif len(binargs) == 3: 
			self.check(1)
			nxbins, xbins = self.getBinArgs("x")
			if nxbins == 0: 
				nxbins = int(binargs[0])
				xbins = lib.bins(nxbins, binargs[1], binargs[2])
			self.parent = ROOT.TH1F(self.var, "", nxbins, xbins)

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
			self.parent = ROOT.TH2F(self.var, "", nxbins, xbins, nybins, ybins)

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
			self.parent = ROOT.TH2F(self.var, "", nxbins, xbins, nybins, ybins)

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
			self.parent = ROOT.TH3F(self.var, "", nxbins, xbins, nybins, ybins, nzbins, zbins)

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
			self.parent = ROOT.TH3F(self.var, "", nxbins, xbins, nybins, ybins, nzbins, zbins)

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
		self.check(hist.dim)
		for sidx in range(len(self.h)):
			for cidx in range(len(self.h[0])):
				coeff = -1.0
				if coeffs != []: coeff = coeffs[sidx][cidx]
				self.h[sidx][cidx].Add(hist.getH(sidx, cidx), coeff)

