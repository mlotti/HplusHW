#!/usr/bin/env python
'''
DESCRIPTIONM:
Script that plots FakeB measurement purity plots created with the FakeB pseudo-dataset.
This pseudo-dataset was generated with the makeInvertedPseudomMulticrab.py script with 
the following command:
./makeInvertedPseudoMulticrab.py -m <FakeBMeasurement_Pseudomilticrab> FakeB --analysisName FakeB


USAGE:
./plot_Purity.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plot_Purity.py -m Hplus2tbAnalysis_3bjets40_MVA0p88_MVA0p88_TopMassCutOff600GeV_180113_050540/ --gridX --gridY --url

LAST USED:
./plot_Purity.py -m Hplus2tbAnalysis_3bjets40_MVA0p88_MVA0p88_TopMassCutOff600GeV_180113_050540/ --`gridX --gridY

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import array
import re
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
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

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
    Print(msg, printHeader)
    return

def rchop(myString, endString):
  if myString.endswith(endString):
    return myString[:-len(endString)]
  return myString

def GetDatasetsFromDir(opts):
    datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab], dataEra=opts.dataEra, searchMode=opts.searchMode, analysisName=opts.analysisName, optimizationMode=opts.optMode)
    return datasets

def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)

    optModes = [""]

    if opts.optMode != None:
        optModes = [opts.optMode]
        
    # For-loop: All opt Mode
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()
            
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Get the luminosity
        if opts.intLumi < 0:
            opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()

        # Set/Overwrite cross-sections
        for i, d in enumerate(datasetsMgr.getAllDatasets(), 0):
            if "FakeB" not in d.getName():
                msg = "Removing dataset %s" % d.getName()
                Verbose(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle(), i==0)
                datasetsMgr.remove(d.getName())

        # Re-order datasets (different for inverted than default=baseline)
        if 0:
            newOrder = ["FakeB"]
            datasetsMgr.selectAndReorder(newOrder)
        
        # Print dataset information
        datasetsMgr.PrintInfo()

        # Get histograms under given folder in ROOT file
        hList   = datasetsMgr.getDataset("FakeB").getDirectoryContent(opts.folder)
        hPaths1 = [os.path.join(opts.folder, h) for h in hList]
        hPaths2 = [h for h in hPaths1 if "Purity" in h]
        keep    = ["MET", "HT", "Njets", "TetrajetBjetEta", "TetrajetBjetPt", "LdgTetrajetMass", 
                   "LdgTetrajetPt", "LdgTetrajetMass", "LdgTrijetBjetEta", "LdgTrijetBjetPt", "LdgTrijetMass", "LdgTrijetPt"]

        allHistos = ["NBjets", "Bjet1Pt", "Bjet2Pt", "Bjet3Pt", "Bjet1Eta", "Bjet2Eta", "Bjet3Eta", "Bjet1Bdisc", "Bjet2Bdisc", 
                     "Bjet3Bdisc", "Jet1Pt", "Jet2Pt", "Jet3Pt", "Jet4Pt", "Jet5Pt", "Jet6Pt", "Jet7Pt", "Jet1Eta", "Jet2Eta", 
                     "Jet3Eta", "Jet4Eta", "Jet5Eta", "Jet6Eta", "Jet7Eta", "Jet1Bdisc", "Jet2Bdisc", "Jet3Bdisc", "Jet4Bdisc", 
                     "Jet5Bdisc", "Jet6Bdisc", "Jet7Bdisc", "MVAmax1", "MVAmax2", "TetrajetBJetPt", "TetrajetBJetEta", "TetrajetBJetBdisc", 
                     "DeltaEtaLdgTrijetBJetTetrajetBJet", "DeltaPhiLdgTrijetBJetTetrajetBJet", "DeltaRLdgTrijetBJetTetrajetBJet", "LdgTrijetM", 
                     "LdgTrijetBJetBdisc", "SubLdgTrijetPt", "SubLdgTrijetM", "SubLdgTrijetBJetBdisc", "LdgDijetPt", "LdgDijetM", 
                     "SubLdgDijetPt", "SubLdgDijetM"]
        

# For-loop: All histograms
        for i, h in enumerate(hPaths2, 1):

            hName = h.split("/")[1]
            if hName.split("_")[0] not in keep:
                Verbose("Skipping %s" % (ShellStyles.ErrorStyle() + h + ShellStyles.NormalStyle()), i==1)
                continue
            else:
                Verbose("Plotting %s" % (ShellStyles.NoteStyle() + h + ShellStyles.NormalStyle()), True)
            PlotHistograms(datasetsMgr, h)
    return

def GetHistoKwargs(h, opts):

    # Common bin settings
    myBins  = []
    vtxBins = []
    ptBins  = []
    bWidth  = 2    
    for i in range(0, 40, bWidth):
        vtxBins.append(i)
    bWidth  = 10 #25
    for i in range(40, 100+bWidth, bWidth):
        vtxBins.append(i)

    _kwargs = {
        "ylabel"           : "Purity / %.0f ",
        "rebinX"           : 1, # cannot rebin unless i divide new purity value by rebinX value!
        "rebinY"           : None,
        "addMCUncertainty" : True, 
        "addLuminosityText": True,
        "addCmText"        : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymax": 1.05},
        "log"              : False,
        "moveLegend"       : {"dx": -0.05, "dy": 0.05, "dh": -0.1}
        }

    kwargs = copy.deepcopy(_kwargs)
    
    if "pt" in h.lower():
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"]+= units
        # kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0 ,"xmax": 500.0, "ymin": 0.0, "ymax": 1.05}

        if "tetrajet" in h.lower():
            kwargs["opts"]   = {"xmin": 0.0 ,"xmax": 800.0, "ymin": 0.0, "ymax": 1.05}
            
    if "mass" in h.lower():
        units             = "GeV/c^{2}"
        kwargs["xlabel"]  = "m_{jjb}^{ldg} (%s)" % units
        kwargs["ylabel"] += units
        if "trijet" in h.lower():
            kwargs["opts"]   = {"xmin": 50.0 ,"xmax": 300.0, "ymin": 0.0, "ymax": 1.05}
            kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "tetrajet" in h.lower():
            kwargs["opts"]   = {"xmin": 0.0 ,"xmax": 3000.0, "ymin": 0.0, "ymax": 1.05}
            kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    if "MET" in h:
        units             = "GeV"
        kwargs["xlabel"]  = "E_{T}^{miss} (%s)" % units
        kwargs["ylabel"] += units
        
    if "Njets" in h:
        units             = ""
        kwargs["xlabel"]  = "jet multiplicity"
        #kwargs["ylabel"] += units
        
    if "HT" in h:
        units             = "GeV"
        kwargs["xlabel"]  = "H_{T} (%s)" % units
        kwargs["ylabel"]  = "Purity / %.0f " + units
        kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["opts"]["xmax"] = 3000.0

    if "eta" in h.lower():
        units             = ""
        kwargs["ylabel"]  = "Purity / %.2f " + units
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -2.5 ,"xmax": 2.5, "ymin": 0.0, "ymax": 1.05}
        if "trijet" in h.lower():
            pass
        if "bjet" in h.lower():
            pass        
    return kwargs
    

def GetBinWidthMinMax(binList):
    if not isinstance(binList, list):
        raise Exception("Argument is not a list instance!")

    minWidth = +1e6
    maxWidth = -1e6
    # For-loop: All bin values (centre)
    for i in range(0, len(binList)-1):
        j = i + 1
        iBin = binList[i]
        jBin = binList[j]
        wBin = jBin-iBin
        if wBin < minWidth:
            minWidth = wBin

        if wBin > maxWidth:
            maxWidth = wBin
    return minWidth, maxWidth

def getHisto(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("FakeB").getDatasetRootHisto(histoName)
    h1.setName("FakeB")
    return h1

def PlotHistograms(datasetsMgr, histoName):
    # Get Histogram name and its kwargs
    saveName = histoName.rsplit("/")[-1]
    kwargs_  = GetHistoKwargs(saveName, opts)

    # Create the plotting object
    # p = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName) )
    p = plots.PlotBase( [getHisto(datasetsMgr, histoName)], saveFormats=[])
    p.setLuminosity(opts.intLumi)

    #  Apply histogram style
    p.histoMgr.forHisto("FakeB", styles.getFakeBStyle())

    # Set drawing/legend style
    p.histoMgr.setHistoDrawStyle("FakeB", "AP")
    p.histoMgr.setHistoLegendStyle("FakeB", "LP")

    #  Customise legend labels
    p.histoMgr.setHistoLegendLabelMany({
            "FakeB": "Fake b (VR)",
            })
    
    # Draw and save the plot
    plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary

    # Save the plots in custom list of saveFormats
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), [".png"])#, ".pdf"] )
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):

    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_").replace(" ", "").replace("(", "").replace(")", "") )

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(saveName + ext, i==0)
        plot.saveAs(saveName, formats=saveFormats)
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
    ANALYSISNAME = "Hplus2tbAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    GRIDX        = False
    GRIDY        = False
    OPTMODE      = None
    BATCHMODE    = True
    INTLUMI      = -1.0
    URL          = False
    SAVEDIR      = "/publicweb/a/aattikis/"
    VERBOSE      = False
    FOLDER       = "ForDataDrivenCtrlPlots"
    
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

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

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
    else:
        mcrabDir = rchop(opts.mcrab, "/")
        if len(mcrabDir.split("/")) > 1:
            mcrabDir = mcrabDir.split("/")[-1]
        opts.saveDir += mcrabDir + "/Purity_VR"

    # Sanity check
    allowedFolders = ["ForDataDrivenCtrlPlots"]

    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_Purity.py: Press any key to quit ROOT ...")
