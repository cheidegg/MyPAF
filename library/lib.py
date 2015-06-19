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

import array, copy, datetime, os, ROOT, subprocess
import clist


## addToVectorIfMissing
##---------------------------------------------------------------
def addToVectorIfMissing(vector, element):
	## adds an element to a vector if it does not already contain it

	if element not in vector:
		vector.append(element)

	return vector


## argsWin
##---------------------------------------------------------------
def argsWin(default, sysval, argval):

	if   str(argval) != "": return setDType(getDType(default), argval) 
	elif str(sysval) != "": return setDType(getDType(default), sysval)
	
	return default


## attr
##---------------------------------------------------------------
def attr(vector, attribute):
	## returns a vector of values for a given attribute of every 
	## element instance in a given vector

	result = []

	if len(vector) == 0:
		return result

	if not hasattr(vector[0], attribute): 
		return result

	for entry in vector:
		result.append(getattr(entry, attribute))

	return result


## bash
##---------------------------------------------------------------
def bash(cmd):

	pipe = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	return pipe.stdout.read()


## bins
##---------------------------------------------------------------
def bins(nxbin, xmin, xmax):
	## produces an array of values to separate the equally spaced 
	## nxbin bins between xmin and xmax

	if nxbin == 0 or xmin == xmax:
		return array.array('d', [])

	list = [0. for i in range(nxbin+1)]
	size = (xmax - xmin) / nxbin
	for i in range(nxbin+1):
		list[i] = xmin + i * size
	
	return array.array('d', list)


## cleanDir
##---------------------------------------------------------------
def cleanDir(path, clcmd = "rm -r"):
	## cleans a directory by removing everything that is inside

	path = path.rstrip("/")

	if os.path.isdir(path) and os.listdir(path) != []:
		os.system(clcmd + " " + path + "/*")


## column
##---------------------------------------------------------------
def column(matrix, column):
	## extracts a column from a matrix and returns it as a vector

	result = []

	if len(matrix) > 0 and len(matrix[0]) <= column: 
		return result

	for row in matrix:
		result.append(row[column])

	return result		


## combine
##---------------------------------------------------------------
def combine(objlist1, objlist2, selection = ""):

	if selection == "": return [[o1, o2] for o1 in objlist1 for o2 in objlist2 if not o1 is o2]
	if objname   != "": selection = selection.replace(objname, "obj")

	pairs = []
	for obj1 in objlist1:
		for obj2 in objlist2:
			if not obj1 is obj2:
				if eval(selection):
					pairs.append([obj1, obj2])

	return pairs


## cpFile
##---------------------------------------------------------------
def copyFile(location, destination, cpcmd = "cp"):

	if os.path.isfile(location):
		os.system(cpcmd + " " + location + " " + destination)


## copyHStyle
##---------------------------------------------------------------
def copyHStyle(hdest, hloc):

	return hdest


## dump
##---------------------------------------------------------------
def dump(name, value):
	print name + "=" + str(value)


## findDatasetCfg
##---------------------------------------------------------------
def findDatasetCfg(samplecfg):

	dsnames = []
	for s in samplecfg:
		dsname = self.db.getVar("samples", s.name, "dataset")
		dsnames = addToVectorIfMissing(dsnames, dsname)

	return dsnames	


## findElm
##---------------------------------------------------------------
def findElm(list, value):
	## returns the index of an element in a vector if it exists,
	## otherwise returns -1

	for i, elm in enumerate(list):
		if elm == value:
			return i
	return -1


## findElmAll
##---------------------------------------------------------------
def findElmAll(list, value):
	## returns a vector of indices of all occurrences of an element
	## in a vector

	result = []
	for i, elm in enumerate(list):
		if elm == value:
			result.append(i)
	return result


## findElmAttr
##---------------------------------------------------------------
def findElmAttr(list, attribute, value):
	## returns the index of an attribute of the instances in a 
	## vector if found, otherwise returns -1

	for i, elm in enumerate(list):
		attr = getattr(elm, attribute)
		if attr == value:
			return i
	return -1


## findElmAttrAll
##---------------------------------------------------------------
def findElmAttrAll(list, attribute, value):
	## returns a vector of elements in list whose attribute
	## is equal to value

	result = []
	for i, elm in enumerate(list):
		attr = getattr(elm, attribute)
		if attr == value:
			result.append(i)
	return result


