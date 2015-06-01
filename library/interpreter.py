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

import schemes


## parser
##------------------------------------------------------------------- 
class parser:

	db      = None
	input   = None
	mypaf   = None
	vb      = None

	objects = []
	

	## __init__
	##---------------------------------------------------------------
	def __init__(self, input):

		self.input = input


	## interpret
	##---------------------------------------------------------------
	def interpret(self, unparsed):

		parsed = unparsed

		## parses a definition string for the following:
		## - tree variables and mathematical combinations -> no actions
		## - replace EVENTinLIST by a selection
		## - replace OBJECTinLIST by a selection
		## - open histogram in canvas or root file and take
		##   + the histogram
		##   + a specific bin


		## room for putting histograms and such
		#if   unparsed.find("EVENTinLIST[") != -1: 
		#elif unparsed.find("OBJECTinLIST[") != -1:

		return parsed


	## parse 
	##---------------------------------------------------------------
	def parse(self, collection, name, unparsed):

		## using elements from collection in parsing of unparsed 

		string = unparsed.replace(name, "collection")
		return eval(string)

			


