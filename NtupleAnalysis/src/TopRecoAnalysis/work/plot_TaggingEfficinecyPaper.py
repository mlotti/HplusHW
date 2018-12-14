#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plot_Efficiency.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_Efficiency.py -m MyHplusAnalysis_180202_fullSignalQCDtt --folder topbdtSelection_ --url
./plot_Efficiency.py -m MyHplusAnalysis_180202_fullSignalQCDtt --folder topbdtSelection_ --url
./plot_TaggingEfficinecyPaper.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400/TopRecoAnalysis_180320_BDT85 --folder topbdtSelection_ --url
./plot_TaggingEfficinecyPaper.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400/TopRecoAnalysis_180320_BDT85 --ratio


LAST USED:
./plot_TaggingEfficinecyPaper.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/BDTcutComparisonPlots_180828_BjetPt40_MassCut400_NewBDTbjetPt40GeV/TopTaggerEfficiency_180827_BDT0p40 --analysisName TopTaggerEfficiency --ratio --url


STATISTICS OPTIONS:
https://iktp.tu-dresden.de/~nbarros/doc/root/TEfficiency.html
statOption = ROOT.TEfficiency.kFCP       # Clopper-Pearson
statOption = ROOT.TEfficiency.kFNormal   # Normal Approximation
statOption = ROOT.TEfficiency.kFWilson   # Wilson
statOption = ROOT.TEfficiency.kFAC       # Agresti-Coull
statOption = ROOT.TEfficiency.kFFC       # Feldman-Cousins
statOption = ROOT.TEfficiency.kBJeffrey # Jeffrey
statOption = ROOT.TEfficiency.kBUniform # Uniform Prior
statOption = ROOT.TEfficiency.kBayesian # Custom Prior
'''
#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
from optparse import OptionParser

import getpass
import array

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck

# Ignore Runtime warnings: Base category for warnings about dubious runtime features.
import warnings
warnings.filterwarnings("ignore")

ROOT.gErrorIgnoreLevel = ROOT.kError

#================================================================================================ 
# Function Definition
#================================================================================================ 
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    aux.Print(msg, printHeader)
    return

def GetLumi(datasetsMgr):
    Verbose("Determininig Integrated Luminosity")
    
    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            lumi += d.getLuminosity()
    Verbose("Luminosity = %s (pb)" % (lumi), True)
    return lumi

def GetListOfQCDatasets():
    return ["QCD_HT1000to1500",
            "QCD_HT1500to2000_ext1",
            "QCD_HT2000toInf",
            "QCD_HT2000toInf_ext1",
            "QCD_HT200to300",
            "QCD_HT200to300_ext1",
            "QCD_HT1000to1500_ext1",
            "QCD_HT100to200",
            "QCD_HT1500to2000",
            "QCD_HT500to700_ext1",
            "QCD_HT50to100",
            "QCD_HT700to1000",
            "QCD_HT700to1000_ext1",
            "QCD_HT300to500",
            "QCD_HT300to500_ext1",
            "QCD_HT500to700"
            ]
#    return ["QCD_bEnriched_HT200to300",
#            "QCD_bEnriched_HT300to500",
#            "QCD_bEnriched_HT500to700",
#            "QCD_bEnriched_HT700to1000",
#            "QCD_HT1000to1500",
#            "QCD_bEnriched_HT1000to1500",
#            "QCD_bEnriched_HT1500to2000",
#            "QCD_bEnriched_HT2000toInf",
#            "QCD_HT1500to2000_ext1",
#            "QCD_HT2000toInf",
#            "QCD_HT2000toInf_ext1",
#            "QCD_HT200to300",
#            "QCD_HT200to300_ext1",
#            "QCD_HT1000to1500_ext1",
#            "QCD_HT100to200",
#            "QCD_HT1500to2000",
#            "QCD_HT500to700_ext1",
#            "QCD_HT50to100",
#            "QCD_HT700to1000",
#            "QCD_HT700to1000_ext1",
#            "QCD_HT300to500",
#            "QCD_HT300to500_ext1",
#            "QCD_HT500to700"
#            ]


def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


def GetDatasetsFromDir(opts):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def GetDatasetsFromDir_second(opts, useMcrab):
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([useMcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([useMcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([useMcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    



def GetHistoKwargs(opts):
    units = "GeV" # not GeV/c

    kwargs = {
        #"xlabel"           : "generated top p_{T} (%s)" % (units),
        # "xlabel"           : "candidate p_{T} (%s)" % (units),
        "xlabel"           : "p_{T} (%s)" % (units),
        "ylabel"           : "Efficiency / " + units,
        # "ylabel"           : "Misidentification rate / " + units,
        # "rebinX"           : 1,
        # "rebinX"           : systematics._dataDrivenCtrlPlotBinning["LdgTrijetDijetMass_AfterAllSelections"],
        "ratioYlabel"      : "Ratio ",
        "ratio"            : opts.ratio,
        "ratioInvert"      : True,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        #"cmsExtraText"     : "Preliminary",
        "cmsExtraText"     : "Simulation",
        #"opts"             : {"ymin": 0.0, "ymax": 1.0},
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.2},
        #"opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "opts2"            : {"ymin": 0.0, "ymax": 10.4},
        "moveLegend"       : {"dx": -0.05, "dy": -0.0, "dh": -0.15},
        "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
        }
    myBins  = [0, 100, 150, 200, 300, 400, 500, 600, 800]

    if len(myBins) > 0:
        kwargs["binList"] = array.array('d', myBins)
    return kwargs


def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(False)
    style.setGridY(False)
    
    # If user does not define optimisation mode do all of them
    if opts.optMode == None:
        if len(optList) < 1:
            optList.append("")
        else:
            pass
        optModes = optList
    else:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        datasetsMgr40 = GetDatasetsFromDir_second(opts, opts.mcrab.replace("_BDT85", "_BDT40"))
        datasetsMgr40.updateNAllEventsToPUWeighted()
        datasetsMgr40.loadLuminosities() # from lumi.json                                                                                                                           

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for datasetsMgr_ in [datasetsMgr, datasetsMgr40]:
            for d in datasetsMgr_.getAllDatasets():
                if "ChargedHiggs" in d.getName():
                    datasetsMgr_.getDataset(d.getName()).setCrossSection(1.0)

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        if 0:
            plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Print dataset information before removing anything?
        if 0:
            datasetsMgr.PrintInfo()

        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        else:
            intLumi = 35920

        # Remove datasets
        filterKeys = ["Data", "TTZToQQ", "TTWJets", "TTTT"]
        #filterKeys = ["Data", "TTZToQQ", "TTWJets", "TTTT"]
        for key in filterKeys:
            datasetsMgr.remove(filter(lambda name: key in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr40.remove(filter(lambda name: key in name, datasetsMgr40.getAllDatasetNames()))
        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            datasetOrder.append(d.getName())
            
        # Select and re-order
        datasetsMgr.selectAndReorder(datasetOrder)
        datasetsMgr40.selectAndReorder(datasetOrder)

        # Print dataset information
        datasetsMgr.PrintInfo()

        # QCD multijet
        datasetsMgr.merge("QCD", GetListOfQCDatasets())
        datasetsMgr40.merge("QCD", GetListOfQCDatasets())
        plots._plotStyles["QCD"] = styles.getQCDLineStyle()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # For-loop: All numerator-denominator pairs
        PlotEfficiency(datasetsMgr, datasetsMgr40, intLumi)
    return


def PlotEfficiency(datasetsMgr, datasetsMgr40, intLumi):
  
    # Definitions
    myList  = []

    dataset_TT    = datasetsMgr.getDataset("TT")
    dataset40_TT  = datasetsMgr40.getDataset("TT")
    dataset_QCD   = datasetsMgr.getDataset("QCD")
    dataset40_QCD = datasetsMgr40.getDataset("QCD")

    # Efficiency
    hNumerator   = os.path.join(opts.folder, "AllTopQuarkPt_MatchedBDT")    
    hDenominator = os.path.join(opts.folder, "TopQuarkPt") #AllTopQuarkPt_Matched
    n_TT = dataset40_TT.getDatasetRootHisto(hNumerator)
    n_TT.normalizeToLuminosity(intLumi)
    num40_TT = n_TT.getHistogram()  

    d_TT = dataset40_TT.getDatasetRootHisto(hDenominator) 
    d_TT.normalizeToLuminosity(intLumi)
    den40_TT = d_TT.getHistogram()    

    # Misidentification rate
    hNumerator   = os.path.join(opts.folder, "TrijetFakePt_BDT")    
    hDenominator = os.path.join(opts.folder, "TrijetFakePt")    
    n_QCD = dataset40_QCD.getDatasetRootHisto(hNumerator)
    n_QCD.normalizeToLuminosity(intLumi)
    num40_QCD = n_QCD.getHistogram()  

    d_QCD = dataset40_QCD.getDatasetRootHisto(hDenominator)
    d_QCD.normalizeToLuminosity(intLumi)
    den40_QCD = d_QCD.getHistogram()    

    # Customise binning
    _kwargs = GetHistoKwargs(opts)
    if "binList" in _kwargs:
        xBins     = _kwargs["binList"]
        nx        = len(xBins)-1
        num40_TT  = num40_TT.Rebin(nx, "", xBins)
        den40_TT  = den40_TT.Rebin(nx, "", xBins)
        num40_QCD = num40_QCD.Rebin(nx, "", xBins)
        den40_QCD = den40_QCD.Rebin(nx, "", xBins)

    # Calculate efficiency
    eff40_TT = ROOT.TEfficiency(num40_TT, den40_TT)
    eff40_TT.SetStatisticOption(ROOT.TEfficiency.kFCP) 

    eff40_QCD = ROOT.TEfficiency(num40_QCD, den40_QCD)
    eff40_QCD.SetStatisticOption(ROOT.TEfficiency.kFCP) #

    eff40_TT  = convert2TGraph(eff40_TT)
    eff40_QCD = convert2TGraph(eff40_QCD)

    styles.ttStyle.apply(eff40_TT)
    styles.qcdStyle.apply(eff40_QCD)

    # Append in list
    gEff40_TT  = histograms.HistoGraph(eff40_TT , "t#bar{t}", "lp", "P")
    #gEff40_QCD = histograms.HistoGraph(eff40_QCD, "QCD multijet", "lp", "P")
    gEff40_QCD = histograms.HistoGraph(eff40_QCD, "QCD", "lp", "P")
    myList.append(gEff40_TT)
    myList.append(gEff40_QCD)
        
    # Define save name
    saveName = "TopTagEfficiency"

    # Plot the efficiency
    #p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
    p = plots.ComparisonManyPlot(gEff40_TT, [gEff40_QCD], saveFormats=[])   
    #p = plots.ComparisonPlot(gEff40_TT, gEff40_QCD, saveFormats=[])   
    plots.drawPlot(p, saveName, **_kwargs)

    # Save plot in all formats
    savePath = os.path.join(opts.saveDir,  opts.optMode)
    save_path = os.path.join(savePath, "BDT0p40")
    SavePlot(p, saveName, save_path, saveFormats = [".png", ".C", ".pdf"])
    return

def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h     = tefficiency.GetCopyTotalHisto()
    n     = h.GetNbinsX()

    # For-loop: All bins
    for i in range(1, n+1):
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))

        # ugly hack to prevent error going above 1
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
        
    graph = ROOT.TGraphAsymmErrors(n, array.array("d",x), array.array("d",y),
                                   array.array("d",xerrl), array.array("d",xerrh),
                                  array.array("d",yerrl), array.array("d",yerrh)) 
    return graph


def SavePlot(plot, saveName, saveDir, saveFormats = [".png"]):
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
#        saveNameURL = saveNameURL.replace(opts.saveDir, "http://home.fnal.gov/~%s" % (getpass.getuser()))
        saveNameURL = saveNameURL.replace("/publicweb/%s/%s" % (getpass.getuser()[0], getpass.getuser()), "http://home.fnal.gov/~%s" % (getpass.getuser()))
        #SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(savePath + ext, i==0)
        plot.saveAs(savePath, formats=saveFormats)
    return


#================================================================================================ 
# Main
#================================================================================================ 
if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''
    
    # Default Settings
    ANALYSISNAME = "TopRecoAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    RATIO        = False
    INTLUMI      = -1.0
    URL          = False
    SAVEDIR      = "/publicweb/%s/%s/%s" % (getpass.getuser()[0], getpass.getuser(), ANALYSISNAME)
    VERBOSE      = False
    NORMALISE    = False
    FOLDER       = "topbdtSelection_"
    MVACUT       = "MVA"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--ratio", dest="ratio", action="store_true", default=RATIO, 
                      help="Enables ratio pad [default: %s]" % RATIO)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", 
                      help="Normalise the histograms to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_Efficiency.py: Press any key to quit ROOT ...")
