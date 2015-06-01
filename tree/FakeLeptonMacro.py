import ROOT, os, subprocess
from lib import lib

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.TGaxis.SetMaxDigits(3)


#samples = [["QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root"                     , "qcdmu", 1.347e+05]]
#samples = [["2015/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6-mdunser-V03-09-00.root", "qcdel", 2.91e+06 ], \
#           ["2015/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root"                  , "qcdel", 4615893.0], \
#           ["2015/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root"                 , "qcdel", 183448.7 ], \
#           ["2015/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6-V03-09-01.root"             , "qcdel", 1.67e+05 ], \
#           ["2015/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6-V03-09-01.root"             , "qcdel", 1.67e+05 ], \
#           ["2015/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6-V03-09-01.root"            , "qcdel", 12.98e+03]]
samples = [["TTJets_complete.root"                                                       , "ttbar", 245.0    ]]
#samples = [["QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root"                     , "qcdmu", 1.347e+05], \
#           ["TTJets_complete.root"                                                       , "ttbar", 245.0    ], \
#           ["2015/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6-mdunser-V03-09-00.root", "qcdel", 2.91e+06 ], \
#           ["2015/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root"                  , "qcdel", 4615893.0], \
#           ["2015/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root"                 , "qcdel", 183448.7 ], \
#           ["2015/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6-V03-09-01.root"             , "qcdel", 1.67e+05 ], \
#           ["2015/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6-V03-09-01.root"             , "qcdel", 1.67e+05 ], \
#           ["2015/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6-V03-09-01.root"            , "qcdel", 12.98e+03]]
path = "/scratch/cheidegg/minitrees_spring14/"


_c = lib.makeCanvas(900, 675)
_p = lib.makePad('tot')

h_el_loose = []
h_el_lnt   = []
h_el_tight = []
h_mu_loose = []
h_mu_lnt   = []
h_mu_tight = []


for s, sample in enumerate(samples):

	h_el_loose.append(ROOT.TH1F("h_el_loose_" + sample[1] + str(s), "Provenance_El_Loose_" + sample[1] + str(s), 6, 0, 6)) 
	h_el_lnt  .append(ROOT.TH1F("h_el_lnt_"   + sample[1] + str(s), "Provenance_El_LNT_"   + sample[1] + str(s), 6, 0, 6)) 
	h_el_tight.append(ROOT.TH1F("h_el_tight_" + sample[1] + str(s), "Provenance_El_Tight_" + sample[1] + str(s), 6, 0, 6)) 
	h_mu_loose.append(ROOT.TH1F("h_mu_loose_" + sample[1] + str(s), "Provenance_Mu_Loose_" + sample[1] + str(s), 6, 0, 6)) 
	h_mu_lnt  .append(ROOT.TH1F("h_mu_lnt_"   + sample[1] + str(s), "Provenance_Mu_LNT_"   + sample[1] + str(s), 6, 0, 6)) 
	h_mu_tight.append(ROOT.TH1F("h_mu_tight_" + sample[1] + str(s), "Provenance_Mu_Tight_" + sample[1] + str(s), 6, 0, 6)) 

	print "looping on " + path + sample[0]
	f = ROOT.TFile(path + sample[0], "read")
	t = f.Get("Analysis")
	nmax = t.GetEntries()

	weight = 8100. * sample[2] / nmax

	ii = 0
	for evt in t:

		if ii % 1000 == 0: print "processing event " + str(ii)
