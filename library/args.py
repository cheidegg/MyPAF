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

import lib


## args
##------------------------------------------------------------------- 
class args:

	#argstring = ""
	#keys      = []
	#list      = []


	## __init__
	##---------------------------------------------------------------
	def __init__(self, argstring):

		self.argstring = argstring
		self.keys = []
		self.list = []

		if len(argstring.strip()) > 0:
			items = argstring.split()
			for item in items:
				part = item.strip().split("=")
				self.keys.append(part[0])
				self.list.append(part[1])


	## all
	##---------------------------------------------------------------
	def all(self, keypostpend = ""):
		## for all keys that end on keypostpend, assemble a argstring
		## with all keys and values 

		res = []
		for i, k in enumerate(self.keys):
			if k[len(k)-len(keypostpend):] == keypostpend:
				res.append(k + "=" + self.list[i])
		return " ".join(res)		


	## allStrip
	##---------------------------------------------------------------
	def allStrip(self, keypostpend = ""):
		## same as all but strips off the keypostpend

		res = []
		for i, k in enumerate(self.keys):
			if k[len(k)-len(keypostpend):] == keypostpend:
				res.append(k[:len(k)-len(keypostpend)] + "=" + self.list[i])
		return " ".join(res)		



	## has
	##---------------------------------------------------------------
	def has(self, key):

		if len(self.list) == 0:
			return False

		idx = lib.findElm(self.keys, key)
		if idx > -1:
			return True

		return False
		

	## get
	##---------------------------------------------------------------
	def get(self, key):

		if len(self.list) == 0: 
			return ""

		idx = lib.findElm(self.keys, key)
		if idx > -1:
			return self.list[idx]

		return ""


	## getAll
	##---------------------------------------------------------------
	def getAll(self, key):

		if len(self.list) == 0: 
			return ""

		result = []
		idxs = lib.findElmAll(self.keys, key)
		for idx in idxs:
			result.append(self.list[idx])

		return result


	## reinit
	##---------------------------------------------------------------
	def reinit(self, alist):
		## reset keys and values using keys and values in another instance of args

		self.keys = alist.keys
		self.list = alist.list


	## remove
	##---------------------------------------------------------------
	def remove(self, key):
		## removes all occurrences of a key in the list

		if key == "": return

		idxs = lib.findElmAll(self.keys, key)
		k = []
		l = []
		s = []
		for i, key in enumerate(self.keys):
			if i not in idxs:
				k.append(key)
				l.append(self.list[i])
				s.append(key + "=" + self.list[i])

		self.keys = k
		self.list = l
		self.argstring = " ".join(s)


	## resetArgs
	##---------------------------------------------------------------
	def resetArgs(self, argstring):
		## resets new arguments from an argstring

		self.argstring = argstring
		self.keys      = []
		self.list      = []

		if len(argstring.strip()) > 0:
			items = argstring.split()
			for item in items:
				part = item.strip().split("=")
				self.set(part[0], part[1])


	## set
	##---------------------------------------------------------------
	def set(self, key, value):
		## adds a new argument to the class
		## if key already exists, value is overwritten
		## if key does not exist, key/value are added new
	
		idx = lib.findElm(self.keys, key)
		if idx > -1:
			self.list[idx] = value
		else:
			self.keys.append(key)
			self.list.append(value)
			self.argstring += " " + key + "=" + str(value)


	## setArgs
	##---------------------------------------------------------------
	def setArgs(self, argstring):
		## adds new arguments from an argstring

		if len(argstring.strip()) > 0:
			self.argstring += " " + argstring.strip()
			items = argstring.split()
			for item in items:
				part = item.strip().split("=")
				self.set(part[0], part[1])



