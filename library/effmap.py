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

import args, dbreader, hist, lib, mypaf, vb


## effmap
##------------------------------------------------------------------- 
class effmap:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, name, definition, argstring = ""):

		self.mypaf     = mypaf
		self.db        = mypaf.db
		self.vb        = mypaf.vb
		self.vb.call("effmap", "__init__", [self, mypaf, name, definition, argstring], "Initializing the effmap class.")

		self.name      = name.strip()
		self.alist     = args.args(argstring)
		self.defs      = definition
		self.built     = False


	## build
	##---------------------------------------------------------------
	def build(self, sources, categs):

		self.vb.call("effmap", "build", [self, sources, categs], "Building the effmap.")

		self.sources = sources
		self.categs  = categs

		self.sss = []
		for sel in self.defs:
			defaults = lib.buildSelSteps(sel, (self.alist.get("ind") == "y"))
			list = []
			for i, d in enumerate(defaults):
				list.append(lib.useVal(d, self.alist.get("name" + str(i+1))))
			self.sss.append(list)

		#sdefs = [lib.buildSelSteps(sel, (self.alist.get("ind") == "y")) for sel in self.defs]
		#self.sss     = [lib.buildSelSteps(sel, (self.alist.get("ind") == "y")) for sel in self.defs]
		self.effs    = [[[0 for i in range(len(self.sss[cidx]))] for cidx in range(len(categs))] for sidx in range(len(sources))]
		self.paths   = [[self.mypaf.prodpath + "effmap_" + self.name + "_" + self.sources[sidx] + "_" + self.categs[cidx] + ".txt" for cidx in range(len(categs))] for sidx in range(len(sources))]
		self.built   = True


	## exportAsCSV
	##---------------------------------------------------------------
	def exportAsCSV(self):

		self.vb.call("effmap", "exportAsCSV", [self], "Exporting the effmap as a CSV file.")
		texts = [["" for cidx in range(len(self.categs))] for sidx in range(len(self.sources))]


		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				path = self.mypaf.prodpath + "effmap_" + self.name + "_" + self.sources[sidx] + "_" + self.categs[cidx] + ".csv" 
				f     = open(path, "a")
				first = self.effs[sidx][cidx][0]
				last  = first
				for i in range(len(self.effs[sidx][cidx])):
					percf = round(lib.div(float(self.effs[sidx][cidx][i]), first) * 100, 2)
					percl = round(lib.div(float(self.effs[sidx][cidx][i]), last ) * 100, 2)
					f.write(self.sss[cidx][i] + "," + str(self.effs[sidx][cidx][i]) + "," + str(percf) + "," + str(percl) + "\n")
					last = float(self.effs[sidx][cidx][i])
				f.close()


	## exportAsHist
	##---------------------------------------------------------------
	def exportAsHist(self):

		self.vb.call("effmap", "exportAsHist", [self], "Exporting the effmap as histogram.")

		## needs to be rewritten!


		## observable?
		#alist = args.args("var=" + var)
		#i = lib.findElm(self.vars, var)
		#binargs, names = lib.prepareHistInfo(self.db, alist)
		#h = hist.hist(self.mypaf, self.name, binargs, names)
		#h.build(self.sources, self.categs)
		#for sidx in range(len(self.sources)):
		#	for cidx in range(len(self.categs)):
		#		f     = open(self.paths[sidx][cidx], "r")
		#		lines = f.readlines()
		#		for entry in lines:
		#			h.fill(sidx, cidx, float(entry.split(":=")[i].strip()))
		#		f.close()
		#return h


	## exportAsTXT
	##---------------------------------------------------------------
	def exportAsTXT(self):

		self.vb.call("effmap", "exportAsTXT", [self], "Exporting the effmap as a TXT file.")

		texts = [["" for cidx in range(len(self.categs))] for sidx in range(len(self.sources))]

		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				path = self.mypaf.prodpath + "effmap_" + self.name + "_" + self.sources[sidx] + "_" + self.categs[cidx] + ".txt" 
				f    = open(path, "a")
				for i in range(len(self.effs[sidx][cidx])):
					f.write(self.sss[cidx][i] + ": " + str(self.effs[sidx][cidx][i]) + "\n")
				f.close()


	## exportAsText
	##---------------------------------------------------------------
	def exportAsText(self):
		## returns the content of the effmap as a string in readable form

		self.vb.call("effmap", "exportAsText", [self], "Exporting the effmap as text.")

		texts = [["" for cidx in range(len(self.categs))] for sidx in range(len(self.sources))]

		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				for i in range(len(self.effs[sidx][cidx])):
					texts[sidx][cidx] += self.sss[sidx][cidx][i] + ": " + str(self.effs[sidx][cidx][i]) + "\n"

		return texts


	## inject
	##---------------------------------------------------------------
	def inject(self, sidx, cidx, yields = []):

		self.vb.call("effmap", "inject", [self, sidx, cidx, yields], "Injecting efficiency to effmap.")
		self.effs[sidx][cidx] = yields




