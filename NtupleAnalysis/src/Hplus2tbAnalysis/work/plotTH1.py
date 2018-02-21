#!/usr/bin/env python
'''
DESCRIPTION:
Script for plotting TH2 histograms only.


USAGE:
./plotTH1.py -m <pseudo-mcrab> [--options]


EXAMPLES:
./plotTH1.py -m Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442 --url -e "JetHT|QCD_b" --normalizeByCrossSection --logY

LAST USED:
./plotTH1.py -m Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442 --url -e "JetHT|QCD_b" --normalizeByCrossSection --logY --gridX --gridY --normalizeToLumi --intLumi 35800 --signal 500
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
import math
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
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
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

def GetLumi(datasetsMgr):
    lumi = 0.0
    for d in datasetsMgr.getAllDatasets():
        if d.isMC():
            continue
        else:
            lumi += d.getLuminosity()
    Verbose("Luminosity = %s (pb)" % (lumi), True)
    return lumi


def GetDatasetsFromDir(opts):
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

    optModes = [""]

    if opts.optMode != None:
        optModes = [opts.optMode]
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
    style.setLogX(opts.logX)
    style.setLogY(opts.logY)
    style.setLogZ(opts.logZ)


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
            datasetsMgr.PrintInfo()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Print merged datasets and MC samples
        if 0:
            datasetsMgr.PrintInfo()

        # Get Luminosity
        if opts.intLumi < 0:
            if "Data" in datasetsMgr.getAllDatasetNames():
                opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
            else:
                opts.intLumi = 1.0
         
        # Set/Overwrite cross-sections. Remove all but 1 signal mass
        removeList = []
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
                if d.getName() != opts.signal:
                    removeList.append(d.getName())

        # Custom filtering of datasets
        for i, d in enumerate(removeList, 1):
            msg = "Removing datasets %s from dataset manager" % (ShellStyles.NoteStyle() + d + ShellStyles.NormalStyle())
            Verbose(msg, i==1)
            datasetsMgr.remove(filter(lambda name: d == name, datasetsMgr.getAllDatasetNames()))


        # Merge EWK samples
        if opts.mergeEWK == "EWK":
            datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        if 1:
            datasetsMgr.PrintInfo()
            
        # Get list of histogram paths
        folder     = opts.folder
        histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)
        histoPaths = [os.path.join(folder, h) for h in histoList]

        # For-loop: All histograms
        for i, h in enumerate(histoPaths, 1):
            if "_Vs_" in h:
                continue

            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i, "/", "%s:" % (len(histoPaths)), h)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)
            PlotHistograms(datasetsMgr, h)
            break

    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
    return

def GetHistoKwargs(h, opts):

    # Defaults
    yMaxF = 1.2
    yMin  = 0.0
    if opts.logX:
        xMin = 1e0
        yMin = 1e0
    if opts.logY:
        yMin    =  1
        yMaxF   = 10
    if opts.normalizeToLumi:
        yLabel  = "Events"
        yMin    = 1e0
    elif opts.normalizeByCrossSection:
        yLabel  = "#sigma (pb)"
        yMin    = 1e-3
    elif opts.normalizeToOne:
        yLabel  = "Arbitrary Units"
    else:
        yLabel = "Unknown"
    cutBox      = {"cutValue": 400.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True} #box = True works
    cutBoxY     = {"cutValue": 200.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True,
                   "mainCanvas": True, "ratioCanvas": False} # box = True not working
    kwargs = {
        "ylabel"           : yLabel,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": opts.normalizeToLumi,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        #"xmin"             : xMin,
        #"xmax"             : xMax,
        "ymin"             : yMin,
        "cutBox"           : cutBox,
        "cutBoxY"          : cutBoxY,
        "moveLegend"       : {"dx": -0.06, "dy": -0.01, "dh": 0.15}, #hack to remove legend (tmp)
        }

    if "njets" in h.lower():
        units             = ""
        kwargs["xlabel"]  = "jet multiplicity"
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax": +14.0, "ymin": yMin, "ymaxfactor": yMaxF}
        ROOT.gStyle.SetNdivisions(8, "X")
        ROOT.gStyle.SetNdivisions(8, "Y")
        
    return kwargs
    

def PlotHistograms(datasetsMgr, histoName):

    # Get Histogram name and its kwargs
    saveName = histoName.rsplit("/")[-1]
    kwargs   = GetHistoKwargs(saveName, opts)

    # Create the plot    
    if "Data" in datasetsMgr.getAllDatasetNames():
        p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])
    else:
        if opts.normalizeToLumi:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi, saveFormats=[])
        elif opts.normalizeByCrossSection:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeByCrossSection=True, saveFormats=[], **{})
        elif opts.normalizeToOne:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToOne=True, saveFormats=[], **{})
        else:
            raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")
            
    # Customise z-axis
    if 0:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitle(kwargs["zlabel"]))
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().GetZaxis().SetTitleOffset(1.3))
        
    # Drawing style
    if 1:
        p.histoMgr.setHistoDrawStyleAll("AP")
        p.histoMgr.setHistoLegendStyleAll("LP")
    else:
        p.histoMgr.setHistoDrawStyleAll("HIST")
        p.histoMgr.setHistoLegendStyleAll("F")

    # Add dataset name on canvas
    # p.appendPlotObject(histograms.PlotText(0.18, 0.88, plots._legendLabels[opts.dataset], bold=True, size=22))

    # Draw the plot
    plots.drawPlot(p, saveName, **kwargs) #the "**" unpacks the kwargs_ dictionary

    # Save the plots in custom list of saveFormats
    SavePlot(p, saveName, os.path.join(opts.saveDir), [".png", ".pdf"] )
    return


def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Verbose(saveNameURL, i==0)
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
    OPTMODE      = None
    BATCHMODE    = True
    GRIDX        = False
    GRIDY        = False
    LOGX         = False
    LOGY         = False
    LOGZ         = False
    MERGEEWK     = False
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    FOLDER       = "ForDataDrivenCtrlPlots" #"topbdtSelection_" #jetSelection_
    SIGNALMASS   = 800
    SIGNAL       = None
    INTLUMI      = -1.0
    NORM2ONE     = False
    NORM2XSEC    = False
    NORM2LUMI    = False

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

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--signalMass", dest="signalMass", type=int, default=SIGNALMASS,
                     help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--logX", dest="logX", action="store_true", default=LOGX, 
                      help="Set x-axis to logarithm scale [default: %s]" % LOGX)

    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY,
                      help="Set y-axis to logarithm scale [default: %s]" % LOGY)

    parser.add_option("--logZ", dest="logZ", action="store_true", default=LOGZ,
                      help="Set z-axis to logarithm scale [default: %s]" % LOGZ)

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

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default = MERGEEWK,
                      help="Merge EWK datasets into a single dataset? [default: %s]" % (MERGEEWK) )

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--normalizeToOne", dest="normalizeToOne", action="store_true", default=NORM2ONE,
                      help="Normalise plot to one [default: %s]" % NORM2ONE)

    parser.add_option("--normalizeByCrossSection", dest="normalizeByCrossSection", action="store_true", default=NORM2XSEC,
                      help="Normalise plot by cross-section [default: %s]" % NORM2XSEC)

    parser.add_option("--normalizeToLumi", dest="normalizeToLumi", action="store_true", default=NORM2LUMI,
                      help="Normalise plot to luminosity [default: %s]" % NORM2LUMI)

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

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="TH1")

    if opts.normalizeToOne == False and opts.normalizeByCrossSection == False and opts.normalizeToLumi == False:
        raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")


    # Sanity check
    allowedFolders = ["counters", "counters/weighted", "PUDependency", "Weighting", 
                      "eSelection_Veto", "muSelection_Veto", "tauSelection_Veto",
                      "ForDataDrivenCtrlPlotsEWKFakeB", "ForDataDrivenCtrlPlotsEWKGenuineB",
                      "jetSelection_", "bjetSelection_", "metSelection_", 
                      "topologySelection_", "topbdtSelection_", "ForDataDrivenCtrlPlots"]

    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

     # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 1500, 2000, 2500, 3000, 5000, 7000]
    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()
    else:
        opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%i" % opts.signalMass

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotTH1.py: Press any key to quit ROOT ...")
