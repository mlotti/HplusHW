#!/usr/bin/env python
'''
Description:

Usage:
./plotQCD_BaseVsInv.py -m <pseudo_mcrab> [opts]

Examples:
./plotQCD_BaseVsInv.py -m FakeBMeasurement_170728_040545/ -o "" --url
./plotQCD_BaseVsInv.py -m FakeBMeasurement_170728_040545/ -o "" --url --normaliseToOne
./plotQCD_BaseVsInv.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170703_031128_CtrlTriggers_QCDTemplateFit --mergeEWK -e "QCD|Charged" -o "OptTriggerOR['HLT_PFHT400_SixJet30']ChiSqrCutValue100"

Last Used:
./plotQCD_BaseVsInv.py -m FakeBMeasurement_SignalTriggers_NoTrgMatch_StdSelections_TopCut_AllSelections_TopCut10_170728_040545/ --url --normaliseToOne
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

    #optModes = ["", "OptChiSqrCutValue50", "OptChiSqrCutValue100", "OptChiSqrCutValue200"]
    optModes = ["OptChiSqrCutValue100"]                                                                                                                             

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

        # Remove dataset ? 
        if 1:
            datasetsMgr.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "Charged" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
   
        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"]
        newOrder.extend(GetListOfEwkDatasets())
        datasetsMgr.selectAndReorder(newOrder)

        # Merge EWK samples
        datasetsMgr.merge("EWK", GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(False)
        style.setGridY(False)

        # 1) Do the StandardSelections/AllSelections
        bType  = ""
        folder = "ForFakeBNormalization" + bType	
        hList  = datasetsMgr.getDataset("EWK").getDirectoryContent(folder)
        hPaths = [os.path.join(folder, h) for h in hList]
        baselinePaths = []
        invertedPath  = []
        for p in hPaths:
            if "Baseline" in p:
                baselinePaths.append(p)
            if "Inverted" in p:
                invertedPath.append(p)
        for hBaseline, hInverted in zip(baselinePaths, invertedPath):
            PlotBaselineVsInverted(datasetsMgr, hBaseline, hInverted)

        # 2) Do the topSelection histos
        analysisType     = "Inverted"
        folder           = "topSelection_%s" % (analysisType)
        invertedList     = datasetsMgr.getDataset("EWK").getDirectoryContent(folder)
        invertedPaths    = [os.path.join(folder, h) for h in invertedList]
        baselinePaths    = [p.replace("Inverted", "Baseline") for p in invertedPaths]
        for hBaseline, hInverted in zip(baselinePaths, invertedPaths):
            if "Vs" in hBaseline: #skip TH2
                continue
            PlotBaselineVsInverted(datasetsMgr, hBaseline, hInverted)
    return

def getHistos(datasetsMgr, dataset, hBaseline, hInverted):
    
    h1 = datasetsMgr.getDataset(dataset).getDatasetRootHisto(hBaseline)
    h1.setName("Baseline-" + dataset)

    h2 = datasetsMgr.getDataset(dataset).getDatasetRootHisto(hInverted)
    h2.setName("Inverted-" + dataset)
    return [h1, h2]

def PlotBaselineVsInverted(datasetsMgr, hBaseline, hInverted):

    # Get the Inclusive (Data, EWK)
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, "Data", hBaseline, hInverted))
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, "EWK", hBaseline, hInverted))
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get Baseline histos
    baseline_Data = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone()
    baseline_QCD  = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone("Baseline-QCD")
    baseline_EWK  = p2.histoMgr.getHisto("Baseline-EWK").getRootHisto().Clone()

    # Get Inverted histos
    inverted_Data = p1.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone()
    inverted_QCD  = p1.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone("Inverted-QCD")
    inverted_EWK  = p2.histoMgr.getHisto("Inverted-EWK").getRootHisto().Clone()

    # Subtract EWK from Data to get QCD
    baseline_QCD.Add(baseline_EWK, -1)
    inverted_QCD.Add(inverted_EWK, -1)

    # Normalize histograms to unit area
    if opts.normaliseToOne:
        baseline_Data.Scale(1.0/baseline_Data.Integral())
        baseline_QCD.Scale(1.0/baseline_QCD.Integral())
        baseline_EWK.Scale(1.0/baseline_EWK.Integral())
        inverted_Data.Scale(1.0/inverted_Data.Integral())
        inverted_QCD.Scale(1.0/inverted_QCD.Integral())
        inverted_EWK.Scale(1.0/inverted_EWK.Integral())

    # Create the final plot object
    p = plots.ComparisonManyPlot(baseline_QCD, [inverted_QCD], saveFormats=[])
        
    # Apply styles
    p.histoMgr.forHisto("Baseline-QCD" , styles.getBaselineStyle() )
    p.histoMgr.forHisto("Inverted-QCD" , styles.getInvertedStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("Baseline-QCD", "AP")
    p.histoMgr.setHistoDrawStyle("Inverted-QCD", "HIST")

    # Set legend style
    p.histoMgr.setHistoLegendStyle("Baseline-QCD", "LP")
    p.histoMgr.setHistoLegendStyle("Inverted-QCD", "F")
    # p.histoMgr.setHistoLegendStyleAll("LP")

    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            "Baseline-QCD" : "QCD (Baseline)",
            "Inverted-QCD" : "QCD (Inverted)",
            })

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    if opts.normaliseToOne:
        _opts   = {"ymin": 1e-4, "ymaxfactor": 2.0}
    else:
        _opts   = {"ymin": 1e0, "ymaxfactor": 2.0}
    _format = "%0.0f"
    _xlabel = None

    if "dijetm" in hBaseline.lower():
        _rebinX = 2
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jj} (%s)" % (_units)
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 400.0
    if "trijetm" in hBaseline.lower():
        _rebinX = 5
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 1500.0
    if "pt" in hBaseline.lower():
        _rebinX = 2
        _format = "%0.0f GeV/c"
    if "eta" in hBaseline.lower():
        _format = "%0.2f"
        _cutBox = {"cutValue": 0., "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmin"] = -3.0
        _opts["xmax"] = +3.0
    if "deltaeta" in hBaseline.lower():
        _format = "%0.2f"
        _opts["xmin"] =  0.0
        _opts["xmax"] = 6.0
    if "bdisc" in hBaseline.lower():
        _format = "%0.2f"
    if "tetrajetm" in hBaseline.lower():
        _rebinX = 10
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjjb} (%s)" % (_units)
        _opts["xmax"] = 3500.0

    plots.drawPlot(p, 
                   hBaseline,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = True, 
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.62, "y1": 0.78, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   ratio        = True,
                   ratioInvert  = False, 
                   ratioYlabel  = "Ratio",
                   cutBox       = _cutBox,
                   )

    # Save plot in all formats    
    saveName = hBaseline.replace("/", "_")
    saveName = saveName.replace("_Baseline_", "_")
    savePath = os.path.join(opts.saveDir, "BaselineVsInverted", opts.optMode)
    SavePlot(p, saveName, savePath) 
    return


def IsBaselineOrInverted(analysisType):
    analysisTypes = ["Baseline", "Inverted"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        pass
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
    ANALYSISNAME = "FakeBMeasurement"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = True
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False

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

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", 
                      help="Normalise the baseline and inverted shapes to one? [default: %s]" % (NORMALISE) )

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
    if not opts.mergeEWK:
        Print("Cannot draw the Baseline Vs Inverted histograms without the option --mergeEWK. Exit", True)
        sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
