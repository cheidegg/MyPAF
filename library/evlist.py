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


## evlist
##------------------------------------------------------------------- 
class evlist:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, name, variables):

		self.mypaf     = mypaf
		self.db        = mypaf.db
		self.vb        = mypaf.vb

		self.name      = name.strip()
		self.vars      = ["Row"]
		self.vars.extend(variables)


	## addEntry
	##---------------------------------------------------------------
	def addEntry(self, sidx, cidx, values):
		## adds an entry to the event list

		if len(values) == len(self.vars) and len(self.files) > sidx:
			self.files[sidx][cidx].write(":=".join(values) + "\n")


	## build
	##---------------------------------------------------------------
	def build(self, sources, categs):

		self.sources = sources
		self.categs  = categs

		self.paths   = [[mypaf.temppath + "evlist_" + name + "_" + str(sidx) + "_" + str(cidx) + ".txt" for sidx in range(len(sources))] for cidx in range(len(categs))]
		self.files   = [[open(self.paths[sidx][cidx], "a") for sidx in range(len(sources))] for cidx in range(len(categs))]


	## close
	##---------------------------------------------------------------
	def close(self):

		if not self.files[0][0].closed:
			for sidx in range(len(sources)):
				for cidx in range(len(categs)):
					self.files[sidx][cidx].close()
	

	## exportAsHist
	##---------------------------------------------------------------
	def exportAsHist(self, var = "run"):

		self.close()

		## observable?
		alist = args.args("var=" + var)
		i = lib.findElm(self.vars, var)
		binargs, names = lib.prepareHistInfo(self.db, alist)
		h = hist.hist(self.mypaf, self.name, binargs, names)
		h.build(self.sources, self.categs)
		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				f     = open(self.paths[sidx][cidx], "r")
				lines = f.readlines()
				for entry in lines:
					h.fill(sidx, cidx, float(entry.split(":=")[i].strip()))
				f.close()
		return h


	## exportAsText
	##---------------------------------------------------------------
	def export(self):
		## returns the content of the event list as a string in readable form

		self.close()
		text = " : ".join(variables)
		texts = [[text for sidx in range(len(self.sources))] for cidx in range(len(self.categs))]

		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				f     = open(self.paths[sidx][cidx], "r")
				lines = f.readlines()
				for entry in lines:
					texts[sidx][cidx] += " : ".join([e.strip() for e in entry.split(":=")]) + "\n"
				f.close()


	## free
	##---------------------------------------------------------------
	def free(self):

		for sidx in range(len(sources)):
			for cidx in range(len(categs)):
				lib.rmFile(self.paths[sidx][cidx])


	## injectScanFile
	##---------------------------------------------------------------
	def injectScanFile(self, sidx, cidx, path):

		f = open(path, "r")
		full = f.readlines()
		f.close()
		assoc = [i for i in range(len(self.vars))]

		self.files[sidx][cidx].close()
		lib.rmFile(self.paths[sidx][cidx])
		self.files[sidx][cidx] = open(self.paths[sidx][cidx], "a")

		for i, head in enumerate(full[1].split("*")[1:]):
			j = lib.findElm(self.vars, head.strip())
			assoc[i] = j 

		for line in full[3:]:
			nl = [elm[assoc[i]].strip() for i in range(len(line.split("*")[1:]))]
			self.files[sidx][cidx].write(":=".join(nl) + "\n")





