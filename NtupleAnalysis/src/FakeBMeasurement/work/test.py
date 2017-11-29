#!/usr/bin/env python
'''
Description:
This script produces QCD normalization factors by running a fitting script.
The steps followed are the following:
1) The user defines the histograms to be used as templates. Two are needed:
   a) Baseline EWK (MC)
   b) Inverted QCD (Data)
This will be used in the fitting processes to extract the templates for:
   a) EWK
   b) QCD
This step gives us the two fitted templates:
   a) fit_EWKInclusive_Baseline_Inclusive.png
   b) fit_QCD_Inverted_Inclusive.png

2) The two extracted templates (from fits) are then used to fit on "Baseline Data" 
(our Signal Region) as a linear combination with the fraction of QCD (f) as the only 
free parameter of the fit:
N = fQCD + (1-f)EWK
This step gives us the final fit and the fit parameter:
   a) finalFit_Inclusive.png 
   b) finalFit_Inclusive_log.png
   c) f = Fraction of QCD Events

In addition to the above, the normalisation factor is also extrated:
   a) R = nQCDBaseline / nQCDInverted
   b) R = nFakeBaseline / nFakeInverted 
where the later is not used in any way (HToTauNu legacy)
These normalisation factor are saved under:
   <pseudo_mcrab_directory> QCDInvertedNormalizationFactors_Run2016_80to1000.py
in an automatically-generated python class. 

This file/class is later used (read) by the makeInvertedPseudoMulticrab.py in order to normalise
properly the "Control-Region" data.


Usage:
./plotQCD_Fit.py -m <pseudo_mcrab_directory> [opts]

Last Used:
/test.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDT0p70_AllSelections_BDT0p70to0p90_RandomSort_171124_144802/ --url --useMC -e "QCD_HT50to100|QCD_HT100to200|QCD_HT200to300|QCD_HT300to500"

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
ROOT.gErrorIgnoreLevel = ROOT.kFatal #kPrint = 0,  kInfo = 1000, kWarning = 2000, kError = 3000, kBreak = 4000, kSysError = 5000, kFatal = 6000
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.FakeBMeasurement.FakeBNormalization as FakeBNormalization
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector

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
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"] #DEFAULT!

def GetHistoKwargs(histoName):
    '''
    '''
    Verbose("Creating a map of histoName <-> kwargs")

    # Definitions
    _opts = {}
    logY  = True
    if logY:
        _opts     = {"ymin": 1e0, "ymaxfactor": 5.0}
    else:
        #_opts     = {"ymin": 1e0, "ymax": 0.08} #"ymaxfactor": 1.2}
        _opts     = {"ymin": 1e0, "ymaxfactor": 1.2}

    if "mass" in histoName.lower():
        _units        = "GeV/c^{2}"
        _xlabel       = "m_{jjb} (%s)" % (_units)
        _opts["xmin"] =  50
        _opts["xmax"] = 400
        if "tetrajet" in histoName.lower():
            _opts["xmin"] =  100
            _opts["xmax"] = 1000
    elif "met" in histoName.lower():
        _units        = "GeV"
        _xlabel       = "E_{T}^{miss} (%s)" % (_units)
        _opts["xmin"] =   0
        _opts["xmax"] = 250
        if logY:
            _opts     = {"ymin": 1e0, "ymaxfactor": 2.0}
    else:
        _units        = "rads"
        _xlabel       = "#Delta#phi (%s)" % (_units)
        _opts["xmin"] = 0.0
        _opts["xmax"] = 3.2

    # Define plotting options
    kwargs = {
        "xlabel"      : _xlabel,
        "ylabel"      : "Arbitrary Units / %.0f " +  _units,
        "log"         : logY,
        "opts"        : _opts,
        "opts2"       : {"ymin": 0.0, "ymax": 2.0},
        "ratio"       : True, 
        # "cutBox"      : {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True},
        "cmsExtraText": "Preliminary",
        "ratioYlabel" : "Ratio",
        "ratioInvert" : False, 
        "addCmsText"  : True,
        "createLegend": {"x1": 0.54, "y1": 0.78, "x2": 0.92, "y2": 0.92},
        }
    return kwargs

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
    
def getHisto(datasetsMgr, datasetName, histoName, analysisType):
    Verbose("getHisto()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-" + datasetName)
    return h1

def getModuleInfoString(opts):
    moduleInfoString = "_%s_%s" % (opts.dataEra, opts.searchMode)
    if len(opts.optMode) > 0:
        moduleInfoString += "_%s" % (opts.optMode)
    return moduleInfoString

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
def main(opts):
    Verbose("main function")

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab)

    # Get list of eras, modes, and optimisation modes
    erasList      = dsetMgrCreator.getDataEras()
    modesList     = dsetMgrCreator.getSearchModes()
    optList       = dsetMgrCreator.getOptimizationModes()
    sysVarList    = dsetMgrCreator.getSystematicVariations()
    sysVarSrcList = dsetMgrCreator.getSystematicVariationSources()

    # Todo: Print settings table
    if 0:
        print erasList
        print
        print modesList
        print
        print optList
        print
        print sysVarList
        print 
        print sysVarSrcList
        
    # If user does not define optimisation mode do all of them
    if opts.optMode == None:
        if len(optList) < 1:
            optList.append("")
        else:
            pass
        optModes = optList
    else:
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
            
        # Get the PSets:
        thePSets = datasetsMgr.getDataset("TT").getParameterSet()
        if 0:
            Print("Printing the PSet:\n" + thePSets, True)
            sys.exit()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Remove datasets
        removeList = ["QCD-b", "Charged"] #"QCD"
        for i, d in enumerate(removeList, 0):
            msg = "Removing dataset %s" % d
            Verbose(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
            datasetsMgr.remove(filter(lambda name: d in name, datasetsMgr.getAllDatasetNames()))
        if 0:
            datasetsMgr.PrintInfo()
        
        # Re-order datasets (different for inverted than default=baseline)
        if 0:
            newOrder = ["Data"]
            newOrder.extend(GetListOfEwkDatasets())
            datasetsMgr.selectAndReorder(newOrder)

        # Merge EWK samples
        datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            
        # Print dataset information
        if 0:
            datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(True)
        style.setGridY(True)
        
        # Do the fit on the histo after ALL selections (incl. topology cuts)
        folderName = "ForFakeBNormalization"
        # histoName  = "LdgTrijetMass_AfterStandardSelections"
        histoName  = "LdgTrijetMass_AfterAllSelections"
        
        folderName = "ForFakeBMeasurement"
        if 1:
            histoName  = "MET_AfterStandardSelections"
            #histoName  = "LdgTetrajetMass_AfterStandardSelections"
            #histoName = "DeltaPhiLdgTrijetBJetTetrajetBJet_AfterStandardSelections"
            #histoName = "DeltaRLdgTrijetBJetTetrajetBJet_AfterStandardSelections"
        else:
            histoName  = "MET_AfterAllSelections"
            #histoName  = "LdgTetrajetMass_AfterAllSelections"
            #histoName = "DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections"
            #histoName = "DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections"

        PlotAndFitTemplates(datasetsMgr, histoName, folderName, opts)
    return

def PlotAndFitTemplates(datasetsMgr, histoName, inclusiveFolder, opts):
    Verbose("PlotAndFitTemplates()")

    # Variable definition
    genuineBFolder  = inclusiveFolder + "EWKGenuineB"
    fakeBFolder     = inclusiveFolder + "EWKFakeB"

    # Histogram names
    hInclusive_Baseline = "%s/%s" % (inclusiveFolder, "Baseline_" + histoName)
    hGenuineB_Baseline  = "%s/%s" % (genuineBFolder , "Baseline_" + histoName)
    hFakeB_Baseline     = "%s/%s" % (fakeBFolder    , "Baseline_" + histoName)

    hInclusive_Inverted = "%s/%s" % (inclusiveFolder, "Inverted_" + histoName)
    hGenuineB_Inverted  = "%s/%s" % (genuineBFolder , "Inverted_" + histoName)
    hFakeB_Inverted     = "%s/%s" % (fakeBFolder    , "Inverted_" + histoName)
    
    # Create plots
    pInclusive_Baseline  = plots.DataMCPlot(datasetsMgr, hInclusive_Baseline)
    pGenuineB_Baseline   = plots.DataMCPlot(datasetsMgr, hGenuineB_Baseline)
    pFakeB_Baseline      = plots.DataMCPlot(datasetsMgr, hFakeB_Baseline)

    pInclusive_Inverted  = plots.DataMCPlot(datasetsMgr, hInclusive_Inverted)
    pGenuineB_Inverted   = plots.DataMCPlot(datasetsMgr, hGenuineB_Inverted)
    pFakeB_Inverted      = plots.DataMCPlot(datasetsMgr, hFakeB_Inverted)

    # Get the desired histograms (Baseline)
    baseline_Data        = pInclusive_Baseline.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline-Data")
    baseline_QCD         = pInclusive_Baseline.histoMgr.getHisto("QCD").getRootHisto().Clone("Baseline-QCD")
    baseline_EWKGenuineB = pGenuineB_Baseline.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKGenuineB")
    baseline_EWKFakeB    = pFakeB_Baseline.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKFakeB")
    inverted_Data        = pInclusive_Inverted.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted-Data")
    inverted_QCD         = pInclusive_Inverted.histoMgr.getHisto("QCD").getRootHisto().Clone("Inverted-QCD")
    inverted_EWKGenuineB = pGenuineB_Inverted.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKGenuineB")
    inverted_EWKFakeB    = pFakeB_Inverted.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKFakeB")

    # Subtract EWKGenuineB from Data to get FakeB (= QCD_inclusive + EWK_genuineB)
    if opts.useMC:
        # FakeB = QCD + EWKFakeB
        baseline_FakeB = baseline_QCD.Clone("Baseline-FakeB")
        baseline_FakeB.Add(baseline_EWKFakeB, +1)

        inverted_FakeB = inverted_QCD.Clone("Inverted-FakeB")
        inverted_FakeB.Add(inverted_EWKFakeB, +1)
    else:
        # FakeB = Data -EWKGenuineB
        baseline_FakeB = baseline_Data.Clone("Baseline-FakeB")
        baseline_FakeB.Add(baseline_EWKGenuineB, -1)

        inverted_FakeB = inverted_Data.Clone("Inverted-FakeB")
        inverted_FakeB.Add(inverted_EWKGenuineB, -1)

    # Rebin the EWK-MC histo (significant fit improvement - opposite effect for QCD fit)
    rebinX = 1
    baseline_Data.RebinX(rebinX)
    baseline_QCD.RebinX(rebinX)
    baseline_EWKGenuineB.RebinX(rebinX)
    baseline_EWKFakeB.RebinX(rebinX)
    baseline_FakeB.RebinX(rebinX)
    inverted_Data.RebinX(rebinX)
    inverted_QCD.RebinX(rebinX)
    inverted_EWKGenuineB.RebinX(rebinX)
    inverted_EWKFakeB.RebinX(rebinX)
    inverted_FakeB.RebinX(rebinX)

    if 1:
        print "DISABLE for calculation of TRANSFER FACTOR!"
        baseline_Data.Scale(1.0/baseline_Data.Integral())
        inverted_Data.Scale(1.0/inverted_Data.Integral())
        baseline_EWKGenuineB.Scale(1.0/baseline_EWKGenuineB.Integral())
        baseline_FakeB.Scale(1.0/baseline_FakeB.Integral())
        inverted_EWKGenuineB.Scale(1.0/inverted_EWKGenuineB.Integral())
        inverted_FakeB.Scale(1.0/inverted_FakeB.Integral())
        
    # Create the final plot object
    #compareHistoList = [inverted_FakeB, baseline_FakeB] #, baseline_EWKGenuineB]
    if 1:
        compareHistoList = [baseline_FakeB, inverted_FakeB]
        p = plots.ComparisonManyPlot(baseline_EWKGenuineB, compareHistoList, saveFormats=[])
    else:
        compareHistoList = [baseline_EWKGenuineB, baseline_FakeB]
        p = plots.ComparisonManyPlot(baseline_Data, compareHistoList, saveFormats=[])

    # Apply styles
    #p.histoMgr.forHisto("Baseline-Data"       , styles.getDataStyle() )
    p.histoMgr.forHisto("Baseline-FakeB"      , styles.getBaselineLineStyle() )
    p.histoMgr.forHisto("Baseline-EWKGenuineB", styles.getAltEWKStyle() )
    p.histoMgr.forHisto("Inverted-FakeB"      , styles.getFakeBStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("Baseline-Data"       , "P")
    p.histoMgr.setHistoDrawStyle("Baseline-FakeB"      , "HIST")
    p.histoMgr.setHistoDrawStyle("Baseline-EWKGenuineB", "P")
    p.histoMgr.setHistoDrawStyle("Inverted-FakeB"      , "P")

    # Set legend style
    p.histoMgr.setHistoLegendStyle("Baseline-Data"        , "P")
    p.histoMgr.setHistoLegendStyle("Baseline-FakeB"       , "L")
    p.histoMgr.setHistoLegendStyle("Baseline-EWKGenuineB" , "P")
    p.histoMgr.setHistoLegendStyle("Inverted-FakeB"       , "P")

    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            "Baseline-Data"       : "Data (SR)",
            "Baseline-FakeB"      : "Fake b (SR)",
            "Baseline-EWKGenuineB": "EWK genuine-b (SR)",
            "Inverted-FakeB"      : "Fake b (CR)",
            })
    
    #=========================================================================================
    # Start fit process
    #=========================================================================================
    binLabels = ["Inclusive"]
    moduleInfoString = opts.optMode #opts.dataEra + "_" + opts.searchMode + "_" + opts.optMode

    #=========================================================================================
    # Create templates (EWK fakes, EWK genuine, QCD; data template is created by manager)
    #=========================================================================================
    manager = FakeBNormalization.FakeBNormalizationManager(binLabels, opts.mcrab, moduleInfoString)
    manager.CalculateTransferFactor(binLabels[0], baseline_FakeB, inverted_FakeB)

    # Print(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle(), True) 


    Verbose("Write the normalisation factors to a python file", True)
    fileName = os.path.join(opts.mcrab, "QCDInvertedNormalizationFactors%s.py"% ( getModuleInfoString(opts) ) )
    manager.writeNormFactorFile(fileName, opts)
    
    # Not really needed to plot the histograms again
    if 1:
        saveName = histoName
        plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 
        SavePlot(p, saveName, os.path.join(opts.saveDir, "Fit", opts.optMode) ) 
    return

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
    MERGEEWK     = True
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    USEMC        = False

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

    parser.add_option("--useMC", dest="useMC", action="store_true", default=USEMC,
                      help="Use QCD MC instead of QCD=Data-EWK? [default: %s]" % (USEMC) )


    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    # Sanity check
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    # Sanity check
    if not opts.mergeEWK:
        Print("Cannot draw the histograms without the option --mergeEWK. Exit", True)
        sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
