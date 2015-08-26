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

import ROOT, copy, pdb
import args, hist, hscheme, lib, rstuff, styleargs


## run 
##---------------------------------------------------------------
def run(scheme, name, schemes = [], alist = args.args("")):

	if   scheme == "add"   : return add   (name, schemes, alist)
	elif scheme == "bins"  : return bins  (name, schemes, alist)
	elif scheme == "card"  : return card  (name, schemes, alist)
	elif scheme == "comp"  : return comp  (name, schemes, alist)
	#elif scheme == "datamc": return datamc(name, schemes[0].getHist(), [s.getHist() for s in schemes[1:]])
	elif scheme == "div"   : return div   (name, schemes, alist)
	elif scheme == "ffit"  : return ffit  (name, schemes, alist)
	elif scheme == "mult"  : return mult  (name, schemes, alist)
	elif scheme == "pack"  : return pack  (name, schemes, alist)
	elif scheme == "proj"  : return proj  (name, schemes, alist)
	#elif scheme == "roc"   : return roc   ()
	elif scheme == "stack" : return stack (name, schemes, alist)
	elif scheme == "sub"   : return sub   (name, schemes, alist)
	elif scheme == "tfit"  : return tfit  (name, schemes, alist)

	


## add
##---------------------------------------------------------------
def add(name, schemes, alist):

	schemes[0].mypaf.divideCanv(1, 1, False)

	## need to fix the coeffs
	if len(schemes) > 1:
		h1 = hist.hist(schemes[0].mypaf, name, schemes[0].getHist().getDim(), schemes[0].getHist().alist.argstring)
		h1.reinit(schemes[0].getHist())
		h1.injectHist(schemes[0].getHist())
		h1.setArgs(alist.argstring)
		for i in range(1,len(schemes)):
			h1.addHist(schemes[i].getHist())

	return h1


