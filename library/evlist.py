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

import os
import args, dbreader, hist, lib, mypaf, vb


## evlist
##------------------------------------------------------------------- 
class evlist:


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf, name, variables, argstring = ""):

		self.mypaf     = mypaf
		self.db        = mypaf.db
		self.vb        = mypaf.vb
		self.vb.call("evlist", "__init__", [self, mypaf, name, variables, argstring], "Initializing the evlist class.")

		self.name      = name.strip()
		self.alist     = args.args(argstring)
		self.vars      = ["Row", lib.useVal("run" , self.mypaf.input.cfg.getVar("treevarrun" )), \
		                         lib.useVal("lumi", self.mypaf.input.cfg.getVar("treevarlumi")), \
		                         lib.useVal("evt" , self.mypaf.input.cfg.getVar("treevarevt" ))]
		self.vars.extend(variables)
		self.built     = False


	## addEntry
	##---------------------------------------------------------------
	def addEntry(self, sidx, cidx, values):
		## adds an entry to the event list

		self.vb.call("evlist", "addEntry", [self, sidx, cidx, values], "Adding an entry to the evlist.")
		if len(values) == len(self.vars) and len(self.files) > sidx:
			self.files[sidx][cidx].write(":=".join(values) + "\n")


	## build
	##---------------------------------------------------------------
	def build(self, sources, categs):

		self.vb.call("evlist", "build", [self, sources, categs], "Building the evlist.")

		self.sources = sources
		self.categs  = categs

		self.paths   = [[self.mypaf.prodpath + "evlist_" + self.name + "_" + self.sources[sidx] + "_" + self.categs[cidx] + ".txt" for cidx in range(len(categs))] for sidx in range(len(sources))]
		self.files   = [[open(self.paths[sidx][cidx], "a") for cidx in range(len(categs))] for sidx in range(len(sources))]
		self.built   = True


	## close
	##---------------------------------------------------------------
	def close(self):

		self.vb.call("evlist", "close", [self], "Closing the evlist.")

		if not self.files[0][0].closed:
			for sidx in range(len(sources)):
				for cidx in range(len(categs)):
					self.files[sidx][cidx].close()


	## exportAsCSV
	##---------------------------------------------------------------
	def exportAsCSV(self):

		self.vb.call("evlist", "exportAsCSV", [self], "Exporting the evlist as CSV.")

		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				self.files[sidx][cidx].close()
				f = open(self.paths[sidx][cidx], "r")
				lines = [l.replace(":", ",") for l in f.readlines()]
				f.close()

				f = open(self.paths[sidx][cidx].replace(".txt", ".csv"), "a")
				for l in lines:
					f.write(l)
				f.close()
				self.files[sidx][cidx] = open(self.paths[sidx][cidx], "a")


	## exportAsHist
	##---------------------------------------------------------------
	def exportAsHist(self, var = "run"):

		self.vb.call("evlist", "exportAsHist", [self, var], "Exporting the evlist as histogram.")

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


	## exportAsPick
	##---------------------------------------------------------------
	def exportAsPick(self):

		self.vb.call("evlist", "exportAsPick", [self], "Exporting the evlist as TXT file good for doing pickevents.")

		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				self.files[sidx][cidx].close()
				f = open(self.paths[sidx][cidx], "r")
				lines = [":".join(l.split(":")[1:4]) for l in f.readlines()[2:]]
				f.close()

				f = open(self.paths[sidx][cidx].replace(".txt", "_pick.txt"), "a")
				for l in lines:
					f.write(l + "\n")
				f.close()
				self.files[sidx][cidx] = open(self.paths[sidx][cidx], "a")


	## exportAsText
	##---------------------------------------------------------------
	def exportAsText(self):
		## returns the content of the event list as a string in readable form

		self.vb.call("evlist", "exportAsText", [self], "Exporting the evlist as TXT file.")

		self.close()
		text = " : ".join(self.vars) + "\n"
		text += "\n"
		texts = [[text for cidx in range(len(self.categs))] for sidx in range(len(self.sources))]

		for sidx in range(len(self.sources)):
			for cidx in range(len(self.categs)):
				f     = open(self.paths[sidx][cidx], "r")
				lines = f.readlines()
				f.close()

				for entry in lines:
					texts[sidx][cidx] += " : ".join([e.strip() for e in entry.split(":=")]) + "\n"

		return texts


	## free
	##---------------------------------------------------------------
	def free(self):

		self.vb.call("evlist", "free", [self], "Freeing memory.")

		for sidx in range(len(sources)):
			for cidx in range(len(categs)):
				lib.rmFile(self.paths[sidx][cidx])


	## injectScanFile
	##---------------------------------------------------------------
	def injectScanFile(self, sidx, cidx, path):

		self.vb.call("evlist", "injectScanFile", [self, sidx, cidx, path], "Injecting an event list in a file done with TTree::Scan.")

		f = open(path, "r")
		full = f.readlines()
		f.close()

		## CH: do not need to compute format ourselves, can take the one from the scan file 
		#cols = lib.getColWidths([line.split("*")[1:len(line.split("*"))-1] for i, line in enumerate(full) if not i == 0 and not i == 2 and not i == len(full)-1]) ## due to * format 
		##cols = [len(col) for i, col in enumerate(full[1].split("*")[1:len(full[1].split("*"))-1])]

		#assoc = [i for i in range(len(self.vars))]
		#header = []

		self.files[sidx][cidx].close()
		lib.rmFile(self.paths[sidx][cidx])
		self.files[sidx][cidx] = open(self.paths[sidx][cidx], "a")

		#print full[1].strip("\n").split("*")[1:len(full[1].split("*"))-1]
		#for i, head in enumerate([entry.strip() for entry in full[1].strip("\n").split("*")[1:len(full[1].split("*"))-1]]):
		#	j = lib.findElm(self.vars, head)
		#	print "searching for " + head + " in " + str(self.vars) + " found " + str(j) 
		#	assoc[i] = j 
		#	header.append(self.vars[j])

		self.files[sidx][cidx].write(" : ".join(self.vars) + "\n\n")

		for line in full[3:len(full)-1]:
			elm = line.split("*")[1:len(line.split("*"))-1]
			#print elm
			#print assoc
			#nl = [elm[assoc[i]].strip() for i in range(len(elm))]
			#nl = [lib.formatStr(elm[assoc[i]].strip(), cols[i]) for i in range(len(elm))]
			nl = [elm[i] for i in range(len(elm))]
			self.files[sidx][cidx].write(" : ".join(nl) + "\n")


	## getColWidths
	## formatStr


