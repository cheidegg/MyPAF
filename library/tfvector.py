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


## run
##---------------------------------------------------------------
def run(tevt, tobjs, function, arguments, selection = ""):

	argattr = []
	for a in arguments:
		## object attribute
		if a.find(".") != -1:
			oidxs = lib.findElmAttrAll(tobjs, "name", a.split(".")[0])
			argattr.append([getattr(tobjs[idx], a.split(".")[1]) for idx in oidxs])
		## object
		elif lib.findElmAttr(tobjs, "name", a) > -1:
			#oidxs = lib.findElmAttr(tobjs, "name", a)
			argattr.append([tobj if lib.findElmAttr(tobj, "name", a) > -1 for tobj in lib.subset(tobjs, selection)])
		## event attribute
		else:
			argattr.append(getattr(tevt, a))

	
	## CH: how to get objname?
	if   function == "sum": return sum(argattr)  
	elif function == "mll": return mll(argattr, selection, objname)


## mll
##---------------------------------------------------------------
def mll(tevt, tobjs, objname, selection = ""):

	objs = lib.getListOfAttrs(tevt, tobjs, objname)
	return [tfkernel.mll(obj1, obj2) for [obj1, obj2] in lib.pairs(objs, selection)]


## mt
##---------------------------------------------------------------
def mt(tevt, tobjs, obj1, obj2, selection = ""):
	objs1 = lib.getListOfAttrs(tevt, tobjs, obj1)
	objs2 = lib.getListOfAttrs(tevt, tobjs, obj2)
	return [tfkernel.mt(obj1, obj2) for [obj1, obj2] in lib.combine(objs1, objs2, selection)]


## sum
##---------------------------------------------------------------
def sum(vars):
	return tfkernel.sum(vars)
	
	




	

	## abs
	##---------------------------------------------------------------
	def abs(self, var):
		return abs(var)
	

	## min
	##---------------------------------------------------------------
	def min(self, objs, selection = ""):
		return min(objs)


	## mll
	##---------------------------------------------------------------
	def mll(self, lep1, lep2, selection = ""):
		return (lep1.p4() + lep2.p4()).M()


	## mllAll
	##---------------------------------------------------------------
	def mllAll(self, leps):
		return [self.mll(lep1, lep2) for lep1 in leps for lep2 in leps]


	## mllPairs
	##---------------------------------------------------------------
	def mllPairs(self, leps):
		return [self.mll(lep[0], lep[1]) for lep in leps]


	## mtAll
	##---------------------------------------------------------------
	def mtAll(self, leps, obj, selection = ""):
		return [self.mt(lep, obj) for lep in leps]


	## num
	##---------------------------------------------------------------
	def num(self, arg, selection = ""):
		return len(arg)


### HOW TO IMPLEMENT SELECTION IN FUCNTIONS?
### HOW TO IMPLEMENT ARRAYS IN BRANCHES?	
	

	## sum
	##---------------------------------------------------------------
	def sum(self, arg, selection = ""):
	
		list = findArg(arg)
		sum = 0.
		for summand in list:
		    if parse(selection):
		        sum += summand
		return sum