## comp
##---------------------------------------------------------------
def comp(name, schemes, alist):
	## compares two or more histograms with each other

	## we need 1 plot pad + 1 ratio pad
	if alist.has("ratio") and alist.get("ratio") == "y":
		schemes[0].mypaf.divideCanv(1, 1, True)
	else:
		schemes[0].mypaf.divideCanv(1, 1, False)

	## what to compare? schemes (histograms between schemes), sources (inside every scheme), categs (inside every scheme)
	comp = lib.useVal("schemes", alist.get("comp"))

	## for the drawing stuff, legend, etc. we need an empty histogram
	## that we draw on top of everything 
	h1 = hist.hist(schemes[0].mypaf, name, schemes[0].getHist().getDim(), alist.argstring)
	h1.reinit(schemes[0].getHist())

	a = []
	for scheme in schemes:
		a.append(scheme.getHist().alist.argstring)
		#scheme.getHist().resetArgs(alist.argstring)
		#scheme.getHist().applyArgs()

	h = []
	l = []
	d = []

	al = [alist.get("name" + str(i+1)) for i in range(len(schemes))]

	## compare sources per scheme and categ
	if comp == "sources":
		for i, scheme in enumerate(schemes):
			h.append([])
			l.append([])
			d.append([])
			for cidx in range(len(scheme.getHist().categs)):
				h[i].append([scheme.getHist()                       for sidx in range(len(scheme.getHist().sources))])
				l[i].append([scheme.getHist().getLNames(sidx, cidx) for sidx in range(len(scheme.getHist().sources))])
				d[i].append([sidx, cidx]                                                                             )

	## compare categs per scheme and source
	elif comp == "categs":
		for i, scheme in enumerate(schemes):
			h.append([])
			l.append([])
			d.append([])
			for sidx in range(len(scheme.getHist().sources)):
				h[i].append([scheme.getHist()                       for cidx in range(len(scheme.getHist().categs))])
				l[i].append([scheme.getHist().categs[cidx]          for cidx in range(len(scheme.getHist().categs))])
				d[i].append([sidx, cidx]                                                                            )

	## compare schemes per source and categ
	else:
		for sidx in range(len(schemes[0].getHist().sources)):
			h.append([])
			l.append([])
			d.append([])
			for cidx in range(len(schemes[0].getHist().categs)):
				h[sidx].append([scheme.getHist()                    for scheme in schemes])
				l[sidx].append([al[i] if al[i] is not "" else scheme.name for i, scheme in enumerate(schemes)])
				d[sidx].append([sidx, cidx]                                               )

	
	## do the loop
	for i, hrow in enumerate(h):
		for j, hline in enumerate(hrow):

			## main plot
			schemes[0].mypaf.pads[0].cd()
			hratio = rstuff.copyTH1F(hline[0].getH(d[i][j][0], d[i][j][1]))

			for k in range(len(hline)):
				hline[k].alist.reinit(alist)

			# draw scheme 2
			sa = styleargs.styleargs(alist.get("style"), "2", lib.useVal("ROOT.kBlack", alist.get("color2")))
			sa.set("labelsizex", "0")
			hline[1].alist.setArgs(sa.alist.argstring)
			hline[1].drawSingle(d[i][j][0], d[i][j][1], 0, "", False, False)

			# draw schemes > 2
			for k in range(2, len(hline)):
				sa.reinit(alist.get("style"), str(k+1), lib.useVal("ROOT.kBlack", alist.get("color" + str(k+1))))
				sa.set("labelsizex", "0")
				hline[k].alist.setArgs(sa.alist.argstring)
				hline[k].drawSingle(d[i][j][0], d[i][j][1], 0, "same", False, False)

			# draw scheme 1
			sa.reinit(alist.get("style"), "1", lib.useVal("ROOT.kBlack", alist.get("color1")))
			sa.set("labelsizex", "0" )
			sa.set("draw1mode" , "pe")
			hline[0].alist.setArgs(sa.alist.argstring)
			hline[0].runPreDraw(0)
			hline[0].drawH(d[i][j][0], d[i][j][1], 0, "same", False, False)
			# do not drawSingle as it resets global style


			sc = [0 for h in hline]
			if hline[0].getH(d[i][j][0], d[i][j][1]).Integral() > 0:
				sc = [round(h.getH(d[i][j][0], d[i][j][1]).Integral() / hline[0].getH(d[i][j][0], d[i][j][1]).Integral() * 100,1) for h in hline]
			lnames = l[i][j]
			if alist.has("sce2"):
				lnames = [l[i][j][0]]
				for li, ll in enumerate(l[i][j][1:]):
					if h.alist.has("sce" + str(li+1)): 
						add = " (" + str(sc[li+1]) + "% +/- " + str(round(100 * float(h.alist.get("sce" + str(li+1))),1) * sc[li+1]) + "%)"
					else: 
						add = ""
					lnames.append(ll + add)
			leg = rstuff.legend([h.getH(d[i][j][0], d[i][j][1]) for h in hline], lnames, [h.d for h in hline])
			leg.Draw("same")
			
			# ratio plot
			if alist.has("ratio") and alist.get("ratio") == "y":
				schemes[0].mypaf.pads[1].cd()
				schemes[0].mypaf.pads[1].SetLogy(0)

				hratio.Divide(hline[1].getH(d[i][j][0], d[i][j][1]))
				hratio = rstuff.setRatioStyle(hratio, l[i][j][0], l[i][j][1], hline[0].labels[0], alist)
				hratio.SetStats(0)
				hratio.Draw("pe")

				line = rstuff.line()
				line.DrawLine(hratio.GetXaxis().GetXmin(), 1.00, hratio.GetXaxis().GetXmax(), 1.00)
				#fit  = rstuff.fit(hratio, "line")
				#fit  = rstuff.lineStyle(fit, 2, 1, ROOT.kRed+1)
				#fit.Draw("l")

			## draw style stuff
			schemes[0].mypaf.saveCanv(name + "_" + schemes[0].getHist().sources[d[i][j][0]].name + "_" + schemes[0].getHist().categs[d[i][j][1]])
			del hratio	
	
	for i, scheme in enumerate(schemes):
		scheme.getHist().alist.resetArgs(a[i])

	return h1


