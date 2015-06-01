inputs:
* tree
* file (root hists)
* histogram (root)
* event yields
* object yields
* selection

selections:
* variables and cuts
* file (root hists)
* histogram (root)
* event lists
* object lists

outputs:
* tree
* file (root hists)
* histogram (eps, pdf, png)
* histogram (root)
* event lists
* object lists
* event yields
* object yields
* efficiencymap

objects:
* trees
* histograms
* evlist
* evyield
* oblist
* obyield
* effmap
* roc

MYPAF:
* 1 tree:   tree                  -> tree
* 2 draw:   tree                  -> file (root hists)
            tree                  -> histogram (eps, pdf, png)
            tree                  -> histogram (root)
* 3 plot:   file (root hists)     -> file (root hists)
            file (root hists)     -> histogram (eps, pdf, png)
            file (root hists)     -> histogram (root)
            histogram (root)      -> file (root hists)
            histogram (root)      -> histogram (eps, pdf, png)
            histogram (root)      -> histogram (root)
* 4 scan:   tree                  -> event lists
            tree                  -> object lists
* 5 stat:   tree                  -> event yields
            tree                  -> object yields
            tree                  -> efficiency map
            tree                  -> roc curve
* 6 hist:   any tier2 output      -> file (root hists)
            any tier2 output      -> histogram (eps, pdf, png)
            any tier2 output      -> histogram (root) 
* 7 publ:   event yields          -> datacards for higgscombined
            any tier2 output      -> latex tables
            any tier2 output      -> keynote slides 

THREE TIER-MODULE-SYSTEM:
* tiers reflect the workflow of MyPAF, modules reflect the actual tasks
* first  tier has one  module : tree
* second tier has four modules: draw, plot, scan, stat
* third  tier has one  module : hist

TIER PURPOSE:
* first : subsetting of a ROOT TTree and adding variables, increasing speed of tier2 and tier3, adding variables needed in tier2 and tier3
* second: producing first set of outputs from TTree, first look inside the TTree, ``categorizing'' what is in there
* third : treating and editing the outputs produced in tier2, publication of things 

MODULE PURPOSE:
* draw: only drawing from tree, TTree::Draw
* hist: reading the buffers and doing the schemes 
* plot: combining histograms, drawing histograms from root files, yields or efficiencies
* scan: only scanning trees, TTree::Scan, for quick use
* stat: studying the selection
* tree: only event-by-event selection, skim trees, add variables to tree, merge friends  

RUN-SCHEME OPTION:
* having at least one scheme in the config file one needs to first run the tier2 schemes necessary in order
  to run tier3
* in order not having to do this manually, MyPAF knows a run-scheme option that checks the config file for
  any potential scheme and then runs the tier2 modules neccessary to run the schemes 

REMARKS:
* every selection produces event yields, object yields and efficiencies, but always unchangeable format
* everything that is configurable is configurable in the cfg file
* every cfg file can be used by every of the 5 modules, variables and secions are unique
* separator (except for lists) always is ":="
* accessor (db, selection, etc) always is "::"
* db files always have the column names in first row

CONFIGURATION:
* head
  - genmatch     : to use gen matching in every sample, options are basic (fakes, misId, prompt),
                                                                    raw (fakes: heavy, light; misId, prompt),
                                                                    fine (fakes: b, c, light, tau; misId, prompt),
                                                                    none (no gen matching), default is none
  - grouping     : to group the output of the samples, options are dataset (qcd Mu, qcd EM, etc), 
                                                                   group (rares, qcd, etc), 
                                                                   gengroup (fakes, prompt, etc), 
                                                                   none (no grouping of the samples), default is none
  - inputdir     : default dir for all the inputs, relative to MyPAF/input/
  - inputtree    : default tree name for all the input trees
  - logscale     : y for everything in log scale, false otherwise
  - normalization: option to normalize samples (lumi-value, unity, data)
  - outputdir    : default dir for all the output, relative to MyPAF/output/
  - outputtree   : default tree name for all the output trees
  - overflow     : display overflow and underflow bins or not
  - systematics  : default is n
  - format: name := value
* selection
  - variables and cuts as used in TTree::Draw
  - access files (root hists) by: FILE[path]::variable::sample::bin
  - access histograms (root)  by: HIST[path]::canvas::histogram::bin
  - access event lists        by: EVENTLIST[path]
  - access object lists       by: OBJECTLIST[path]
  - format: type := name := definition := arguments
  - type: tree, file, root, evlist, oblist
  - args: obj
