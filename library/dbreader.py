#################################################################
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
import clist, lib, mypaf, parser, vb


## dbreader
##-------------------------------------------------------------------
class dbreader:

	vb     = None

	dbs    = []
	#dbsreq = ["datasets", "samples", "hstyles"]
	dbsreq = []
	header = []
	path   = ""


	## __init__
	##---------------------------------------------------------------
	def __init__(self, mypaf):
		## initializes and loads the dbreader class

		self.vb     = mypaf.vb
		self.vb.call("dbreader", "__init__", [self, mypaf], "Initializing the dbreader class.")

		self.path   = mypaf.path + "db/"

		self.check()
		self.prepare()
		self.load()


	## check
	##---------------------------------------------------------------
	def check(self):
		## checks if the database directory exists and if all the 
		## required database files exist 

		self.vb.call("dbreader", "check", [self], "Performing basic functioning checks.")

		if not os.path.isdir(self.path): 
			self.vb.error("database directory does not exist")
		for db in self.dbsreq:
			if not os.path.isfile(self.path + db + ".db"): 
				self.vb.error("required database file does not exist")	 


	## get
	##---------------------------------------------------------------
	def get(self, dbname, selection, columns = "all"): 
		## returns the columns given by vars of all entries in the db
		## file that match region and accessor selection
		## separate individual columns with ":", define a range with "-"
		## or ask for all columns using "all"
		## ATTENTION: this function shall only be accessed via getAll,
		## getColumn or getVar

		self.vb.call("dbreader", "get", [self, dbname, selection, columns], "Retrieving information from the database.")

		dbname = dbname.strip()
		result = []
	
		if dbname not in self.dbs: 
			self.vb.error("database does not exist")

		collection = getattr(self, dbname)	
		header     = self.getHeader(dbname)
		
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
	def getAll(self, db, selection, columns = "all"):
		## returns the columns given by vars of all entries in the db
		## that match the region and pass the selection
		## separate individual columns with ":", define a range with "-"
		## or ask for all columns using "all"

		self.vb.call("dbreader", "getAll", [self, db, selection, columns], "Retrieving a matrix from the database.")	
		return self.get(db, selection, columns)
	
	
	## getColumn
	##--------------------------------------------------------------- 
	def getColumn(self, db, selection, column = "first"):
		## returns a single column according to column of all entries in
		## the db that match region and pass the selection
		
		self.vb.call("dbreader", "getColumn", [self, db, selection, column], "Retrieving a column vector from the database.")	
		matrix = self.get(db, selection, column) 
		if len(matrix)>0:
			return [l[0] for l in matrix]
		return []


	## getHeader
	##--------------------------------------------------------------- 
	def getHeader(self, db):
		
		self.vb.call("dbreader", "getHeader", [self, db], "Getting the header labels for a given database.")	
		idx = lib.findElm(self.dbs, db)
		return self.header[idx].list	
	

	## getRow
	##--------------------------------------------------------------- 
	def getRow(self, db, selection, row = "first"):
		## returns a single row according to row of all entries in
		## the db that match region and pass the selection
	
		self.vb.call("dbreader", "getRow", [self, db, selection, row], "Retrieving a row vector from the database.")	
		matrix = self.get(db, selection, "all") 
		if len(matrix)>0:
			if   row == "first": return matrix[0]
			elif row == "last" : return matrix[len(matrix)-1]
			else               : return matrix[int(row)] 
		return []

	
	## getVar
	##--------------------------------------------------------------- 
	def getVar(self, db, selection, column = "first"):
		## returns column var of the first entry in the db that
		## matches the region and passes the selection
		
		self.vb.call("dbreader", "getVar", [self, db, selection, column], "Retrieving a cell (variable) from the database.")	
		column = self.getColumn(db, "name=='" + selection + "'", column)
		if len(column)>0:
			return column[0]
		return ""


	## load
	##---------------------------------------------------------------
	def load(self):
		## loads the database

		self.vb.call("dbreader", "load", [self], "Loading all databases.")	
		for db in self.dbs:
			f = open(self.path + db + ".db", "r")
			lines = f.readlines()
			f.close()

			for i, line in enumerate(lines):
					
				line = line.strip()
				line = line.strip("\n")
				if len(line) == 0: continue
				if line[0] == "#": continue

				cols = line.split(":=")
				cols = [cell.strip().strip("\t") for cell in cols]
				if i == 0: self.header.append(clist.clist(cols))
				else     : eval("self." + db + ".append(cols)")


	## prepare
	##---------------------------------------------------------------
	def prepare(self):
		## prepares the database for loading, i.e. gets a list of all
		## databases available and prepares the cache

		self.vb.call("dbreader", "prepare", [self], "Preparing the dbreader for loading the databases.")	
		dbs = [f[f.rfind("/")+1:f.rfind(".")] for f in os.listdir(self.path) if os.path.isfile(self.path + f)]
		for db in dbs:
			setattr(self, db, [])
			self.dbs.append(db)


	## reload
	##---------------------------------------------------------------
	def reload(self):
		## clears the cache and reloads the databases

		self.vb.call("dbreader", "reload", [self], "Re-loading all databases.")
		prepare()
		load()