## div
##---------------------------------------------------------------
def div(name, schemes, alist):

	schemes[0].mypaf.divideCanv(1, 1, False)

	## need to fix the coeffs
	if len(schemes) > 1:
		h1 = hist.hist(schemes[0].mypaf, name, schemes[0].getHist().getDim(), schemes[0].getHist().alist.argstring)
		h1.reinit(schemes[0].getHist())
		h1.injectHist(schemes[0].getHist())
		h1.setArgs(alist.argstring)
		for i in range(1,len(schemes)):
			h1.divHist(schemes[i].getHist(), [], alist.get("error"))
	return h1


## ffit
##---------------------------------------------------------------
def ffit(name, schemes, alist):
	## ffit: fit one or more functions to a histogram

	if schemes[0].getHist.getH(0, 0).Integral() == 0: 
		return False

	## we need 1 plot pad + 1 ratio pad
	if alist.has("ratio") and alist.get("ratio") == "y":
		schemes[0].mypaf.divideCanv(1, 1, True)
	else:
		schemes[0].mypaf.divideCanv(1, 1, False)

	return True


## filter
##---------------------------------------------------------------
def filter(name, schemes, alist):

	if len(schemes) == 1 and alist.has("cut"):
		h1 = hist.hist(schemes[0].mypaf, name, schemes[0].getHist().binargs, "")
		h1.reinit(schemes[0].getHist())
		h1.injectHist(schemes[0].getHist())
		h1.setArgs(alist.argstring)
		for sidx in range(len(h1.schemes)):
			for cidx in range(len(h1.categs)):
				for i in range(1,h1.getH(sidx, cidx).GetNbins()):
					if not eval("h1.getH(sidx, cidx).GetBinContent(" + i + ") " + alist.get("cut")):
						h1.getH(sidx, cidx).SetBinContent(i, 0)
		return h1


## mult
##---------------------------------------------------------------
def mult(name, schemes, alist):

	schemes[0].mypaf.divideCanv(1, 1, False)

	## need to fix the coeffs
	if len(schemes) > 1:
		h1 = hist.hist(schemes[0].mypaf, name, schemes[0].getHist().getDim(), schemes[0].getHist().alist.argstring)
		h1.reinit(schemes[0].getHist())
		h1.injectHist(schemes[0].getHist())
		h1.setArgs(alist.argstring)
		for i in range(1,len(schemes)):
			h1.divHist(schemes[i].getHist(), [], alist.get("error"))
	return h1


## proj
##---------------------------------------------------------------
def proj(name, schemes, alist):

	dim = "x"
	if alist.has("dim"):
		dim = alist.get("dim")

	h1 = hist.hist(schemes[0].getHist().mypaf, name)
	h1.inject(schemes[0].getHist().getProj("x"))
	
	return h1


## sub
##---------------------------------------------------------------
def sub(name, schemes, alist):

	schemes[0].mypaf.divideCanv(1, 1, False)

	## need to fix the coeffs
	if len(schemes) > 1:
		h1 = hist.hist(schemes[0].mypaf, name, schemes[0].getHist().getDim(), schemes[0].getHist().alist.argstring)
		h1.reinit(schemes[0].getHist())
		h1.injectHist(schemes[0].getHist())
		h1.setArgs(alist.argstring)
		for i in range(1,len(schemes)):
			h1.subHist(schemes[i].getHist())
	return h1


## stack
##---------------------------------------------------------------
def stack(name, schemes, alist):


	if hlist == []: return hlist

	return True


