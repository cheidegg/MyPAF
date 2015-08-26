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

import cfgobj, clist, dbreader, lib, mypaf, parser, vb


## cfg
##------------------------------------------------------------------- 
class cfg:

	cfg       = None
	db        = None
	header    = [clist.clist(["name", "value"]), \
                 clist.clist(["type", "name", "path", "args"]), \
                 clist.clist(["type", "name", "definition", "args"]), \
	             clist.clist(["scheme", "name", "definition", "args"]), \
                 clist.clist(["type", "name", "definition"])]
	mypaf     = None
	path      = ""
	regions   = ["head", "input", "output", "schemes", "selection"]
	undef     = []
	vb        = None


	## __init__
	##--------------------------------------------------------------- 
	def __init__(self, input, path):

		for region in self.regions:
			setattr(self, region, [])

		self.mypaf  = input.mypaf
		self.db     = input.mypaf.db
		self.vb     = input.mypaf.vb
		self.vb.call("cfg", "__init__", [self, input, path], "Initializing the cfg class.")

		self.load(path)	
		self.check()
		self.loadObjs()


	## check
	##--------------------------------------------------------------- 
	def check(self):
		## checks the current contents read from the cfg file
		## if its syntax and semantic are OK

		return
		inputfiletypes = ["tree", "file", "root", "evlist", "evyield", "oblist", "obyield", "numfile"]

		for region in regions:
			collection = getattr(self, region)

			for entry in collection:

				## columns missing
				if (region == "head" and len(entry) < 2) or (region != "head" and len(entry) < 3):
					self.vb.error("Not enough information provided in the cfg file at line " + " := ".join(entry) + ".")

				## required head variables => not! defaults should go into the code
				#cvars = [elm[1] for elm in collection]
				#required = ["]
				#if any([True if var not in cvars else False for var in required]

				## input file paths
				if region == "input":
					if entry[0] in inputfiletypes:
						sdef = entry[2].split() 
			
			

	## get
	##--------------------------------------------------------------- 
	def get(self, region, selection = "", columns = "all"):
		## returns the columns given by vars of all entries in the cfg
		## file that match region and selection
		## separate individual columns with ":", define a range with "-"
		## or ask for all columns using "all"
		## ATTENTION: this function shall only be accessed via getAll,
		## getColumn or getVar 

		self.vb.call("cfg", "get", [self, region, selection, columns], "Retrieving information from the cfg file.")
		region    = region.strip()

		result = []
		if region in self.regions: collection = getattr(self, region)
		else                     : collection = self.undef

		header  = self.getHeader(region)
	
		if columns.find(":") != -1:
			cols = columns.split(":")
			rcolumns = [i for i, head in enumerate(header) if head in cols]
		elif columns.find("-") != -1:
			above = False
			cols = columns.split("-")
			rcolumns = []
			for i, head in enumerate(header):
				if head == cols[0]: above = True
				if above: rcolumns.append(i)
				if head == cols[1]: above = False
		elif columns == "all":
			rcolumns = [i for i in range(len(header))]
		elif columns == "first":
			rcolumns = [0]
		elif columns == "last":
			rcolumns = [len(header)-1]
		else:
			rcolumns = [lib.findElm(header, columns)]

		for i, head in enumerate(header):
			selection = selection.replace(head, "line[" + str(i) + "]")	

		for line in collection:
			sel = parser.parse(line, "line", selection)
			if sel:
				result.append([line[i] if i < len(line) else "" for i in rcolumns])

		return result


	## getAll
	##--------------------------------------------------------------- 
	def getAll(self, region, selection = "", columns = "all"):
		## returns the columns given by vars of all entries in the cfg
		## file that match the region and pass the selection
		## separate individual columns with ":", define a range with "-"
		## or ask for all columns using "all"

		self.vb.call("cfg", "getAll", [self, region, selection, columns], "Retrieving a matrix from the cfg file.")
		return self.get(region, selection, columns)


	## getColumn
	##--------------------------------------------------------------- 
	def getColumn(self, region, selection = "", column = "first"):
		## returns a single column according to column of all entries in
		## the cfg file that match region and pass the selection

		self.vb.call("cfg", "getColumn", [self, region, selection, column], "Retrieving a column vector from the cfg file.")
		matrix = self.get(region, selection, column)
		if len(matrix)>0:
			return [l[0] for l in matrix]
		return []


	## getHeader
	##--------------------------------------------------------------- 
	def getHeader(self, region):

		self.vb.call("cfg", "getHeader", [self, region], "Getting the header labels for a given region.")
		idx = lib.findElm(self.regions, region)
		return self.header[idx].list


	## getObjs
	##--------------------------------------------------------------- 
	def getObjs(self, selection = ""):

		self.vb.call("cfg", "getObjs", [self, selection], "Getting a list of objects that pass a given selection.")
		for k,v in self.objs[0].__dict__.items():
			selection = selection.replace(k, "obj." + k)

		olist = []
		for obj in self.objs:
			if parser.parse(obj, "obj", selection):		
				olist.append(obj)
		return olist


	## getVar
	##--------------------------------------------------------------- 
	def getVar(self, selection, region = "head"):
		## returns column var of the first entry in the cfg file that
		## matches the region and passes the selection
		## useful for single, unique variables in the head region

		self.vb.call("cfg", "getVar", [self, selection, region], "Retrieving a header variable from the cfg file.")
		column = self.getColumn(region, "name=='" + selection + "'", "value")
		if len(column)>0:
			return column[0]
		return ""


	## getVars
	##--------------------------------------------------------------- 
	def getVars(self, selection, region = "head"):
		## returns column var of all the entries in the cfg file that
		## matches the region and passes the selection

		self.vb.call("cfg", "getVar", [self, selection, region], "Retrieving a header variable from the cfg file.")
		return self.getColumn(region, "name=='" + selection + "'", "value")


	## hasVar
	##--------------------------------------------------------------- 
	def hasVar(self, selection, region = "head"):

		self.vb.call("cfg", "hasVar", [self, selection, region], "Searching for a header variable.")
		column = self.getColumn(region, "name=='" + selection + "'", "value")
		if len(column)==0: return False
		if column[0].strip() == "": return False
		return True


	## load
	##--------------------------------------------------------------- 
	def load(self, path):

		self.vb.call("cfg", "load", [self, path], "Loading the cfg file " + path + ".")
		if path[0] != "/": path = self.mypaf.path + path
		self.path = path

		self.vb.talk("Configuration file " + self.path + " is loaded.")

		self.cfg = open(path, "r")
		lines = self.cfg.readlines()
		self.cfg.close()

		region = ""
		for line in lines:

			line = line.strip()
			line = line.strip("\t")
			line = line.strip("\n")
			if len(line) == 0: continue
			if line[0] == "#": continue

			if line[0] == "&":
				line   = line.strip("&")
				line   = line.strip()
				if line in self.regions: region = line	
				else                   : region = "undef"
				continue

			cols = line.split(":=")
			cols = [cell.strip().strip("\t") for cell in cols]
			eval("self." + region + ".append(cols)")


	## loadObjs
	##--------------------------------------------------------------- 
	def loadObjs(self):

		self.vb.call("cfg", "loadObjs", [self], "Retrieving all cfg objects from the cfg file.")
		self.objs = []
		for i, region in enumerate(self.regions):
			if region == "head": continue
			full = self.getAll(region)
			if region == "selection":
				full.append(["none", "nosel", ""])
			for entry in full:
				self.objs.append(eval("cfgobj.cfgobj(region, " + ", ".join(["entry[" + str(j) + "]" for j in range(self.header[i].len)]) + ")"))


	## reload
	##--------------------------------------------------------------- 
	def reload(self, path):
		## clears the cache and reloads the cfg file

		self.vb.call("cfg", "reload", [self, path], "Re-loading the class for a new cfg file " + path + ".")
		self.undef = []
		for region in regions:
			eval("self." + region + " = []")

		self.load(path)
		self.check()



