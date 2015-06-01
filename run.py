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
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.TGaxis.SetMaxDigits(3)


## arguments

args = [arg for i, arg in enumerate(sys.argv) if i > 0]
if len(args) != 2:
	print "mypaf needs two arguments to run! (module and config file)"
	sys.exit(0)


## initialize classes

mypaf = mypaf.mypaf(args[0], args[1])
mypaf.run()
mypaf.finalize()
mypaf.save()
mypaf.close()