## tfit
##---------------------------------------------------------------
def tfit(name, schemes, alist):

	if schemes[0].getHist().getH(0, 0).Integral() == 0: return

	if len(schemes) > 10: maxs = 10
	else                : maxs = len(schemes)

	## init a trivial scheme for total fit
	h1 = hist.hist(schemes[0].mypaf, name + "_tfit", schemes[0].getHist().binargs, schemes[0].getHist().labels, schemes[1].getHist().alist.argstring)
	h1.alist.resetArgs(alist.argstring)
	setsources = [alist.get("source") for s in schemes[0].getHist().sources]
	alist.remove("source")
	if setsources=="": setsource = [s.name for s in schemes[0].getHist().sources]
	h1.build(setsources, schemes[0].getHist().categs)
	h1.applyArgs()
	h1.applySourceInfo()
	s1 = hscheme.hscheme(schemes[0].mypaf, "hist", name + "_tfit", "", alist.argstring)
	s1.setTrivial(h1)

	## do the fit for every sidx/cidx pair
	x = ROOT.RooRealVar("xx", "xx", schemes[0].getHist().getH(0,0).GetXaxis().GetXmin(), schemes[0].getHist().getH(0,0).GetXaxis().GetXmax())
	list = ROOT.RooArgList(x)
	set  = ROOT.RooArgSet(x)

	for sidx in range(len(schemes[0].getHist().sources)):
		for cidx in range(len(schemes[0].getHist().categs)):

			data = ROOT.RooDataHist("data", "data", list, schemes[0].getHist().getH(sidx, cidx))
			dint = schemes[0].getHist().getH(sidx, cidx).Integral()

			mcint = sum([schemes[i].getHist().getH(sidx, cidx).Integral() for i in range(1,len(schemes))])
			if mcint > dint:
				for i in range(1,len(schemes)):
					schemes[i].getHist().getH(sidx, cidx).Scale(dint/mcint)

			dh = []
			hi = []
			mc = []
			sc = []
			for i in range(1,len(schemes)):
				dh.append(ROOT.RooDataHist("mc" + str(i), "mc" + str(i), list, schemes[i].getHist().getH(sidx, cidx)))
				hi.append(schemes[i].getHist().getH(sidx, cidx).Integral())
				mc.append(ROOT.RooHistPdf("mcpdf" + str(i), "mcpdf" + str(i), set, dh[i-1]))
				sc.append(ROOT.RooRealVar("mcscale" + str(i), "mcscale" + str(i), hi[i-1]/dint, 0.0, 1.0))
			
			pdfs   = eval("ROOT.RooArgList(" + ", ".join(["mc[" + str(i) + "]" for i in range(len(mc))]) + ")")
			coeffs = eval("ROOT.RooArgList(" + ", ".join(["sc[" + str(i) + "]" for i in range(len(sc))]) + ")")

			totPdf = ROOT.RooAddPdf("totPdf", "totPdf", pdfs, coeffs)

			result = totPdf.fitTo(data, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.Extended(), ROOT.RooFit.PrintLevel(-1)) 

			## scale mc hists accordingly
			value = []
			syerr = []
			alerr = []
			auerr = []
			for i in range(1,len(schemes)):
				value.append(sc[i-1].getVal())
				syerr.append(sc[i-1].getError())
				alerr.append(sc[i-1].getAsymErrorLo())
				auerr.append(sc[i-1].getAsymErrorHi())
				schemes[i].getHist().getH(sidx, cidx).Scale(value[i-1])
				alist.set("sce" + str(i+1), str(sc[i-1].getError() / sc[i-1].getVal()))

			## ignore asymm errors??

			## delete params
			for i in range(len(mc)):
				mc[i].Delete()
				sc[i].Delete()
			data.Delete(), pdfs.Delete(), coeffs.Delete()
			del data, mc, sc, hi, pdfs, coeffs

			## write total fit hist
			h1.getH(sidx, cidx).SetLineColor(ROOT.kRed)
			for i in range(1,len(schemes)):
				h1.inject(schemes[i].getHist().getH(sidx, cidx), sidx, cidx)

	## plot everything
	ns = [schemes[0], s1]
	ns.extend(schemes[1:])
	alist.set("ratio", "y")
	comp(name, ns, alist)


