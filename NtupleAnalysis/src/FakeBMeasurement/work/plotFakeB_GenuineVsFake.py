#!/usr/bin/env python
'''
Description:
This scipt creates all histograms for comparing 
Baseline and Inverted distributions of key variables, like
the leading trijet mass, and its properties.

For the definition of the counter class see:
HiggsAnalysis/NtupleAnalysis/scripts

For more counter tricks and optios see also:
HiggsAnalysis/NtupleAnalysis/scripts/hplusPrintCounters.py

Usage:
./plotFakeB_GenuineVsFake.py -m <pseudo_mcrab> [opts]

Examples:
./plotFakeB_GenuineVsFake.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170630_045528_IsGenuineBEventBugFix_TopChiSqrVar --mergeEWK -e "QCD|Charged" -o "OptChiSqrCutValue100"
./plotFakeB_GenuineVsFake.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar --mergeEWK -e "QCD|Charged" -o "OptChiSqrCutValue100"
./plotFakeB_GenuineVsFake.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170627_124436_BJetsGE2_TopChiSqrVar_AllSamples --mergeEWK -e "QCD|Charged" -o "OptChiSqrCutValue100p0"
./plotFakeB_GenuineVsFake.py -m <pseudo_mcrab> --mergeEWK --histoLevel Vital
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

        # Custom Filtering of datasets 
        if 0:
            datasetsMgr.remove(filter(lambda name: "HplusTB" in name and not "M_500" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
   
        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"] #, "TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
        newOrder.extend(GetListOfEwkDatasets())
        datasetsMgr.selectAndReorder(newOrder)

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        # Sanity check
        if not opts.mergeEWK:
            Print("Cannot draw the histograms without the option --mergeEWK. Exit", True)
            sys.exit()

        # Merge EWK samples
        datasetsMgr.merge("EWK", GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)


        # Do the plots
        for analysisType in ["Baseline", "Inverted"]:
            for hName in GetHistoList(analysisType, bType=""):
                DoPlots(datasetsMgr, hName, analysisType)
    return


def GetHistoList(analysisType, bType):
    Verbose("Creating purity histo list  for %s" % analysisType)

    IsBaselineOrInverted(analysisType)

    bTypes = ["", "EWKFakeB", "EWKGenuineB"]
    if bType not in bTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (bType, "\"" + "\", \"".join(bTypes) + "\"") )

    histoList = []

    # Some histograms only available for Inverted 
    if analysisType == "Inverted":
        folder = "FakeBPurity" + bType    
        histoList.append("%s/%s_FailedBJetPt_AfterAllSelections" % (folder, analysisType) )
        histoList.append("%s/%s_FailedBJetEta_AfterAllSelections" % (folder, analysisType) )
        histoList.append("%s/%s_FailedBJetBDisc_AfterAllSelections" % (folder, analysisType) )
        histoList.append("%s/%s_FailedBJetPdgId_AfterAllSelections" % (folder, analysisType) )
        histoList.append("%s/%s_FailedBJetPartonFlavour_AfterAllSelections" % (folder, analysisType) )
        histoList.append("%s/%s_FailedBJetHadronFlavour_AfterAllSelections" % (folder, analysisType) )
        histoList.append("%s/%s_FailedBJetAncestry_AfterAllSelections" % (folder, analysisType) )
        
    folder = "ForFakeBMeasurement" + bType
    histoList.append("%s/%s_TopMassReco_ChiSqr_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_LdgTetrajetPt_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_LdgTetrajetMass_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_SubldgTetrajetPt_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_SubldgTetrajetMass_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_TetrajetBJetPt_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_TetrajetBJetEta_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_LdgTrijetPt_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_LdgTrijetM_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_SubLdgTrijetPt_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_SubLdgTrijetM_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_LdgDijetPt_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_LdgDijetM_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_SubLdgDijetPt_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_TopMassReco_SubLdgDijetM_AfterAllSelections" % (folder, analysisType) )
    return histoList


def getHistos(datasetsMgr, histoName, analysisType):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName(analysisType + "-EWK")
    return [h1, h2]


def DoPlots(datasetsMgr, histoName, analysisType="Inverted"):
    
    # Sanity check
    IsBaselineOrInverted(analysisType)
    
    # Definitions
    defaultFolder = ""
    if "FakeBPurity" in histoName:
        defaultFolder = "FakeBPurity"
    elif "ForFakeBMeasurement" + histoName:
        defaultFolder = "ForFakeBMeasurement"
    else:
        raise Exception("This should never happen")
    genuineBFolder = defaultFolder + "EWKGenuineB"
    fakeBFolder    = defaultFolder + "EWKFakeB"

    # Get the EWK (GenuineB)
    h1 = histoName.replace( defaultFolder, genuineBFolder)
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, h1, analysisType))
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get the EWK (FakeB)
    h2 = histoName.replace( defaultFolder, fakeBFolder)
    p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, h2, analysisType) )
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get EWK histos
    EWKGenuineB = p1.histoMgr.getHisto(analysisType + "-EWK").getRootHisto().Clone("EWKGenuineB")
    EWKFakeB    = p2.histoMgr.getHisto(analysisType + "-EWK").getRootHisto().Clone("EWKFakeB")

    # Normalize histograms to unit area
    if 0:
        EWKGenuineB.Scale(1.0/EWKGenuineB.Integral())
        EWKFakeB.Scale(1.0/EWKFakeB.Integral())

    # Create the final plot object
    #p = plots.ComparisonManyPlot(EWKFakeB, [EWKGenuineB], saveFormats=[])
    p = plots.ComparisonManyPlot(EWKGenuineB, [EWKFakeB], saveFormats=[])
    p.setLuminosity(GetLumi(datasetsMgr))
        
    # Apply styles
    p.histoMgr.forHisto("EWKGenuineB" , styles.getGenuineBStyle() )
    p.histoMgr.forHisto("EWKFakeB"    , styles.getFakeBLineStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("EWKGenuineB", "HIST")
    p.histoMgr.setHistoDrawStyle("EWKFakeB"   , "AP")

    # Set legend style
    p.histoMgr.setHistoLegendStyle("EWKGenuineB", "F")
    p.histoMgr.setHistoLegendStyle("EWKFakeB"   , "P")
    # p.histoMgr.setHistoLegendStyleAll("LP")

    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            #"EWKGenuineB": "EWK-GenuineB",
            #"EWKFakeB"   : "EWK-FakeB",
            "EWKGenuineB": "EWK-GenuineB (%s)" % (analysisType),
            "EWKFakeB"   : "EWK-FakeB (%s)" % (analysisType),
            })

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _opts   = {"ymin": 1e0, "ymaxfactor": 2.0}
    _format = "%0.0f"
    _xlabel = None

    if "dijetm" in histoName.lower():
        _rebinX = 2
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jj} (%s)" % (_units)
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 400.0
    if "trijetm" in histoName.lower():
        _rebinX = 5
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 1500.0
    if "pt" in histoName.lower():
        _rebinX = 2
        _format = "%0.0f GeV/c"
    if "eta" in histoName.lower():
        _format = "%0.2f"
        _cutBox = {"cutValue": 0., "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmin"] = -3.0
        _opts["xmax"] = +3.0
    if "deltaeta" in histoName.lower():
        _format = "%0.2f"
        _opts["xmin"] =  0.0
        _opts["xmax"] = 6.0
    if "bdisc" in histoName.lower():
        _format = "%0.2f"
    if "tetrajetm" in histoName.lower():
        _rebinX = 10
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjjb} (%s)" % (_units)
        _opts["xmax"] = 3500.0
    if "ancestry" in histoName.lower():
        _rebinX = 1
        _units  = ""
        _format = "%0.0f " + _units
        _opts["xmax"] = 32.0
    plots.drawPlot(p, histoName,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = True, 
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.42, "y1": 0.78, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.0, "ymax": 100}, #{"ymin": 0.6, "ymax": 1.4},
                   ratio        = False,
                   ratioInvert  = False, 
                   ratioYlabel  = "Ratio",
                   cutBox       = _cutBox,
                   )
    # Save plot in all formats
    SavePlot(p, histoName, os.path.join(opts.saveDir, "GenuineVsFake", opts.optMode) ) 
    return


def IsBaselineOrInverted(analysisType):
    analysisTypes = ["Baseline", "Inverted"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        pass
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
