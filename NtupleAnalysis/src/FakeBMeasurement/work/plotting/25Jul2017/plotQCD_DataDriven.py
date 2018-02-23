#!/usr/bin/env python
'''
Description:
This scipt plots TH1 histograms produced by the
FakeBMeasurement.cc class. These histograms
are considered auxiliary to those created by
plotEwkVsQcd.py and plotBaselineVsInverted.py 
scripts. They show the QCD (or EWK) purity as a 
function of a given variable.

For the definition of the counter class see:
HiggsAnalysis/NtupleAnalysis/scripts

For more counter tricks and optios see also:
HiggsAnalysis/NtupleAnalysis/scripts/hplusPrintCounters.py

Usage:
./plotQCD_DataDriven.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotQCD_DataDriven.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar -o OptChiSqrCutValue100 --url
./plotQCD_DataDriven.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar -o OptChiSqrCutValue100 --url --mergeEWK
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
    Print(msg, printHeader)
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


def GetHistoList(analysisType="Baseline"):
    '''
    Returns the list of histograms created by
    the TopSelection class
    '''
    
    Verbose("Creating histogram list for %s" % analysisType, True)

    # Entire list
    hList = [        
        "ForDataDrivenCtrlPlots/Njets"
        ]
    return hList


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

    #optModes = ["", "OptChiSqrCutValue50", "OptChiSqrCutValue100"]
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

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                print d.getName()
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0) # ATLAS 13 TeV H->tb exclusion limits
                
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
   
        # Custom Filtering of datasets 
        datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
        # datasetsMgr.remove(filter(lambda name: "Charged" in name, datasetsMgr.getAllDatasetNames()))

        # Replace QCD MC with QCD-DataDriven
        replaceQCDFromData(datasetsMgr, "FakeBMeasurementTrijetMass", "QCD-Data")

        # Re-order datasets (different for inverted than default=baseline)
        if 1:
            newOrder = ["Data"]
            newOrder.extend(["ChargedHiggs_HplusTB_HplusToTB_M_500"])
            newOrder.extend(["QCD-Data"])
            newOrder.extend(GetListOfEwkDatasets())
            datasetsMgr.selectAndReorder(newOrder)

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)

        # Do Data-MC histograms with DataDriven QCD
        DataMCHistograms(datasetsMgr)
    return


def DataMCHistograms(datasetsMgr):
    '''
    Create data-MC comparison plot, with the default:
    - legend labels (defined in plots._legendLabels)
    - plot styles (defined in plots._plotStyles, and in styles)
    - drawing styles ('HIST' for MC, 'EP' for data)
    - legend styles ('L' for MC, 'P' for data)
    '''
    Verbose("Plotting Data-MC Histograms")

    # Definitions
    histoNames  = []
    histoKwargs = {}
    saveFormats = [".png"] #[".C", ".png", ".pdf"]

    # General Settings
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.12}
    else:
        _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": 0.1}
 
    _kwargs = {"rebinX"           : 1,
               "rebinY"           : None,
               "ratioYlabel"      : "Data/MC",
               "ratio"            : True, 
               "stackMCHistograms": True,
               "ratioInvert"      : False, 
               "addMCUncertainty" : False, 
               "addLuminosityText": True,
               "addCmsText"       : True,
               "cmsExtraText"     : "Preliminary",
               "opts"             : {"ymin": 2e-1, "ymaxfactor": 10}, #1.2
               "opts2"            : {"ymin": 0.0, "ymax": 2.0},
               "log"              : True,
               "moveLegend"       : _moveLegend,
               "cutBox"           : {"cutValue": 7.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
               }


    histoName = "ForDataDrivenCtrlPlots/Njets"
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f GeV/c^{2}"
    kwargs["cutBox"] = {"cutValue": 7.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    # For-loop: All histograms in list
    for histoName in histoNames:
        kwargs_  = histoKwargs[histoName]
        saveName = histoName.replace("/", "_")

        # Create the plotting object
        p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])

        # Apply QCD data-driven style
        dName = "QCD-Data"
        p.histoMgr.forHisto(dName, styles.getFakeBStyle())
        p.histoMgr.setHistoDrawStyle(dName, "HIST")
        p.histoMgr.setHistoLegendStyle(dName, "F")
        p.histoMgr.setHistoLegendLabelMany({
                #dName: "QCD (Data)",
                dName: "Fake b (data)",
                })

        # Draw and save the plot
        plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        SavePlot(p, saveName, os.path.join(opts.saveDir, "Test", opts.optMode) )
    return

def replaceQCDFromData(dMgr, dataDrivenDatasetName, newName="QCD-Data"):
    
    # Define variables
    mcQCDName      = "QCD"
    dataDrivenQCD  = dMgr.getDataset(dataDrivenDatasetName)
    dataDrivenQCD.setName(newName)

    # Get list of dataset names
    names = dMgr.getAllDatasetNames()

    # Return the index in the list of the first dataset whose name is mcQCDName.
    index = names.index(mcQCDName)

    # Remove the dataset at the given position in the list, and return it. 
    names.pop(index)
    
    # Insert the dataset to the given position  (index) of the list
    names.insert(index, dataDrivenQCD.getName())

    # Remove from the dataset manager the mcQCDName
    dMgr.remove(mcQCDName)
    names.pop(names.index(dataDrivenQCD.getName()))
    
    # Select and reorder Datasets. 
    # This method can be used to either select a set of dataset.Dataset objects. reorder them, or both.
    dMgr.selectAndReorder(names)
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

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
    ANALYSISNAME = "FakeBMeasurement"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MCONLY       = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug' 

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

    parser.add_option("--mcOnly", dest="mcOnly", action="store_true", default=MCONLY,
                      help="Plot only MC info [default: %s]" % MCONLY)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--histoLevel", dest="histoLevel", action="store", default = HISTOLEVEL,
                      help="Histogram ambient level (default: %s)" % (HISTOLEVEL))

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

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
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