## formatStr
##---------------------------------------------------------------
def formatStr(string, length = 0, append = 0):
	## adds whitespaces to a string in order to achieve the desired length
	## append = 0: add the whitespaces left to the string
	##        = 1: add the whitespaces right to the string
	##        = 2: add the whitespaces equally left and right to the string

	if length == 0         : return string
	if length < len(string): return string

	if   append == 0: return "".join([" " for i in range(length - len(string))]) + string
	elif append == 1: return string + "".join([" " for i in range(length - len(string))])
	elif append == 2: return "".join([" " for i in range((length - len(string)) / 2)]) + string + "".join([" " for i in range((length - len(string)) / 2)])

	return string


## getAllFiles
##---------------------------------------------------------------
def getAllFiles(path):

	return [path + f for f in os.listdir(path) if os.path.isfile(path + f)]


## getColWidths
##---------------------------------------------------------------
def getColWidths(matrix = []):

	if len(matrix)    == 0: return []
	if len(matrix[0]) == 0: return []

	print matrix
	widths = [0 for i in range(len(matrix[0]))]

	for row in matrix:
		for i, col in enumerate(row):
			if len(col.strip()) > widths[i]:
				widths[i] = len(col.strip())

	return widths


## getDType
##---------------------------------------------------------------
def getDType(variable):

	if   type(variable) is int  : return "int"
	elif type(variable) is float: return "float"
	elif type(variable) is str  : return "str"

	return "undef"


## getElmAttrAllOr
##---------------------------------------------------------------
def getElmAttrAllOr(list, attribute, values):
	## returns a vector of elements in list whose attribute
	## is in a given collection

	result = []
	for i, elm in enumerate(list):
		attr = getattr(elm, attribute)
		if attr in values:
			result.append(elm)
	return result


## getElmVar
##---------------------------------------------------------------
def getElmVar(matrix, elm, variable, idx):
	
	for row in matrix:
		if row[elm] == variable:
			return row[idx]
	return None


## getListOfAttrs
##---------------------------------------------------------------
def getListOfAttrs(tevt, tobjs, attr):

	result = []

	## object attribute
	if attr.find(".") != -1:
		oidxs = lib.findElmAttrAll(tobjs, "name", a.split(".")[0])
		result.append([getattr(tobjs[idx], a.split(".")[1]) for idx in oidxs])

	## object
	elif lib.findElmAttr(tobjs, "name", a) > -1:
		result.append([tobjs[idx] for idx in lib.findElmAttr(tobjs, "name", attr)])

	## event attribute
	else:
		result.append(getattr(tevt, attr))

	return result


## getHistMinMax
##---------------------------------------------------------------
def getHistMinMax(hmin, hmax, logscale = False):

	nmin = 0.0
	nmax = 0.0

	if hmax != 0.0 and hmax > hmin:

		nmax = round(1.1 * hmax, 1)
		nmin = round(0.9 * hmin, 1)		

	if logscale and nmin == 0.0:
		nmin = 0.001

	return nmin, nmax


## getObj
##---------------------------------------------------------------
def getObj(objlist, objname):

	idx = findElmAttr(objlist, "name", objname)
	if idx == -1: return None
	return objlist[idx]


## getPadSize
##---------------------------------------------------------------
def getPadSize(pad):
	## returns the size of the area covered by a pad with respect
	## to the total canvas size
	## note that x and y values are already relative to the 
	## canvas position, hence, the product of the dimensions gives
	## the area

	x = pad.GetWNDC()
	y = pad.GetHNDC()

	return x*y


## getTimeStamp
##---------------------------------------------------------------
def getTimeStamp():
	## returns current timestamp in format yyyy-mm-dd-hh-mm-ss

	today   = datetime.datetime.now()
	return str(today.year) + "-" + "%02d" % today.month + "-" + "%02d" % today.day + "-" + "%02d" % today.hour + "-" + "%02d" % today.minute + "-" + "%02d" % today.second
	

## makeDir
##---------------------------------------------------------------
def makeDir(path, mkcmd = "mkdir"):
	## creates a directory if it does not yet exist

	if not os.path.isdir(path):
		os.system(mkcmd + " " + path)