#		if ii == 20000: break

		el_loose_idx = []
		el_loose_orn = []
		el_lnt_idx = []
		el_lnt_orn = []
		el_tight_idx = []
		el_tight_orn = []
		jet_idx = []
		jet_away_idx = []
		mu_loose_idx = []
		mu_loose_orn = []
		mu_lnt_idx = []
		mu_lnt_orn = []
		mu_tight_idx = []
		mu_tight_orn = []

		# electrons
		for i in range(len(evt.ElPt)):

			
			# loose electrons
			if evt.ElPt[i] < 10.: continue
			if not evt.ElIsLoose[i]: continue
			if evt.ElPFIso[i] > 0.6: continue
			el_loose_idx.append(i)
			el_loose_orn.append(lib.getLeptonOrigin(evt.ElMID[i], evt.ElGMID[i]))
			
			# loose-not-tight electrons
			if not evt.ElIsTight[i] or evt.ElPFIso[i] > 0.15:
				el_lnt_idx.append(i)
				el_lnt_orn.append(lib.getLeptonOrigin(evt.ElMID[i], evt.ElGMID[i]))

			# tight electrons:
			else:
				el_tight_idx.append(i)
				el_tight_orn.append(lib.getLeptonOrigin(evt.ElMID[i], evt.ElGMID[i]))
		

		# muons
		for i in range(len(evt.MuPt)):
			
			# loose muons
			if evt.MuPt[i] < 10.: continue
			if not evt.MuIsLoose[i]: continue
			mu_loose_idx.append(i)		
			mu_loose_orn.append(lib.getLeptonOrigin(evt.MuMID[i], evt.MuGMID[i]))
			
			# loose-not-tight muons
			if not evt.MuIsTight[i]: 
				mu_lnt_idx.append(i)
				mu_lnt_orn.append(lib.getLeptonOrigin(evt.MuMID[i], evt.MuGMID[i]))

			# tight muons
			else:
				mu_tight_idx.append(i)
				mu_tight_orn.append(lib.getLeptonOrigin(evt.MuMID[i], evt.MuGMID[i]))

		# jets
		for i in range(len(evt.JetPt)):
			if evt.JetPt[i] < 40.: continue
			if evt.JetEta[i] > 2.5: continue
			
			dr_cache = 999.
			for el in el_loose_idx:
				dr = lib.dR(evt.ElEta[el], evt.JetEta[i], evt.ElPhi[el], evt.JetPhi[i])
				if dr < dr_cache: dr_cache = dr
			for mu in mu_loose_idx:
				dr = lib.dR(evt.MuEta[mu], evt.JetEta[i], evt.MuPhi[mu], evt.JetPhi[i])
				if dr < dr_cache: dr_cache = dr
			if dr_cache < 0.4: continue

			jet_idx.append(i)



		# fill provenance histograms for NOT-AES
		for origin in el_loose_orn:
			#h_el_loose[s].Fill(0)
			h_el_loose[s].Fill(origin)
		for origin in el_lnt_orn:
			#h_el_lnt[s]  .Fill(0)
			h_el_lnt[s]  .Fill(origin)
		for origin in el_tight_orn:
			#h_el_tight[s].Fill(0)
			h_el_tight[s].Fill(origin)
		for origin in mu_loose_orn:
			#h_mu_loose[s].Fill(0)
			h_mu_loose[s].Fill(origin)
		for origin in mu_lnt_orn:
			#h_mu_lnt[s]  .Fill(0)
			h_mu_lnt[s]  .Fill(origin)
		for origin in mu_tight_orn:
			#h_mu_tight[s].Fill(0)
			h_mu_tight[s].Fill(origin)



	
		# measurement region selection

		#if len(mu_loose_idx) + len(el_loose_idx) > 1: continue

		#if len(mu_loose_idx) == 1:
		#	if evt.MuPt[mu_loose_idx[0]] < 20.: continue 
		#	MT = lib.getMT(evt.MuPt[mu_loose_idx[0]], evt.pfMET1, evt.MuPhi[mu_loose_idx[0]], evt.pfMET1Phi)
		#	origin = lib.getLeptonOrigin(evt.MuMID[mu_loose_idx[0]], evt.MuGMID[mu_loose_idx[0]]) 
		#	filltight = (len(mu_tight_idx) == 1 and mu_loose_idx[0] == mu_tight_idx[0])
		#	for jet in jet_idx:
		#		dr = lib.dR(evt.MuEta[mu_loose_idx[0]], JetEta[jet], evt.MuPhi[mu_loose_idx[0]], JetPhi[i])
		#		if dr < 1.0: continue
		#		jet_away_idx.append(jet)

		#if len(el_loose_idx) == 1:
		#	if evt.ElPt[el_loose_idx[0]] < 20.: continue
		#	MT = lib.getMT(evt.ElPt[el_loose_idx[0]], evt.pfMET1, evt.ElPhi[el_loose_idx[0]], evt.pfMET1Phi)
		#	origin = lib.getLeptonOrigin(evt.ElMID[el_loose_idx[0]], evt.ElGMID[el_loose_idx[0]]) 
		#	filltight = (len(el_tight_idx) == 1 and el_loose_idx[0] == el_tight_idx[0])
		#	for jet in jet_idx:
		#		dr = lib.dR(evt.ElEta[el_loose_idx[0]], JetEta[jet], evt.ElPhi[el_loose_idx[0]], JetPhi[i])
		#		if dr < 1.0: continue
		#		jet_away_idx.append(jet)

		#if len(jet_away_idx) < 1: continue

		#if evt.pfMET1 > 20.: continue

		#if MT > 20.: continue

		#h_aes_loose.Fill(0)
		#h_aes_loose.Fill(origin)

		#if filltight:
		#	h_aes_tight.Fill(0)
		#	h_aes_tight.Fill(origin)		
		ii+=1

	f.Close()


groups = []
hists  = []
labels  = ['all', 'W', 'B', 'C', 'U/D/S', 'unm.']

for i, sample in enumerate(samples):
	j = -1

	for j, group in enumerate(groups):
		if group == sample[1]:
			idx = j
	if j > -1:
		hists[j][0].Add(h_el_loose[i])
		hists[j][1].Add(h_el_lnt  [i])
		hists[j][2].Add(h_el_tight[i])
		hists[j][3].Add(h_mu_loose[i])
		hists[j][4].Add(h_mu_lnt  [i])
		hists[j][5].Add(h_mu_tight[i])
	else:
		groups.append(sample[1])
		hists.append([h_el_loose[i], h_el_lnt[i], h_el_tight[i], h_mu_loose[i], h_mu_lnt[i], h_mu_tight[i]])
		hists[-1][0].SetTitle("Provenance_El_Loose_" + sample[1])
		hists[-1][1].SetTitle("Provenance_El_LNT_"   + sample[1])
		hists[-1][2].SetTitle("Provenance_El_Tight_" + sample[1])
		hists[-1][3].SetTitle("Provenance_Mu_Loose_" + sample[1])
		hists[-1][4].SetTitle("Provenance_Mu_LNT_"   + sample[1])
		hists[-1][5].SetTitle("Provenance_Mu_Tight_" + sample[1])

for hist in hists:
	for i in range(len(hist)):
		#hist[i].Draw("hist text")
		#lib.saveCanvas(_c, _p, "/shome/cheidegg/FRstuff/output/", hist[i].GetTitle()+"_test")
		hp = lib.makeProvenancePlots(hist[i], labels, [3,4,5,6]) 
		hp[0].Draw("hist text")
		for k in range(1, len(hp)): hp[k].Draw("hist text same")
		lib.saveCanvas(_c, _p, "/shome/cheidegg/FRstuff/output/", hist[i].GetTitle()) 


