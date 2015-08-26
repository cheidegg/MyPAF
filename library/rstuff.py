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
import lib


## canv
##---------------------------------------------------------------
def canv(width = 975, height = 700, name = "c"):

	canvas = ROOT.TCanvas("c", "c", 975, 700)
	canvas.SetBottomMargin(0.12)
	canvas.SetLeftMargin(0.12)
	canvas.SetRightMargin(0.12)
	canvas.SetTopMargin(0.09)

	return canvas


## cms
##---------------------------------------------------------------
def cms(canv, lumi, energy, mcOnly = False, remarks = ""):

	#canv.cd()
	pad = ROOT.gPad
	factor = lib.getPadSize(pad)
	f = 1 - (1. - factor)/5

	ts = 0.75 * canv.GetTopMargin() / factor 
	lx = ROOT.TLatex()
	lx.SetTextSize(ts)
	lx.SetNDC() 

	lx.SetName("LxLumi")

	#if fullCanv: lumix = 0.922
	#else:        lumix = 0.965

	## lumi and energy
	if lumi > 0.:
		lx.SetTextFont(42)
		lx.SetTextAlign(31)
		lx.SetTextSize(0.6*ts)

		if lumi > 1000.:
			lx.DrawLatex(0.89, 0.88 * f, "#sqrt{s} = %.0f TeV, L_{int} = %.1f fb^{-1}" % (energy, lumi/1000.))
		else:
			lx.DrawLatex(0.89, 0.88 * f, "#sqrt{s} = %.0f TeV, L_{int} = %.1f pb^{-1}" % (energy, lumi)) 

	return
	## need to reconsider!

	## CMS
	lx.SetTextAlign(31)
	lx.SetTextFont(61)
	lx.SetTextSize(ts)
	lx.DrawLatex(0.84, 0.73, "CMS")

	## Simulation or Preliminary
	lx.SetTextFont(52);
	lx.SetTextSize(0.76*ts);

	if mcOnly:
		lx.DrawLatex(0.84, 0.68, "Simulation")
	else:
		lx.DrawLatex(0.84, 0.68, "Preliminary")


