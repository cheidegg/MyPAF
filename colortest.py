import ROOT

col = [ROOT.kBlack,
       ROOT.kOrange+3,
       ROOT.kOrange+4,
       ROOT.kOrange+10,
       ROOT.kOrange+2,
       ROOT.kOrange+8,
       ROOT.kOrange-3,
 	   ROOT.kOrange+6,
       ROOT.kOrange-9,
       ROOT.kBlack]
#col = [ROOT.kBlack,
#       ROOT.kOrange+3, 
#       ROOT.kOrange+4, 
#       ROOT.kOrange+9, 
#       ROOT.kOrange+8, 
#       ROOT.kOrange+6,
#       ROOT.kOrange-9,
#       ROOT.kBlack,
#       ROOT.kBlack,
#       ROOT.kBlack]

# BACKGROUNDS
# blue:   ROOT.kBlue+4, ROOT.kBlue+3, ROOT.kBlue+2, ROOT.kBlue+1, ROOT.kBlue, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kBlue-10
# azure:  ROOT.kAzure+3, ROOT.kAzure-6, ROOT.kAzure+4, ROOT.kAzure+9, ROOT.kAzure+5, ROOT.kAzure+8, ROOT.kAzure+6, ROOT.kAzure-9
# green:  ROOT.kGreen+4, ROOT.kGreen+3, ROOT.kGreen+2, ROOT.kGreen+1, ROOT.kGreen, ROOT.kGreen-7, ROOT.kGreen-9, ROOT.kGreen-10
# red:    ROOT.kRed+4, ROOT.kRed+3, ROOT.kRed+2, ROOT.kRed+1, ROOT.kRed, ROOT.kRed-7, ROOT.kRed-9, ROOT.kRed-10 
# orange: ROOT.kOrange+3, ROOT.kOrange+4, ROOT.kOrange+10, ROOT.kOrange+2, ROOT.kOrange+8, ROOT.kOrange-3, ROOT.kOrange+6, ROOT.kOrange-9 
# yellow: ROOT.kYellow+4, ROOT.kYellow+3, ROOT.kYellow+2, ROOT.kYellow+1, ROOT.kYellow, ROOT.kYellow-7, ROOT.kYellow-9, ROOT.kYellow-10  

# SIGNALS
# cyan:    ROOT.kCyan+3, ROOT.kCyan+2, ROOT.kCyan+1, ROOT.kCyan, ROOT.kCyan-9, ROOT.kCyan-10 
# teal:
# spring:
# pink:
# magenta: ROOT.kMagenta+4, ROOT.kMagenta+3, ROOT.kMagenta+2, ROOT.kMagenta+1, ROOT.kMagenta, ROOT.kMagenta-7, ROOT.kMagenta-9, ROOT.kMagenta-10
# violet:

c = ROOT.TCanvas("c", "c", 975, 600)
h = [ROOT.TH1F("h" + str(i), "h" + str(i), 10, 0, 10) for i in range(10)]

for i in range(len(h)):
	h[i].SetBinContent(i+1, 10)
	h[i].SetFillColor(col[i])

h[0].Draw("hist")
for i in range(1,len(h)):
	h[i].Draw("hist same")
c.SaveAs("colortest.png")