## makeTDir
##---------------------------------------------------------------
def makeTDir(tfile, tdir):
	## creates a TDirectory if it does not yet exist and sets
	## focus to it

	if tfile.GetDirectory(tdir) == None:
		tfile.mkdir(tdir)
	tfile.cd(tdir)

	return tfile


## pairs
##---------------------------------------------------------------
def pairs(objlist, selection = "", objname = ""):

	if selection == "": return [[o1, o2] for o1 in objlist for o2 in objlist if not o1 is o2]
	if objname   != "": selection = selection.replace(objname, "obj")

	pairs = []
	for obj1 in objlist:
		for obj2 in objlist:
			if not obj1 is obj2:
				if eval(selection):
					pairs.append([obj1, obj2])

	return pairs


## prepareHistInfo
##---------------------------------------------------------------
def prepareHistInfo(db, alist):
	## CH: this wants to be improved!!
	
	binargs = []
	names   = []
	
	## 1d histogram
	if (alist.has("obs") or alist.has("obsx")) and not alist.has("obsy"):
		oname = alist.get("obs")
		if alist.has("obsx"): oname = alist.get("obsx")
		obs = db.getRow("observables", "name=='" + oname + "'")
		if obs[6].strip() == "[]": binargs.append(clist.clist(list(bins(int(obs[3]), float(obs[4]), float(obs[5])))))
		else                     : binargs.append(clist.clist(eval(obs[6])))
		if obs[2].strip() == "lep": yaxis = "leptons"
		else                      : yaxis = "events"
		names = [obs[1], yaxis]
	
	## 2d histogram
	elif alist.has("obsx") and alist.has("obsy"):
		obs1 = db.getRow("observables", "name=='" + alist.get("obsx") + "'")
		obs2 = db.getRow("observables", "name=='" + alist.get("obsy") + "'")
		if obs1[6].strip() == "[]": binargs.append(clist.clist(list(bins(int(obs1[3]), float(obs1[4]), float(obs1[5])))))
		else                      : binargs.append(clist.clist(eval(obs1[6])))
		if obs2[6].strip() == "[]": binargs.append(clist.clist(list(bins(int(obs2[3]), float(obs2[4]), float(obs2[5])))))
		else                      : binargs.append(clist.clist(eval(obs2[6])))
		if obs1[2].strip() == "lep": zaxis = "leptons"
		else                       : zaxis = "events"
		names = [obs1[1], obs2[1], zaxis]
	
	return binargs, names



## rebin
##---------------------------------------------------------------
def rebin(h, bins):

	dim = h.GetDimension()

	## CH: only 1dim histograms to be rebinned??
	#if dim == 3: 
	#	h = h.RebinAxis(array.array('d', bins[0].list), h.GetXaxis())
	#	h = h.RebinAxis(array.array('d', bins[1].list), h.GetYaxis())
	#	h = h.RebinAxis(array.array('d', bins[2].list), h.GetZaxis())
	#	#h = h.RebinX(int(bins[0].len)-1,     array.array('d', bins[0].list))
	#	#h = h.RebinX(int(bins[1].len)-1,     array.array('d', bins[1].list))
	#	#h = h.RebinX(int(bins[2].len)-1,     array.array('d', bins[2].list))
	#elif dim == 2: 
	#	h = h.RebinAxis(array.array('d', bins[0].list), h.GetXaxis())
	#	h = h.RebinAxis(array.array('d', bins[1].list), h.GetYaxis())
	#	#h = h.RebinX(int(bins[0].len)-1,     array.array('d', bins[0].list))
	#	#h = h.RebinY(int(bins[1].len)-1,     array.array('d', bins[1].list))
	#else: 
	if dim == 1: 
		h = h.Rebin (int(bins[0].len)-1, "", array.array('d', bins[0].list))

	return h


## removeFromVector
##---------------------------------------------------------------
def removeFromVector(vector, indices = []):

	if indices == []: return vector

	newvector = []
	for i in range(len(vector)):
		if i not in indices:
			newvector.append(vector[i])

	return newvector


## resetHStyle
##---------------------------------------------------------------
def resetHStyle(h):

	h.GetXaxis(). SetTitleSize(0)
	h.GetXaxis().SetTitleOffset(0)
	h.GetXaxis().SetLabelSize(0)
	
	return h