## copyStyle
##---------------------------------------------------------------
def copyStyle(copy, hist):

	#copy.SetBarOffset  (hist.SetBarOffset  ())
	#copy.SetBarWidth   (hist.SetBarWidth   ())
	copy.SetFillColor  (hist.GetFillColor  ())
	copy.SetFillStyle  (hist.GetFillStyle  ())
	copy.SetLineColor  (hist.GetLineColor  ())
	copy.SetLineStyle  (hist.GetLineStyle  ())
	copy.SetLineWidth  (hist.GetLineWidth  ())
	copy.SetMarkerColor(hist.GetMarkerColor())
	copy.SetMarkerStyle(hist.GetMarkerStyle())
	copy.SetMarkerSize (hist.GetMarkerSize ())
	#copy.SetStats      (hist.GetStats      ())


	copy.GetXaxis().SetAxisColor  (hist.GetXaxis().GetAxisColor  ())
	copy.GetXaxis().SetLabelColor (hist.GetXaxis().GetLabelColor ())
	copy.GetXaxis().SetLabelFont  (hist.GetXaxis().GetLabelFont  ())
	copy.GetXaxis().SetLabelOffset(hist.GetXaxis().GetLabelOffset())
	copy.GetXaxis().SetLabelSize  (hist.GetXaxis().GetLabelSize  ())
	copy.GetXaxis().SetNdivisions (hist.GetXaxis().GetNdivisions ())
	copy.GetXaxis().SetTickLength (hist.GetXaxis().GetTickLength ())
	copy.GetXaxis().SetTitleColor (hist.GetXaxis().GetTitleColor ())
	copy.GetXaxis().SetTitleFont  (hist.GetXaxis().GetTitleFont  ())
	copy.GetXaxis().SetTitleOffset(hist.GetXaxis().GetTitleOffset())
	copy.GetXaxis().SetTitleSize  (hist.GetXaxis().GetTitleSize  ())

	copy.GetYaxis().SetAxisColor  (hist.GetYaxis().GetAxisColor  ())
	copy.GetYaxis().SetLabelColor (hist.GetYaxis().GetLabelColor ())
	copy.GetYaxis().SetLabelFont  (hist.GetYaxis().GetLabelFont  ())
	copy.GetYaxis().SetLabelOffset(hist.GetYaxis().GetLabelOffset())
	copy.GetYaxis().SetLabelSize  (hist.GetYaxis().GetLabelSize  ())
	copy.GetYaxis().SetNdivisions (hist.GetYaxis().GetNdivisions ())
	copy.GetYaxis().SetTickLength (hist.GetYaxis().GetTickLength ())
	copy.GetYaxis().SetTitleColor (hist.GetYaxis().GetTitleColor ())
	copy.GetYaxis().SetTitleFont  (hist.GetYaxis().GetTitleFont  ())
	copy.GetYaxis().SetTitleOffset(hist.GetYaxis().GetTitleOffset())
	copy.GetYaxis().SetTitleSize  (hist.GetYaxis().GetTitleSize  ())

	if hist.GetDimension() > 1:
		copy.GetZaxis().SetAxisColor  (hist.GetZaxis().GetAxisColor  ())
		copy.GetZaxis().SetLabelColor (hist.GetZaxis().GetLabelColor ())
		copy.GetZaxis().SetLabelFont  (hist.GetZaxis().GetLabelFont  ())
		copy.GetZaxis().SetLabelOffset(hist.GetZaxis().GetLabelOffset())
		copy.GetZaxis().SetLabelSize  (hist.GetZaxis().GetLabelSize  ())
		copy.GetZaxis().SetNdivisions (hist.GetZaxis().GetNdivisions ())
		copy.GetZaxis().SetTickLength (hist.GetZaxis().GetTickLength ())
		copy.GetZaxis().SetTitleColor (hist.GetZaxis().GetTitleColor ())
		copy.GetZaxis().SetTitleFont  (hist.GetZaxis().GetTitleFont  ())
		copy.GetZaxis().SetTitleOffset(hist.GetZaxis().GetTitleOffset())
		copy.GetZaxis().SetTitleSize  (hist.GetZaxis().GetTitleSize  ())

	return copy


## copyTH1
##---------------------------------------------------------------
def copyTH1(hist, name = ""):

	if name == "": name = hist.GetName() + "_copied"

	if hist.GetDimension() == 1: return copyTH1F(hist, name)
	if hist.GetDimension() == 2: return copyTH2F(hist, name)
	if hist.GetDimension() == 3: return copyTH3F(hist, name)

	return hist


## copyTH1F
##---------------------------------------------------------------
def copyTH1F(hist, name = ""):

	if name == "": name = hist.GetName() + "_copied"

	copy = ROOT.TH1F(name, hist.GetTitle(), hist.GetNbinsX(), hist.GetXaxis().GetXbins().GetArray())

	for bin in range(1,hist.GetNbinsX()+1):
		copy.SetBinContent(bin, hist.GetBinContent(bin))
		copy.SetBinError  (bin, hist.GetBinError  (bin))

	copy = copyStyle(copy, hist)

	return copy

 
## copyTH2F
##---------------------------------------------------------------
def copyTH2F(hist, name = ""):

	if name == "": name = hist.GetName() + "_copied"

	copy = ROOT.TH2F(name, hist.GetTitle(), hist.GetNbinsX(), hist.GetXaxis().GetXbins().GetArray(), hist.GetNbinsY(), hist.GetYaxis().GetXbins().GetArray())

	for xbin in range(1,hist.GetNbinsX()+1):
		for ybin in range(1,hist.GetNbinsY()+1):
			copy.SetBinContent(xbin, ybin, hist.GetBinContent(xbin, ybin))
			copy.SetBinError  (xbin, ybin, hist.GetBinError  (xbin, ybin))

	copy = copyStyle(copy, hist)

	return copy

 
