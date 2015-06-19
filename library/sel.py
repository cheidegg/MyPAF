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


## sel
##------------------------------------------------------------------- 
class sel:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, selstring):

		self.string = selstring

		#self.collectArgs()



	## addAnd
	##---------------------------------------------------------------
	def addAnd(self, statement = ""):
		## for all keys that end on keypostpend, assemble a argstring
		## with all keys and values

		if statement   == "": return
		if self.string == "": self.string = statement

		self.string += " && " + statement 
		## self.updateString()

		## CH: actually should be doing the following:
		## - init calls collectArgs which splits up the selstring into individual arguments and their structure
		## - addAnd adds a statement to this structure and then calls updateString() which updates the entire string 





