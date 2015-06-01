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


## effmap
##------------------------------------------------------------------- 
class effmap:

	
	## CH: to be rewritten completely


	## __init__
	##---------------------------------------------------------------
	def __init__(self, name, sources, categories):

		self.name    = name.strip()

		self.samples.extend(samples)
		self.cuts   .extend(cuts)

		self.stats   = [[0 for cut in cuts] for sample in samples]


	## count
	##---------------------------------------------------------------
	def count(self, sample):

		if sample in self.samples:
			i = lib.findElm(self.samples, sample)
			self.stats[0][0] += 1
			self.stats[i][0] += 1


	## count
	##---------------------------------------------------------------
	def count(self, sample, cut):

		if sample in self.samples and cut in self.cuts: 
			i = lib.findElm(self.samples, sample)
			j = lib.findElm(self.cuts, cut)
			self.stats[0][j] += 1
			self.stats[i][j] += 1


	## efficiency
	##---------------------------------------------------------------
	def efficiency(self, cut, total = False):

		if cut in self.cuts:
			j = lib.findElm(self.cuts, cut)			
			if total: previous = self.stats[0][0]
			else:     previous = self.stats[0][j-1]
			current  = self.stats[0][j]
			return current / previous
		return 0.0


	## efficiency
	##---------------------------------------------------------------
	def efficiency(self, sample, cut, total = False):

		if sample in self.samples and cut in self.cuts:
			i = lib.findElm(self.samples, sample)
			j = lib.findElm(self.cuts, cut)
			if total: previous = self.stats[i][0]
			else:     previous = self.stats[i][j-1]
			current  = self.stats[i][j]
			return current / previous
		return 0.0


	## exportEff
	##---------------------------------------------------------------
	def exportEff(self):

		self.text = ""




	## exportStats
	##---------------------------------------------------------------
	def exportStats(self):

		for i, sample in enumerate(self.samples):

			text  = "Cut flow for selection " + self.name + " on sample " + sample + ":\n"
			total = self.stats[i][0] 

			for j, cut in enumerate(self.cuts[i]):

				text += "Cut " + cut + ": " + str(self.stats[i][j]) + " (" + str(self.efficiency(sample, cut, False)) + ", " + str(self.efficiency(sample, cut, True)) + "\n"

		return text	


