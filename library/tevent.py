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


## tevent
##-------------------------------------------------------------------
class tevent:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, objTemps):

		self.vars = []
		self.defs = []
		self.types = []
		self.objTemps = objTemps


	## addVar
	##---------------------------------------------------------------
	def addVar(self, var, def, dtype):

		self.vars.append(var)
		self.defs.append(def)
		self.types.append(dtype)


	## applySelection
	##---------------------------------------------------------------
	def applySelection(self, selection):
		## applies a selection string

		if eval(interpretSelString(selection)):
			self.passed = True
		else:
			self.passed = False


	## getObjects
	##---------------------------------------------------------------
	def getObjects(self, objname):

		return lib.findElmAttrAll(self.objects, "name", objname)


	## interpretSelString
	##---------------------------------------------------------------
	def interpretSelString(self, selection):
		for k,v in self.__dict__.items(): 
		    string = string.replace(k, "self." + k) 
		for obj in [obj.name for obj in self.objects]: 
		    string = string.replace(obj, "self.getObjects(" + obj + ")") 
		for k,v in tfscalar.__dict__.items(): 
		    string = string.replace(k + "(", "tfscalar." + k + "(self, self.getObjects(" + obj + "), ") 
		for k,v in tfvector.__dict__.items(): 
		    string = string.replace(k + "(", "tfvector." + k + "(self, self.getObjects(" + obj + "), ") 
		return string


	## load
	##---------------------------------------------------------------
	def load(self, evt)

		self.loadObjects(evt)
		## compute all the variables

	
	## loadObjects
	##---------------------------------------------------------------
	def loadObjects(self, evt):
		
		self.objects = []
		for ot in self.objTemps:
			branch = getattr(self.evt, ot.branch)
			instances = len(branch)

			for i in range(instances):
				self.objects.append(tobj.tobj(ot.name))
				self.objects[-1].__dict__.update(ot.__dict__)
				self.objects[-1].setInstance(i)
				self.objects[-1].loadEvt(evt)


