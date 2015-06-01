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
import dbreader, lib, mypaf, tevent, tobject, vb


## tvars
##-------------------------------------------------------------------
class tvars:



	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf,  vnames, vdefs, vsels, vargs = ""):

		self.mypaf = mypaf
		self.db    = mypaf.db
		self.vb    = mypaf.vb

		self.vars = vnames
		self.defs = vdefs
		self.sels = vsels
		self.args = vargs

		self.tevt = None
		self.prepareObjects()
		self.prepareTree()


		
	## applySelection
	##---------------------------------------------------------------
	def applySelection(self, idx):

		if self.event == None: return 
		if selection  == ""  : return 

		self.event.applySelection(self.sels[idx])


	## close
	##---------------------------------------------------------------
	def close(self):

		self.closeTrees()
		self.freeBranches()


	## closeTrees
	##---------------------------------------------------------------
	def closeTrees(self):
		self.ot = None
		#self.nt.Close()
		#self.nt = None


	## freeBranches
	##---------------------------------------------------------------
	def freeBranches(self):

		print "really necessary?"


	## getBranchType
	##---------------------------------------------------------------
	def getBranchType(self, branch):

		dtype = self.ot.GetBranch(branch).GetLeaf(branch).GetTypeName() 
		if dtype[0:3] == "Int"   : return "int"
		if dtype[0:6] == "Double": return "float"
	
		return "float"
	

	## getVarType
	##---------------------------------------------------------------
	def getVarType(self, var):

		definition = self.vdefs[lib.findElm(self.vars, var)]

		if self.isBranch(definition):
			return self.getBranchType(definition)
		elif self.isComputable(definition):
			## CH: what for?
			##self.defs[i] = self.fixAttr(self.defs[i])
			return "float"
		
		return "float"


	## isBranch
	##---------------------------------------------------------------
	def isBranch(self, definition):

		if hasattr(self.ot, definition):
			return True

		return False


	## isComputable
	##---------------------------------------------------------------
	def isComputable(self, definition):

		## do somehow differently
	
		if definition.strip() == "": return False
	
		for f in self.functions:
			if definition.find(" " + f + "(") != -1:
				return True

		return False
	

	## load
	##---------------------------------------------------------------
	def load(self, evt):

		for obj in self.objects:
			obj.loadEvt(evt)
		self.event.load(evt)


	## prepareEvent
	##---------------------------------------------------------------
	def prepareEvent(self):

		self.event = tevt.tevt(self.objtemps)

		for i, var in enumerate(self.vars):
			if var.find(".") == -1:
				self.event.addVar(var, self.defs[i], self.getVarType(var))


	## prepareObjects
	##---------------------------------------------------------------
	def prepareObjects(self):
		## prepares a list of objects and objectnames and adds the
		## variables to the objects

		self.objnames = []
		for i, var in enumerate(self.vars):
			if var.find(".") != -1:
				if var.split(".")[0] not in self.objnames:
					self.objnames = lib.addToVectorIfMissing(self.objnames, var.split(".")[0])
					self.objtemps.append(tobject.tobject(objname))
					self.objtemps.setSelections(self.mypaf.input.objsel)
				
				idx = lib.findElmAttr(self.objects, "name", var.split(".")[0])
				self.objtemps[idx].addVar(var.split(".")[1], self.defs[i], self.getVarType(var))
				if self.isBranch(self.defs[i]):
					self.objtemps[idx].setBranch(self.defs[i])
	
		for obj in self.objtemps:
			obj.prepare()


	## prepareTree
	##---------------------------------------------------------------
	def prepareTree(self):
		## prepares the new tree with its branches

		for i, var in enumerate(self.vars):

			if var.strip() == "" or self.vdefs[i].strip() == "": continue

			bname = var
			aname = var
			dtype = self.getVarType(var)

			if var.find(".") != -1:
				idx = lib.findElmAttr(self.objects, "name", var.split(".")[0])
				source = self.objects[idx]
				bname = var.replace(".", "_")
				aname = var[1]
			else:
				source = self.event

			if hasattr(source, aname):

				dt = "F"
				if dtype == "int":
					dt = "I"

				self.nt.Branch(bname, getattr(self, aname), aname + "/" + dt)	


	## setNewTree
	##---------------------------------------------------------------
	def setNewTree(self, tree):

		self.nt = tree


	## setOldTree
	##---------------------------------------------------------------
	def setOldTree(self, tree):

		self.ot = tree


	## write
	##---------------------------------------------------------------
	def write(self):

		if self.event.passed:	
			self.nt.fill()



########################################################################


	## fixAttr
	##---------------------------------------------------------------
	def fixAttr(self, string):

		if string.strip() == "": return string
	
		for f in self.functions:
			string.replace(" " + f + "(", " self." + f + "(")

		for b in self.ot.GetListOfBranches():
			string.replace(b.GetName(), "self.evt." + b.GetName()) 

		for i, v in enumerate(self.vars):
			string.replace(v, "self.vals[" + i + "]")

		return string
	

	## prepareObjects
	##---------------------------------------------------------------
	def prepareObjects(self):

		for i, var in enumerate(self.vars):

			objname = lib.getObj(var)
			if objname not in [o.name for o in self.tobj]:
				self.tobj.append(tobj.tobj(objname))
				self.tevt.addObj(self.tobj[-1])


	## recompute
	##---------------------------------------------------------------
	def recompute(self):
		## compute the values of all variables with the entries in the
		## current event and store them in the variables for the branches

		for i, var in enumerate(self.vars):
			if self.isBranch(self.defs[i]):
				self.vals[i] = getattr(self.tevt, self.defs[i])
			elif self.isComputable(self.defs[i]):
				eval("self.vals[i] = float(" + self.defs[i] + ")")
				## CH: attention! is it guaranteed that every variable needed in the computation comes from the good evt?
			else:
				self.vals[i] = float(self.defs[i])


## first load old branches into buffer -> lep, jet, met, objects...
## take these objects to compute new branches
## write new branches into new tree

	## subset
	##---------------------------------------------------------------
	def subset(self, objs, selection = ""):
		result = []
		for obj in objs:
			if selection:
				result.append(obj)
		return result


	## pairs
	##---------------------------------------------------------------
	def pairs(self, objs1, objs2, selection = ""):
		result = []
		for obj1 in objs1:
			for obj2 in obj2:
				if selection:
					result.append([obj1, obj2])
		return result


	## write
	##---------------------------------------------------------------
	def write(self):

		## fill objects and variables into branches and write to tree

		self.nt.fill()		



	## HERE GO THE PHYSICAL FUNCTIONS
	##---------------------------------------------------------------
	##---------------------------------------------------------------
	

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


