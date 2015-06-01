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

import datetime, os, sys
import mypaf


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
		self.path  = mypaf.prodpath
		self.vb    = setvb
		self.log   = open(self.path + "log.out", "a")

		self.start()


	## end
	##---------------------------------------------------------------
	def end(self):
		self.talk("CLOSING MyPAF - THE my PURPOSE ANALYSIS FRAMEWORK")
		self.log.close()


	## error
	##---------------------------------------------------------------
	def error(self, message):
		self.talk("ERROR: " + message, True)


	## start
	##--------------------------------------------------------------- 
	def start(self):
		self.talk("STARTING MyPAF - THE my PURPOSE ANALYSIS FRAMEWORK")
		if   self.mypaf.imodule == 1: self.talk("INITIALIZING TREE")
		elif self.mypaf.imodule == 2: self.talk("INITIALIZING DRAW")
		elif self.mypaf.imodule == 3: self.talk("INITIALIZING PLOT")
		elif self.mypaf.imodule == 4: self.talk("INITIALIZING SCAN")
		elif self.mypaf.imodule == 5: self.talk("INITIALIZING STAT")
		elif self.mypaf.imodule == 6: self.talk("INITIALIZING HIST")
		elif self.mypaf.imodule == 7: self.talk("INITIALIZING PUBL")
		else: self.error("nothing to initialize")


	## talk
	##--------------------------------------------------------------- 
	def talk(self, message, exit = False):
		if exit: message += ". exiting..."
		if self.vb > 0: print "> " + message
		self.log.write(message + "\n")
		if exit: sys.exit(0)


	## warning
	##--------------------------------------------------------------- 
	def warning(self, message):
		self.talk("WARNING: " + message, False)

