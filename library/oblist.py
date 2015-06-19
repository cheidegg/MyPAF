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


## oblist
##------------------------------------------------------------------- 
class oblist:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, obj, name, variables, argstring = ""):

		self.mypaf     = mypaf
		self.db        = mypaf.db
		self.vb        = mypaf.vb

		self.obj       = obj.strip()
		self.name      = name.strip()
		self.alist     = args.args(argstring)
		self.vars      = ["Row", "Instance"]
		self.vars.extend(variables)
		self.built     = False


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

		print self.sources
		print categs
		self.paths   = [[self.mypaf.temppath + "oblist_" + self.name + "_" + self.sources[sidx] + "_" + self.categs[cidx] + ".txt" for cidx in range(len(categs))] for sidx in range(len(sources))]
		self.files   = [[open(self.paths[sidx][cidx], "a") for cidx in range(len(categs))] for sidx in range(len(sources))]
		self.built   = True


	## close
	##---------------------------------------------------------------
	def close(self):

		if not self.files[0][0].closed:
			for sidx in range(len(sources)):
				for cidx in range(len(categs)):
					self.files[sidx][cidx].close()
	

	## exportAsHist
	##---------------------------------------------------------------
	def exportAsHist(self, var = "pt"):

		self.close()

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
		## returns the content of the object list as a string in readable form

		self.close()
		text = " : ".join(self.vars) + "\n"
		text += "\n"
		texts = [[text for cidx in range(len(self.categs))] for sidx in range(len(self.sources))]

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
		header = []

		self.files[sidx][cidx].close()
		lib.rmFile(self.paths[sidx][cidx])
		self.files[sidx][cidx] = open(self.paths[sidx][cidx], "a")

		for i, head in enumerate(full[1].split("*")[1:]):
			j = lib.findElm(self.vars, head.strip())
			assoc[i] = j
			header.append(self.vars[j])

		self.files[sidx][cidx].write(" : ".join(header) + "\n\n")
		
		for line in full[3:]:
			nl = [elm[assoc[i]].strip() for i in range(len(line.split("*")[1:]))]
			self.files[sidx][cidx].write(" : ".join(nl) + "\n")
	



