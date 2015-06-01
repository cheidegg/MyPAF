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

import ROOT
import args, dbreader, lib


## hstyle
##-------------------------------------------------------------------
class hstyle:

	alist    = None
	defaults = []
	defs     = []
	name     = "zombie"


	## __init__
	##---------------------------------------------------------------
	def __init__(self, db, name, alist):
		## initializes the hstyle class

		self.alist     = alist
		self.db        = db
		self.name      = name
		self.defaults  = self.db.getRow("hstyles", "name == '" + self.name + "'")



	## build
	##---------------------------------------------------------------	
	def build(self, h):
		## applies the selected style to the histogram h

		## note 
		if self.alist.has("note")  : self.note  = args.get("note") 
		elif self.defaults != []   : self.note  = self.defaults[1]
		else                       : self.note  = "cmsPrel"
	
		## grid 
		if self.alist.has("grid")  : self.grid  = args.get("grid")
		elif self.defaults != []   : self.grid  = self.defaults[2]
		else                       : self.grid  = "y"

		## scale
		if self.alist.has("scale") : self.scale = args.get("scale")
		elif self.defaults != []   : self.scale = self.defaults[3]
		else                       : self.scale = "lin"
		
		## norm
		if self.alist.has("norm")  : self.norm  = args.get("norm")
		elif self.defaults != []   : self.norm  = self.defaults[4]
		else                       : self.norm  = "norm"

		## errors
		if self.alist.has("errors"): self.norm  = args.get("norm")
		elif self.defaults != []   : self.norm  = self.defaults[4]
		else                       : self.norm  = "norm"

		
		#h = self.buildNote  (h)
		#h = self.buildGrid  (h)
		#h = self.buildScale (h)
		#h = self.buildNorm  (h)
		#h = self.buildErrors(h)

		return h


	## buildNote
	##---------------------------------------------------------------	
	def buildNote(self):
		print "doing nothing"
		
	
	## buildGrid
	##---------------------------------------------------------------	
	def buildGrid(self):
		print "doing nothing"







