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
#import args, evlist, evyield, histcoll, oblist, obyield, schemes
import args, evlist, lib, oblist, schemes


## hscheme
##-------------------------------------------------------------------
class hscheme:

	#dargs      = []
	#name       = "zombie"
	#type       = "none"
	#alist      = None

	#errorstate = False
	#h          = None

	mypaf      = None
	db         = None
	vb         = None


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, type, name, definition = "", argstring = ""):

		self.type       = type
		self.name       = name
		self.dargs      = definition.strip().split()
		self.alist      = args.args(argstring)
		self.argstring  = argstring

		self.errorstate = False
		self.executed   = False

		self.mypaf      = mypaf
		self.db         = mypaf.db
		self.vb         = mypaf.vb

		self.vb.call("hscheme", "__init__", [self, mypaf, type, name, definition, argstring], "Initializing the hscheme class.")
		self.check()


	## build
	##---------------------------------------------------------------
	def build(self):
		## first run the argument schemes, then run this scheme

		self.vb.call("hscheme", "build", [self], "Building the hscheme.")

		if not self.isTrivial():

			if self.type == "draw":
				self.draw()

			else:	
				if not self.executed and not self.errorstate:

					## run previous schemes
					argeval = []
					for scheme in self.schemes:
						scheme.build()
						argeval.append(scheme)

					## run this scheme
					self.h = schemes.run(self.type, self.name, argeval, self.alist)
					self.setExecuted()

			## draw result
			if self.isPrimary():
					self.h.alist.resetArgs(self.argstring)
					self.h.setP(True)
					self.h.draw()
					#self.h.draw("", 0, True)

			## reset argument schemes to initial	
			if self.type != "draw":
				for scheme in self.schemes:
					scheme.getHist().loadInitial()

			self.mypaf.resetCanv()


	## check
	##---------------------------------------------------------------
	def check(self):

		## check for good type, if it exists in schemes
		## check for number of arguments in definition
		## check if all arguments are hschemes themselves
		## check for arguments in arglist

		self.vb.call("hscheme", "check", [self], "Performing basic checks for the hscheme.")


	## draw
	##---------------------------------------------------------------
	def draw(self):
		## a non-trivial scheme tries to draw a trivial scheme
		## first, reload the trivial scheme which reproduces the histogram for that scheme
		## second, put the histogram into the non-trivial scheme

		self.vb.call("hscheme", "draw", [self], "Drawing a non-trivial scheme with trivial input.")

		if self.type == "draw" and len(self.schemes) == 1:
			self.schemes[0].reload(self.alist.get("var"))
			self.h = self.schemes[0].getHist()


	## getHist
	##---------------------------------------------------------------
	def getHist(self):

		self.vb.call("hscheme", "getHist", [self], "Returning the histogram of the scheme.")
		return self.h
 

	## isPrimary
	##---------------------------------------------------------------
	def isPrimary(self):

		self.vb.call("hscheme", "isPrimary", [self], "Testing if the scheme is primary.")

		if self.isTrivial()     : return True

		if self.type == "add"   : return True
		if self.type == "div"   : return True
		if self.type == "draw"  : return True
		#if self.type == "ffit"  : return True
		if self.type == "filter": return True
		if self.type == "mult"  : return True
		if self.type == "proj"  : return True
		if self.type == "sub"   : return True
		#if self.type == "tfit"  : return True

		return False


	## isTrivial
	##---------------------------------------------------------------
	def isTrivial(self):

		self.vb.call("hscheme", "isTrivial", [self], "Testing if the scheme is trivial.")

		if self.type == "hist"  : return True
		if self.type == "elhist": return True
		if self.type == "eyhist": return True
		if self.type == "olhist": return True
		if self.type == "oyhist": return True 

		return False


	## reload
	##---------------------------------------------------------------
	def reload(self, arg):
		## when a trivial hscheme is initialized, we may have several
		## hists from a given object that could interest us (c.f.
		## event lists produce hists for every variable)
		## when drawing the trivial hscheme, we need to reset the histogram

		self.vb.call("hscheme", "reload", [self, arg], "Reloading the scheme and its histogram if its trivial.")

		if self.isTrivial() and self.type != "hist":	
			self.h = self.obj.exportAsHist(arg)


	## setExecuted
	##---------------------------------------------------------------
	def setExecuted(self):
		self.vb.call("hscheme", "setExectued", [self], "Setting the executed parameter to true.")
		self.executed = True


	## setSchemes
	##---------------------------------------------------------------
	def setSchemes(self, schemelist):
		## check if one of the definition arguments is also a scheme
		## if so, this scheme needs to be run first, so we save it for later

		self.vb.call("hscheme", "setSchemes", [self, schemelist], "Checking if one of the arguments in the definition is also a scheme.")
		self.schemes = []

		if not self.isTrivial():
			for arg in self.dargs:
				idx = lib.findElmAttr(schemelist, "name", arg)
				if idx > -1:
					if schemelist[idx].isPrimary():
						schemelist[idx].setSchemes(schemelist)
						self.schemes.append(schemelist[idx])
					else:
						self.vb.warning("trying to read secondary scheme as argument. scheme cannot be evaluated.")
						self.errorstate = True
				else:
					self.vb.warning("argument is not a valid scheme.")
					self.errorstate = True			


	## setTrivial
	##---------------------------------------------------------------
	def setTrivial(self, obj):

		self.vb.call("hscheme", "setTrivial", [self, obj], "Setting trivial scheme for the hscheme.")

		if not self.isTrivial(): return False

		self.obj = obj
		self.setExecuted()

		## set histogram from histogram
		if self.type == "hist":
			self.h = obj
			return True

		## set histogram from evlist, evyields, oblist or obyields
		else:
			self.h = obj.exportAsHist()
			return True