## rmFile
##---------------------------------------------------------------
def rmFile(path, rmcmd = "rm"):

	if os.path.isfile(path):
		os.system(rmcmd + " " + path)


## row
##---------------------------------------------------------------
def row(matrix, row):

	if len(matrix) <= row: 
		return []

	return matrix[row]


## saveHist
##---------------------------------------------------------------
def saveHist(file, h, name):

	sn   = name.split("/")
	
	makeTDir(file, sn[0])
	makeTDir(file, sn[0] + "/" + sn[1])
	
	h.SetName(sn[2])
	h.Write()
	file.Write()

	return h


## scaleLumi
##---------------------------------------------------------------
def scaleLumi(lumi, xsec, nevts):

	return lumi * xsec / nevts


## setDType
##---------------------------------------------------------------
def setDType(dtype, variable):

	if   dtype == "int"  : return int(variable)
	elif dtype == "float": return float(variable)
	elif dtype == "str"  : return str(variable)

	return variable


## setProperBinning
##---------------------------------------------------------------
def setProperBinning(h):

	if toList(h.GetXaxis().GetXbins()) == []:

		hname  = h.GetName()
		htitle = h.GetTitle()
		hdim   = h.GetDimension()

		xbins = bins(h.GetXaxis().GetNbins(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
		print xbins

		if hdim == 2 or hdim == 3:
			ybins = bins(h.GetYaxis().GetNbins(), h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())
		elif hdim == 3:	
			zbins = bins(h.GetZaxis().GetNbins(), h.GetZaxis().GetXmin(), h.GetZaxis().GetXmax())

		htemp = copy.deepcopy(h)
		htemp = copyHStyle(htemp, h)
		del h
		
		if   hdim == 3: h = ROOT.TH3F(hname, htitle, len(xbins)-1, xbins, len(ybins)-1, ybins, len(zbins)-1, zbins)
		elif hdim == 2: h = ROOT.TH2F(hname, htitle, len(xbins)-1, xbins, len(ybins)-1, ybins)
		else          : h = ROOT.TH1F(hname, htitle, len(xbins)-1, xbins)

		h.Add(htemp)
		h = copyHStyle(h, htemp)

	return h		


## subset
##---------------------------------------------------------------
def subset(objlist, selection = "", objname = ""):

	if selection == "": return objlist
	if objname   != "": selection = selection.replace(objname, "obj")

	subset = []
	for obj in objlist:

		#s = obj.interpretSelString(selection)
		if eval(s):
			subset.append(obj)

	return subset


## toList
##---------------------------------------------------------------
def toList(tarrayd):

	list = []
	for i in range(tarrayd.GetSize()):
		list.append(tarrayd[i])
	return list


## uniformBins
##---------------------------------------------------------------
def uniformBins(bins = []):

	if len(bins) <= 2: 
		return True

	if any([bins[i]-bins[i-1]-d for i in range(2,len(bins))]):
		return False

	return True


## usePath
##---------------------------------------------------------------
def usePath(mypafpath, headpath, filepath, argpath = ""):
	## realizes the logic of combining different paths to a file
	## mypafpath = default mypaf input path
	## headpath  = input directory given in header of cfg file
	## filepath  = input filepath of input file
	## argpath   = directory given in arguments to input object

	## argpath replaces headpath
	if argpath != "": headpath = argpath

	## no filepath
	if filepath == "": return ""

	## absolute filepath
	if filepath[0] == "/": return filepath

	## relative filepath and absolute headpath -> relative to headpath
	if headpath[0] == "/":
		if headpath.find("psi.ch") != -1: headpath = "dcap://t3se01.psi.ch:22125/" + headpath
		if headpath.find("eos/")   != -1: headpath = "root://cms-xrd-global.cern.ch/" + headpath
		return headpath.rstrip("/") + "/" + filepath

	## relative filepath and relative headpath -> all relative to mypaf input path
	return mypafpath + headpath.rstrip("/") + "/" + filepath
	


## useVal
##---------------------------------------------------------------
def useVal(default, value1, value2 = ""):
	if   value2 != "": return value2
	elif value1 != "": return value1
	return default


## writeFile
##---------------------------------------------------------------
def writeFile(path, text):
	f = open(path, "w")
	f.write(text)
	f.close()


