import ROOT, array, os

lsdir = os.listdir("/Users/conni/Computing/MyPAF/temp")
print lsdir


vint = 2
vfloat = 3.
string = "string"

print type(vint) is int
print type(vfloat) is float
print type(string) is str


#class destClass:
#
#	def __init__(self, name):
#		print "init instance " + name + " of destClass"
#		self.name = name
#
#class origClass:
#
#	def __init__(self, oname):
#		print "init instance " + oname + " of origClass"
#		self.oname = oname
#		self.var1 = 1
#		self.var2 = 2
#		self.var3 = 3
#
#oc = origClass("myFancyTest")
#dc = destClass("myDestTest")
#print hasattr(oc, "var1")
#print hasattr(dc, "var1")
#print [k for k,v in dc.__dict__.items()]
#
#dc.__dict__.update(oc.__dict__)
#print oc.var1
#print dc.var1
#oc.var1 = 3
#dc.var1 = 5
#print oc.var1
#print dc.var1

#f = ROOT.TFile("input/tree/WJetsincl.root", "r")
#t = f.Get("tree")
#
#for i, evt in enumerate(t):
#
#	branch = getattr(evt, "LepGood_pt")
#	print len(branch)
#
#	if i == 50: break



#def checkUniformity(bins):
#
#	d = bins[1] - bins[0]
#	if any([bins[i]-bins[i-1]-d for i in range(2,len(bins))]):
#		return False
#
#	return True
#
#
#print checkUniformity([10, 20, 30, 40, 50, 60, 70])
#print checkUniformity([10, 20, 25, 35, 45, 55, 65])


#ta = array.array('d', [5, 6, 7, 8])
#print list(ta)
#
#mystring = "[4, 6, 8]"
#
#ar = eval(mystring)
#print ar
#print len(ar)

#print ROOT.kBlue+2
#print 602
##eval("print ROOT.kBlue")
#var = eval("ROOT.kBlue+2")
#print var
#
#mystring = "events/bin"
#print mystring[-4:]
#
#
#h0 = ROOT.TH1F("h0", "h0", 10, 0, 10)
#h0.SetBinContent(1, 20)
#h0.SetBinContent(2, 40)
#
#h1 = ROOT.TH1F("h1", "h1", 10, 0, 10)
#h1.SetBinContent(2, 5)
#
#h2 = ROOT.TH1F("h2", "h2", 10, 0, 10)
#h2.SetBinContent(1, 5)
#h2.SetBinContent(2, 13)
#
#x = ROOT.RooRealVar("x", "x", h0.GetXaxis().GetXmin(), h0.GetXaxis().GetXmax())
#list = ROOT.RooArgList(x)
#set  = ROOT.RooArgSet(x)
#
#h0RDH  = ROOT.RooDataHist("data", "data", list, h0)
#h1RDH  = ROOT.RooDataHist("mc1" , "mc1" , list, h1)
#h2RDH  = ROOT.RooDataHist("mc2" , "mc2" , list, h2)
#
#hBPDF  = ROOT.RooHistPdf("mc1pdf", "mc1pdf", set, h1RDH)
#hCPDF  = ROOT.RooHistPdf("mc2pdf", "mc2pdf", set, h2RDH)
#
#scB    = ROOT.RooRealVar("mc1sc", "mc1sc", 0.5, 0.0, 1.0)
#scC    = ROOT.RooRealVar("mc2sc", "mc2sc", 0.5, 0.0, 1.0)
#
#pdfs   = ROOT.RooArgList(hBPDF, hCPDF)
#coeffs = ROOT.RooArgList(scB, scC)
#
#totPdf = ROOT.RooAddPdf("totPdf", "totPdf", pdfs, coeffs)
#
#result = totPdf.fitTo(h0RDH, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.Extended(), ROOT.RooFit.PrintLevel(-1))
#
#print coeffs[0].getVal() * h1.Integral() / h0.Integral()
#print coeffs[1].getVal() * h2.Integral() / h0.Integral()



#c = ROOT.TCanvas("c", "c", 975, 600)
#
#p = ROOT.TPad("p", "p", 0.0, 0.0, 1.0, 1.0, ROOT.kWhite, 0, 0)
#ROOT.SetOwnership(p, False)
#p.Draw()
#c.Update()
#
#p.cd()
#h = ROOT.TH1F("h", "h", 10, 0, 10)
#
#
##p.cd()
#h.SetBinContent(1, 10)
#h.SetBinContent(2, 50)
#h.Draw("hist")
#
##print ROOT.gPad()
##c.cd(1)
#p.SetLogy(1)
##c.Draw()
#c.SaveAs("test.png")
#
#c.Clear()
#del p
#p1 = ROOT.TPad("p", "p", 0.0, 0.3, 1.0, 1.0, ROOT.kWhite, 0, 0)
#p2 = ROOT.TPad("pr", "pr", 0.0, 0.0, 1.0, 3.0, ROOT.kWhite, 0, 0)
#p1.Draw()
#p2.Draw()
#c.Update()
#p1.cd()
#
#h1 = ROOT.TH1F("h", "h", 10, 0, 10)
#h.SetBinContent(1, 30)
#h.SetBinContent(2, 20)
#h.Draw("hist")
#p1.SetLogy(1)
#c.SaveAs("test2.png")



#f = ROOT.TFile("test.root", "recreate")
#
#if f.GetDirectory("sample") == None: print "none"
#f.mkdir("sample")
#if f.GetDirectory("sample") != None: print "not none"
#f.cd("sample")
#f.mkdir("sample/selection")
#f.Write()
#f.Close()

### getElmVar
###---------------------------------------------------------------
#def getElmVar(matrix, elm, variable, idx):
#
#	for row in matrix:
#		if row[elm] == variable:
#			return row[idx]
#	return None
#
#
#inputs=[["thisisthefilename", "thisisthefilepath", "args"], ["anotherfilename", "anotherfilepath", "args2"]]
#definition="FILE[thisisthefilename]::directory/histogram"
#
#sdef = definition.split("::")
#fname = sdef[0][5:-1]
#print fname
#fpath = getElmVar(inputs, 0, fname, 1)
#print fpath

#f = ROOT.TFile("input/tree/WJetsincl.root", "read")
#t = f.Get("tree")
#
#branch = t.GetBranch("run")
#print branch.GetLeaf("run").GetTypeName()
#print t.GetBranch("LepGood_pt").GetLeaf("LepGood_pt").GetTypeName()
#print t.GetListOfBranches()[0].GetName()
#print t.GetListOfLeaves()[0].GetName()
