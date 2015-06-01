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


## tobject
##-------------------------------------------------------------------
class tobject:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, name, instance = -1):

		self.name  = name
		self.i     = instance
		self.ready = False

	
	## addVar
	##---------------------------------------------------------------
	def addVar(self, var, def, dtype):

		self.vars.append(var)
		self.defs.append(def)


	## applySelections
	##---------------------------------------------------------------
	def applySelections(self):

		## applies the selections by adding an attribute with true/false to the instance for every selection
		for i, s in enumerate(self.selstrings):
			setattr(self, "sel_" + self.selnames[i], eval(s))


	## interpretSelString
	##---------------------------------------------------------------
	def interpretSelString(self, string, objid = ""):

		if objid.strip() == "":
			string = string.replace(name, "self.")
		for obj in self.objnames:
			string = string.replace(obj, "self.event.getObjects(" + obj + ")")
		for k,v in self.event.__dict__.items():
			string = string.replace(k, "self.event." + k)
		for k,v in tfscalar.__dict__.items():
			string = string.replace(k + "(", "tfscalar." + k + "(self.event, self, ")
		for k,v in tfvector.__dict__.items():
			string = string.replace(k + "(", "tfvector." + k + "(self.event, self, ")
		return string


	## loadEvt
	##---------------------------------------------------------------
	def loadEvt(self, evt):

		if self.i < 1: return
		if not self.ready: self.prepare()

		self.event = evt

		## compute every variable
		for i, v in enumerate(self.vars):
			setattr(self, v, eval(self.defs[i]))	
		
		self.applySelections()		


	## prepare
	##---------------------------------------------------------------
	def prepare(self):

		if not self.ready:
			for d in self.defs:
				d = self.interpretSelString(d)

			self.ready = True
		

	## setBranch
	##---------------------------------------------------------------
	def setBranch(self, branch):
		self.branch = branch


	## setInstance
	##---------------------------------------------------------------
	def setInstance(self, instance):
		self.i = instance


	## setObjNames
	##---------------------------------------------------------------
	def setObjNames(self, objnames):
		self.objnames = objnames


	## setSelections
	##---------------------------------------------------------------
	def setSelections(self, selections = []):

		self.selnames   = []
		self.selstrings = []
		for s in selections:
			alist = args.args(s[3])
			if alist.has("obj") and alist.get("obj") == name:
				self.selnames  .append(s[1])
				self.selstrings.append(interpretSelString(s[2]))


