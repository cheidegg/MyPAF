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
	def __init__(self, selstring, sels = []):

		self.string = self.load(selstring, sels)

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



	## load
	##---------------------------------------------------------------
	def load(self, selstring, sels = []):
		## replaces other selection strings used in this selection string
		## via the SEL[<name>] keyword

		if sels                   == []: return selstring
		if selstring.find("SEL[") == -1: return selstring

		pos = selstring.find("SEL[")
		end = pos + 4 + selstring[pos + 4:].find("]")
		name = selstring[pos+4:end]

		newstring = selstring[0:pos] + sels[lib.findElm([s[0] for s in sels], name)][1] + selstring[end+1:]

		return self.load(newstring, sels)	