## copyTH3F
##---------------------------------------------------------------
def copyTH3F(hist, name = ""):

	if name == "": name = hist.GetName() + "_copied"

	copy = ROOT.TH3F(name, hist.GetTitle(), hist.GetNbinsX(), hist.GetXaxis().GetXbins().GetArray(), hist.GetNbinsY(), hist.GetYaxis().GetXbins().GetArray(), hist.GetNbinsZ(), hist.GetZaxis().GetXbins().GetArray())

	for xbin in range(1,hist.GetNbinsX()+1):
		for ybin in range(1,hist.GetNbinsY()+1):
			for zbin in range(1,hist.GetNbinsZ()+1):
				copy.SetBinContent(xbin, ybin, zbin, hist.GetBinContent(xbin, ybin, zbin))
				copy.SetBinError  (xbin, ybin, zbin, hist.GetBinError  (xbin, ybin, zbin))

	copy = copyStyle(copy, hist)

	return copy


## fit
##---------------------------------------------------------------
def fit(hist, func = "", xmin = 0, xmax = 0):

	#func = ROOT.TF1("func","[0]*sin(x) + [1]*exp(-[2]*x)", 0, 2);
	print "fit"


## fitLine
##---------------------------------------------------------------
def fitLine(hist, xmin = 0, xmax = 0):

	print "fit line"
	#return fit(hist, )


## sumHists
def sumHists(hists):

	if len(hists) == 0: return None

	sum = copy.deepcopy(hists[0])
	for i in range(1,len(hists)):
		sum.Add(hists[i])

	return sum


## findLegendPosition
##---------------------------------------------------------------
def findLegendPosition(pad, hist, xsize, ysize):

	padX1 = pad.GetX1() 
	padX2 = pad.GetX2() 
	padY1 = pad.GetY1() 
	padY2 = pad.GetY2() 
	



	


## legend
##---------------------------------------------------------------
def legend(hists, lnames, hdmodes):

	if hists[0].GetDimension() != 1: return
	if len(hists) != len(lnames): return

	pad = ROOT.gPad
	factor = lib.getPadSize(pad)

	d = 0.05

	y2 = 0.83
	y1 = y2 - d * len(lnames)
	dy1 = 0.07
	dy2 = dy1 + d * len(lnames)
	dx = (1.0-pad.GetWNDC()) / 2 + pad.GetWNDC()
	dy = (1.0-pad.GetHNDC()) / 2 + pad.GetHNDC()
	#pos = findLegendPosition(pad, sumHists(hists), 0.2 * dx, dy2 - dy1)
	#l = ROOT.TLegend(0.15 * dx, dy1 * dy, 0.35 * dx, dy2 * dy)
	#l = ROOT.TLegend(0.25 * dx, dy1 * dy, 0.45 * dx, dy2 * dy)
	l = ROOT.TLegend(0.57 * dx, y1 * dy, 0.87 * dx, y2 * dy)
	l.SetFillColor(ROOT.kWhite)
	l.SetTextFont(42)
	l.SetBorderSize(0)
	l.SetMargin(0.23)
	l.SetTextSize(0.035 / factor)
	#l.SetTextSize(0.045 / factor)

	styles = []
	for i, d in enumerate(hdmodes):
		if   d.find("p") > -1                                    : styles.append("p")
		elif d.find("hist") > -1 and hists[i].GetFillStyle() != 0: styles.append("f")
		else                                                     : styles.append("l")

	for i in range(len(hists)):
		l.AddEntry(hists[i], lnames[i], styles[i])

	return l




	## adjust legend position is missing
	## below...

	#x1 = 0.
	#y1 = 0.
	#x2 = 0.
	#y2 = 0.

	#for i in range(1, hist.GetNbinsX()+1):
	#	x1 = hist.GetBinCenter(i) - hist.GetBinWidth(i)/2. 
	#
	#
	#   for(int i=0;i<h->GetNbinsX()+2;i++) { 
	#     out[0].push_back( h->GetBinCenter(i) - h->GetBinWidth(i)/2. ); 
	#     out[0].push_back( h->GetBinCenter(i) ); 
	#      
	#     out[1].push_back( max(h->GetBinContent(i), h->GetBinContent(i+1) ) ); 
	#     out[1].push_back( h->GetBinContent(i) ); 
	#     //cout<<i<<"   "<<h->GetBinCenter(i)<<"  "<<h->GetBinContent(i)<<endl; 
	#   } 


