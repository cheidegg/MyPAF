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

		self.load(path)	
		self.loadObjs()


	## get
	##--------------------------------------------------------------- 
	def get(self, region, selection = "", columns = "all"):
		## returns the columns given by vars of all entries in the cfg
		## file that match region and selection
		## separate individual columns with ":", define a range with "-"
		## or ask for all columns using "all"
		## ATTENTION: this function shall only be accessed via getAll,
		## getColumn or getVar 

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

		return self.get(region, selection, columns)


	## getColumn
	##--------------------------------------------------------------- 
	def getColumn(self, region, selection = "", column = "first"):
		## returns a single column according to column of all entries in
		## the cfg file that match region and pass the selection

		matrix = self.get(region, selection, column)
		if len(matrix)>0:
			return [l[0] for l in matrix]
		return []


	## getHeader
	##--------------------------------------------------------------- 
	def getHeader(self, region):

		idx = lib.findElm(self.regions, region)
		return self.header[idx].list


	## getObjs
	##--------------------------------------------------------------- 
	def getObjs(self, selection = ""):

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

		column = self.getColumn(region, "name=='" + selection + "'", "value")
		if len(column)>0:
			return column[0]
		return ""


	## hasVar
	##--------------------------------------------------------------- 
	def hasVar(self, selection, region = "head"):

		column = self.getColumn(region, "name=='" + selection + "'", "value")
		if len(column)==0: return False
		if column[0].strip() == "": return False
		return True


	## load
	##--------------------------------------------------------------- 
	def load(self, path):

		if path[0] != "/": path = self.mypaf.path + path
		self.path = path

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

		self.undef = []
		for region in regions:
			eval("self." + region + " = []")

		self.load(path)



