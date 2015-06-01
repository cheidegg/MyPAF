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
## collection of functions performing some parsing

import copy, ROOT
import cfg, dbreader, lib, mypaf


## access
##---------------------------------------------------------------
def access(mypaf, inputs, vidx, definition):

	definition = definition.strip()
	if len(definition) == 0: return None
	if definition.find("::") == -1: return None

	sdef = definition.split("::")
	source  = ""
	rescale = 1.0

	## source given
	if sdef[0][0:4] == "FILE" and len(sdef) == 3: source = sdef[2]
	if sdef[0][0:4] == "HIST" and len(sdef) == 4: source = sdef[3] 
	if source != "":
		attr = mypaf.db.getRow("samples", "name == '" + source + "'")
		if attr != []:
			rescale = float(mypaf.input.cfg.getVar("luminosity")) * float(eval(attr[4])) / float(eval(attr[6]))

	## access histogram in ROOT file
	if sdef[0][0:4] == "FILE":
		fname = sdef[0][5:-1]
		fpath = lib.getElmVar(inputs, vidx, fname, vidx+1) 
		return accessFile(fpath, sdef[1], rescale)

	## access histogram in canvas in ROOT file
	elif sdef[0][0:4] == "HIST":
		fname = sdef[0][5:-1]
		fpath = lib.getElmVar(inputs, vidx, fname, vidx+1) 
		return accessHist(fpath, sdef[1], sdef[2], rescale)

	return None



## accessFile
##---------------------------------------------------------------
def accessFile(path, variable, rescale = 1.0):

	if path.strip() != "":
		f = ROOT.TFile(path)
		h = copy.deepcopy(f.Get(variable))
		f.Close()
		h.Scale(rescale)
		return h
	return None


## accessHist
##---------------------------------------------------------------
def accessHist(path, canvas, variable, rescale = 1.0):

	if path.strip() != "":
		f = ROOT.TFile(path)
		c = f.Get(canvas)
		h = copy.deepcopy(c.GetPrimitive(variable))
		f.Close()
		h.Scale(rescale)
		return h
	return None


## getSelSteps
##---------------------------------------------------------------
def getSelSteps(selstring):

	result = [""]
	if selstring.strip() == "": return result

	## now split up the selection string in individual little strings
	## then add them together in a pyramid way, step1, step1+2, step1+2+3, etc.

	return result


## parse 
##---------------------------------------------------------------
def parse(collection, name, unparsed):
	## using elements from collection in parsing of unparsed 
	if unparsed.strip() == "": return True

	string = unparsed.replace(name, "collection")
	return eval(string)

			


