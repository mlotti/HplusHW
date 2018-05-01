#!/usr/bin/env python
'''
DESCRIPTION:
Create to answer Abdollah's question prior to pre-approval:

Q. I see that you are sensitive before ~ 400 GeV, but after that boosted analysis gets more sensitive. It is a bit surprising. Do you expect that jets (top and/or W) get merged at Charged Higgs mass of 400 GeV? If not, then either there is an issue with your results or something wrong from their sides. Maybe a simple check would be to look at the dR between top components and W decays for M_H+=400 GeV

A. The resolved analysis is indeed sensitive to the mass of the charged Higgs boson. As the mass of H+ increases, the W/top from the H+ side become more boosted due to purely kinematical effects. Similarly, as the pt of H+ increases, its decay products become increasingly collinear, meaning that the probability they can be contained within a fat-jet also increases. This is consistent with the exclusion limit plots which show that the resolved top sensitivity is maximum for the region mH+ < 500 GeV, with the sensitivity eventually flattening out for mH+ > 1000 GeV. This effect was can verified by inspecting Figures 11 and 16 in the AN, which show the efficiency of the top candidates as a function of their pt and the invariant mass of the charged Higgs boson candidates, respectively.

Q. I am afraid you have not addressed my concern here. 400 GeV H+ will lead to a 175GeV Top and 80 GeVGeV W. Thus if H+ momentum is not so high, none of the Top or W will be highly boosted!
So here is my request: Make the dR between top product(W and b quark) and W product(two light jets) coming from H+ 400 GeV. You have to look at the generator level to make such plots.


USAGE:
./plot_Boost.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_Boost.py -m HtbKinematics_180430_031946 --intLumi 35900 --url


LAST USED:1
./plot_Boost.py -m HtbKinematics_180430_031946 -n

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck

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
    

def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(False)
    style.setGridY(False)
    
    optModes = [""]                                                                                                                             

    if opts.optMode != None:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
            if d.getName() not in opts.signalMass:
                datasetsMgr.remove(d.getName())

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Do the topSelection histos
        folder     = opts.folder 
        histoList  = datasetsMgr.getDataset(opts.signalMass[0]).getDirectoryContent(folder)
        histoPaths = [os.path.join(folder, h) for h in histoList]
        myHistos   = ["Htb_tbW_WBoson_Quark_Htb_tbW_WBoson_AntiQuark_dEta",
                      "Htb_tbW_WBoson_Quark_Htb_tbW_WBoson_AntiQuark_dPhi",
                      "Htb_tbW_WBoson_Quark_Htb_tbW_WBoson_AntiQuark_dR",
                      "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta",
                      "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi",
                      "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR",
                      "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta",
                      "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi",
                      "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR",
                      "Htb_tbW_WBoson_Htb_tbW_BQuark_dEta",
                      "Htb_tbW_WBoson_Htb_tbW_BQuark_dPhi",
                      "Htb_tbW_WBoson_Htb_tbW_BQuark_dR"]



        # For-loop: All histos in folder
        counter = 0
        for i, histo in enumerate(histoPaths, 1):
            h = histo.split("/")[-1] 
            if h not in myHistos:
                continue
            counter +=1 
            # Print("Plotting histogram %s" % (histo), counter==1)
            PlotMC(datasetsMgr, histo)
    return

def PlotMC(datasetsMgr, histo):

    kwargs = {}
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    p.setLuminosity(opts.intLumi)

    p1 = "a"
    p2 = "b"
    if "Htb_tbW_WBoson_Quark_Htb_tbW_WBoson_AntiQuark" in histo:
        p1 = "q_{1}"
        p2 = "q_{2}"
    if "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark" in histo:
        p1 = "b_{2}"
        p2 = "q_{1}"
    if "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark" in histo:
        p1 = "b_{2}"
        p2 = "q_{2}"        
    if "Htb_tbW_WBoson_Htb_tbW_BQuark_dR" in histo:
        p1 = "W^{+}"
        p2 = "q_{2}"

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _format = "%0.0f"
    _xlabel = None
    _format = "%0.2f"
    _logY   = True
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}
    
    if "pt" in histo.lower():
        _format = "%0.0f"
        _rebinX = 2
        _format = "%0.0f GeV/c"

    if "eta" in histo.lower():
        _cutBox = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmin"] = -3.0
        _opts["xmax"] = +3.0

    if "dPhi" in histo:
        _format = "%0.2f"
        _opts["xmin"]  =  0.0
        _opts["xmax"]  = +3.2
        _xlabel = "#Delta#phi(%s, %s)" % (p1, p2)

    if "dEta" in histo:
        _format = "%0.2f"
        _opts["xmin"] = 0.0
        _opts["xmax"] = 3.2
        _xlabel = "#Delta#eta(%s, %s)" % (p1, p2)

    if "dR" in histo:
        _format = "%0.2f"
        _rebinX = 2
        _opts["xmin"] = 0.0
        _opts["xmax"] = 5.0
        _cutBox = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "#DeltaR(%s, %s)" % (p1, p2)

    if _logY:
        _opts["ymaxfactor"] = 2.0
    else:
        _opts["ymaxfactor"] = 1.2

    if opts.normaliseToOne:
        _opts["ymin"] = 1e-3
    else:
        _opts["ymin"] = 1e0

    # Customise Dataset styling
    for signal in opts.signalMass:
        m = signal.split("M_")[-1]
        p.histoMgr.forHisto(signal, styles.getSignalStyleHToTB_M(m))

    # Draw the customised plot
    plots.drawPlot(p, 
                   histo,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = _logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.60, "y1": 0.72, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   addLuminosityText = (opts.intLumi!=-1),
                   ratio        = False,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )
        
    if 0:
        histograms.addText(0.20, 0.88, "test", 27)

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    saveDict     = {}
    saveDict["Htb_tbW_WBoson_Htb_tbW_BQuark_dR"] = "dR_W_b2"
    saveDict["Htb_tbW_WBoson_Quark_Htb_tbW_WBoson_AntiQuark_dR"] = "dR_q1_q2"
    saveDict["Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR"] = "dR_b2_q1"
    saveDict["Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR"] =  "dR_b2_q2"
    savePath = os.path.join(opts.saveDir, histo.split("/")[0], "", opts.optMode)
    if saveName in saveDict.keys():
        SavePlot(p, saveDict[saveName], savePath) 
    else:
        SavePlot(p, saveName, savePath) 
    return


def SavePlot(plot, saveName, saveDir, saveFormats = [".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
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
    ANALYSISNAME = "HtbKinematics"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    #SIGNALMASS   = [200, 500, 2000]
    SIGNALMASS   = [500]#, 1000]
    INTLUMI      = -1.0
    MERGEEWK     = False
    URL          = False
    SAVEDIR      = "/publicweb/a/aattikis/" + ANALYSISNAME
    VERBOSE      = False
    NORMALISE    = False
    FOLDER       = "TH1"
    
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

    #parser.add_option("--signalMass", dest="signalMass", type=float, default=SIGNALMASS, 
    #                  help="Mass value of signal to use [default: %s]" % SIGNALMASS)

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

    # Sanity check
    if opts.mergeEWK:
        Print("Merging EWK samples into a single Datasets \"EWK\"", True)

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    opts.signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        opts.signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotMC_Top.py: Press any key to quit ROOT ...")
