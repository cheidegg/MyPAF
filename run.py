#################################################################
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

import ROOT, sys
from library import mypaf

ROOT.gErrorIgnoreLevel = 3000
ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.gStyle.SetOptStat(111100)
ROOT.gStyle.SetStatX(0.35)
ROOT.gStyle.SetStatY(0.82)

#ROOT.gStyle.SetOptStat(0)
#ROOT.TGaxis.SetMaxDigits(3)
#ROOT.TGaxis.SetMaxDigits(10)


## arguments

args = [arg for i, arg in enumerate(sys.argv) if i > 0]
if len(args) < 2:
	print "mypaf needs two arguments to run! (module and config file)"
	sys.exit(0)
if len(args) == 2:
	args.append("")

## initialize instance and run

mypaf = mypaf.mypaf(args[0], args[1], args[2])
mypaf.run()
mypaf.finalize()
mypaf.save()
mypaf.close()