* input
  - format: type := name := path := args
  - type: tree, file, root, evlist, evyields, oblist, obyields, number
  - args: dir, tree, data 
  - it is important that the args are separated by a blank space and there is only a = between key and value
* output
  - format: type := name := definition := args
  - type: tree, file, plot, root, evlist, oblist, evyields, obyields, effmap
  - definition: tree variable to draw, accessor for hist
  - making histograms, access files (root hists) by: FILE[name]::directory/histogram
  - making histograms, access histograms (root)  by: HIST[name]::canvas::histogram
  - args (tree): dtype (datatype)
  - args (plot): style, log (y,n), note, grid, scale, ratio, errors, norm, draw2mode, draw1mode, nxbins, xmin, xmax, xbins, nybins, ... 
  - args (plot taken from hist/root file): source
  - e.g. old tree variables: tree := lep.pt := LepGood_pt (if no datatype given, take the one of LepGood_pt)
  - e.g. new tree variables: tree := lep.pt2 := 10 (if no datatype given, take a float)
  - e.g. newly computed variable: tree := minMllSFSS := min(mll(SSSS))
  - it is important that the args are separated by a blank space and there is only a = between key and value
* schemes
  - format: scheme := name := definition := args
  - scheme: add, sub, div, mult, proj, eyhist, oyhist, elhist, olhist, roc, comp, cratio, stack, datamc, tfit, ffit
  - definition: histograms that enter the scheme (e.g. the summands of 'add')
  - args: additional arguments defining the output of the scheme (legend name 1, legend name 2, style)
  - since schemes always are stored in the root file and are saved as plots, also all plot variables apply
  - schemes take several objects using the names defined in the config file
  - outcome is new object that directly is saved to disk after its creation
  - note: schemes also should be available for other usage? or not? (e.g. stack)

OUTPUT FORMATS:
* file (root hists): histograms per variable and sample given in "variable/sample"
* histogram (root): single histogram stored in canvas
* event lists: separator is ":", run:lumi:evt always fixed, additional variables configurable
* object lists: separator is ":", run:lumi:evt:instance always fixed, one list per object
* event yields: separator is ":=" 

DATABASE:
* groups (combination of samples)
  - format: type := name := lname := color := linestyle
  - type: dataset, bggroup, gengroup
  - dataset: combines different bins of DY to one DY sample
  - bggroup: combines different rare SM samples to one rare SM 
  - gengroup: combines gen categories (fakes, rares, misId)

* observables (physics observables):
  - format: name := lname := parent := nbins := min := max
  - e.g. LepGood_pt := P_T(lep) := lep := 5 := 10 := 120
* samples (dataset as given by DAS, e.g. "DYJets HT100-200")
  - format: name := lname := dataset := bggroup := gengroup := color := xsec := nevents := ngenevents := datasetname
  - e.g. QCD_EM20-30 := QCD 20-30 (EM) := QCDe := QCD := fakes := FF9933 := 100. := 24000 := 25000 := /QCD_Pt20to30_EMEnriched_.../../MINIAODSIM



------------------
OLD THINGS:
* datasets (logical combination of samples, e.g. "QCD")
  - format: name := lname := color
  - e.g. QCD := QCD := ROOT.kBlue
* groups (typical groups of datasets, e.g. "MC", "rares"):
  - format: name := lname := parent
  - e.g. rares := rares := MC
* gengroups (gen-matched mc groups, "fakes", "misId", "prompt")
* 
* schemes (information in an output, name needs to match function in dblib/schemes)
* styles (way how information is presented in an output, name needs to match function in dblib/styles)
  - format: type := name := arguments (separated by :)
  - 
* histograms
  -> what do you want to show? => scheme
  -> how do you want to show it? => style
* histogram schemes:
* histogram styles
  - format: scheme - draw option - scale option - 
=> histschemes
  - single (hist, one group, entries per one quantity)
  - mult (hist, at least two groups)
  - shape (normalized lines, at least two groups, )
  - roc (at least one group, two quantities)
  - corr (2d scatter, one group, two quantities)
  - map (2d plot, one group, three quantities)
------------------
