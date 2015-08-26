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

import sys
import lib, mypaf


## vb
##------------------------------------------------------------------- 
class vb:

	path  = ""
	log   = None

	mypaf = None
	vb    = 0


	## __init__
	##--------------------------------------------------------------- 
	def __init__(self, mypaf, setvb):

		self.mypaf = mypaf
		self.path  = mypaf.temppath # we're in a pickle, first call vb and then input or the other way around?
		self.vb    = setvb
		self.log   = open(self.path + "log.out", "a")

		self.start()


	## call
	##---------------------------------------------------------------
	def call(self, classname, functionname, arguments, description):
		if self.vb > 0: return 
		self.talk("CALL " + classname + "." + functionname + "(" + ", ".join([str(a) for a in arguments]) + "): " + description, 0)


	## end
	##---------------------------------------------------------------
	def end(self):
		self.talk("CLOSING MyPAF - THE my PURPOSE ANALYSIS FRAMEWORK")
		self.log.close()


	## error
	##---------------------------------------------------------------
	def error(self, message):
		self.talk("ERROR: " + message + " EXITING.", 0, True)


	## move
	##--------------------------------------------------------------- 
	def move(self):
		self.log.close()
		lib.mvFile(self.path + "log.out", self.mypaf.prodpathmypaf + "log.out")
		self.path = self.mypaf.prodpathmypaf
		self.log  = open(self.path + "log.out", "a")


	## modulein
	##--------------------------------------------------------------- 
	def modulein(self):
		self.talk("LOADING INPUT FOR MODULE " + self.mypaf.module.upper(), 2)


	## moduleout
	##--------------------------------------------------------------- 
	def moduleout(self):
		self.talk("PREPARING OUTPUT FOR MODULE " + self.mypaf.module.upper(), 2)


	## modulerun
	##--------------------------------------------------------------- 
	def modulerun(self):
		self.talk("RUNNING MODULE " + self.mypaf.module.upper(), 2)


	## setVB
	##--------------------------------------------------------------- 
	def setVB(self, setvb):
		self.vb    = setvb


	## start
	##--------------------------------------------------------------- 
	def start(self):
		self.talk("STARTING MyPAF - THE my PURPOSE ANALYSIS FRAMEWORK", 2)


	## talk
	##--------------------------------------------------------------- 
	def talk(self, message, level = 0, exit = False):
		if exit: 
			message += ". exiting..."
		if level >= self.vb: 
			print "> " + message
		if not self.log.closed:
			self.log.write(message + "\n")
		if exit: 
			sys.exit(0)


	## warning
	##--------------------------------------------------------------- 
	def warning(self, message):
		self.talk("WARNING: " + message, 0, False)