## line
##---------------------------------------------------------------
def line(width = 2, style = 7, color = ROOT.kBlack):

	line = ROOT.TLine()
	line = lineStyle(line, width, style, color)
	return line


### line
###---------------------------------------------------------------
#def line(x1 = 0.0, y1 = 0.0, x2 = 1.0, y2 = 1.0, width = 2, style = 7, color = ROOT.kBlack):
#
#	line = ROOT.TLine(x1, y1, x2, y2)
#	line = lineStyle(line, width, style, color)
#	#line.Draw()
#	#line.Draw("same")
#	return line


## lineStyle
##---------------------------------------------------------------
def lineStyle(line, width = 2, style = 1, color = ROOT.kBlack):

	line.SetLineWidth(width)
	line.SetLineStyle(style)
	line.SetLineColor(color)
	return line


## pad
##---------------------------------------------------------------
def pad(name = 'p', x1 = 0.0, y1 = 0.0, x2 = 1.0, y2 = 1.0, mbottom = 0.14, mleft = 0.11, mright = 0.11, mtop = 0.14):

	pad = ROOT.TPad(name, 'p', x1, y1, x2, y2, ROOT.kWhite, 0, 0)
	pad.SetBorderSize(0)
	pad.SetBottomMargin(mbottom)
	pad.SetLeftMargin(mleft)
	pad.SetTopMargin(mtop)
	pad.SetRightMargin(mright)
	pad.SetTicks(1,1)
	pad.Draw()
	ROOT.SetOwnership(pad, False) 

	return pad


## plotpad
##---------------------------------------------------------------
def plotpad(name = 'pp', x1 = 0.0, y1 = 0.32, x2 = 1.0, y2 = 1.0):

	area = (x2-x1)*(y2-y1)
	return pad(name, x1, y1, x2, y2, 0.0, 0.11, 0.11, 0.14/area)


## ratiopad
##---------------------------------------------------------------
def ratiopad(name = 'pr', x1 = 0.0, y1 = 0.0, x2 = 1.0, y2 = 0.30):

	area = (x2-x1)*(y2-y1)
	return pad(name, x1, y1, x2, y2, 0.14/area, 0.11, 0.11, 0.0)


## setRatioStyle
##---------------------------------------------------------------
def setRatioStyle(hist, name1, name2, xlabel, alist):

	hrange = lib.findHistRange(hist, "y", False)
	min = float(lib.useVal(str(hrange[0]), alist.get("rmin")))
	max = float(lib.useVal(str(hrange[1]), alist.get("rmax")))
	hist.GetYaxis().SetRangeUser(min, max)

	factor = lib.getPadSize(ROOT.gPad)

	hist.SetLineColor(ROOT.kBlack)
	hist.SetLineWidth(2)
	hist.SetLineStyle(1)
	hist.SetMarkerColor(ROOT.kBlack)
	hist.SetMarkerSize(1.6)
	hist.SetMarkerStyle(8)
	hist.SetFillStyle(0)
	hist.SetTitle('')

	hist.GetYaxis().SetNdivisions(105)
	hist.GetYaxis().SetTitle(name1 + "/" + name2)
	hist.GetYaxis().SetLabelSize(0.030 / factor)
	hist.GetYaxis().SetTitleSize(0.045 / factor)
	hist.GetYaxis().SetTitleOffset(factor*1.1)

	hist.GetXaxis().SetNdivisions(505)
	hist.GetXaxis().SetTitle(xlabel)
	hist.GetXaxis().SetLabelSize(0.045 / factor)
	hist.GetXaxis().SetTitleSize(0.045 / factor)
	hist.GetXaxis().SetTitleOffset(1.0 + factor / 2)

	return hist



