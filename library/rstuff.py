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
def cms(canv, lumi, energy, mcOnly = False):

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
			lx.DrawLatex(0.89, 0.88 * f, "#sqrt{s} = %.0f TeV, L_{int} = %.0f pb^{-1}" % (energy, lumi)) 

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


## legend
##---------------------------------------------------------------
def legend(hists, lnames, styles):

	if hists[0].GetDimension() != 1: return
	if len(hists) != len(lnames): return

	pad = ROOT.gPad
	factor = lib.getPadSize(pad)

	y2 = 0.83
	y1 = y2 - 0.08 * len(lnames)
	dx = (1.0-pad.GetWNDC()) / 2 + pad.GetWNDC()
	dy = (1.0-pad.GetHNDC()) / 2 + pad.GetHNDC()
	l = ROOT.TLegend(0.47 * dx, y1 * dy, 0.87 * dx, y2 * dy)
	l.SetFillColor(ROOT.kWhite)
	l.SetTextFont(42)
	l.SetBorderSize(0)
	l.SetMargin(0.23)
	l.SetTextSize(0.045 / factor)

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
def line(x1 = 0.0, y1 = 0.0, x2 = 1.0, y2 = 1.0, width = 2, style = 7, color = ROOT.kBlack):

	line = ROOT.TLine(x1, y1, x2, y2)
	line = lineStyle(line, width, style, color)
	line.Draw("same")
	return line


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
def ratiopad(name = 'pr', x1 = 0.0, y1 = 0.0, x2 = 1.0, y2 = 0.28):

	area = (x2-x1)*(y2-y1)
	return pad(name, x1, y1, x2, y2, 0.14/area, 0.11, 0.11, 0.0)


## setRatioStyle
##---------------------------------------------------------------
def setRatioStyle(hist, name1, name2, xlabel):

	hmin, hmax = lib.getHistMinMax(hist.GetMinimum(0.0), hist.GetMaximum(), False)
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
	#hist.GetYaxis().SetTitleOffset(factor)
	hist.GetYaxis().SetTitleOffset(factor)
	hist.GetYaxis().SetRangeUser(hmin * 0.9, hmax * 1.1)

	hist.GetXaxis().SetNdivisions(505)
	hist.GetXaxis().SetTitle(xlabel)
	hist.GetXaxis().SetLabelSize(0.045 / factor)
	hist.GetXaxis().SetTitleSize(0.045 / factor)
	hist.GetXaxis().SetTitleOffset(1.0 + factor / 2)

	return hist



