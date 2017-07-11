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
./plotPurity.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotFakeB_Purity.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170630_045528_IsGenuineBEventBugFix_TopChiSqrVar -e "QCD|Charged" --mergeEWK -o OptChiSqrCutValue100  
./plotFakeB_Purity.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170627_124436_BJetsGE2_TopChiSqrVar_AllSamples --mergeEWK -e 'QCD|Charged'
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

    #optModes = ["", "OptChiSqrCutValue50p0", "OptChiSqrCutValue100p0", "OptChiSqrCutValue200p0"]
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
        
        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()
            
        # Custom Filtering of datasets 
        if 0:
            datasetsMgr.remove(filter(lambda name: "Charged" in name and not "M_500" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
   
        # Re-order datasets (different for inverted than default=baseline)
        if 0:
            newOrder = ["Data"]
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

        # Do the purity plots
        if not opts.mergeEWK:        
            Print("Cannot draw the Data/QCD/EWK histograms without the option --mergeEWK. Exit", True)
            return
        for hName in GetHistoList(analysisType="Inverted", bType=""):
            PurityPlots(datasetsMgr, hName, "Inverted")
    return


def GetHistoList(analysisType="Inverted", bType=""):
    Verbose("Creating purity histo list  for %s" % analysisType)

    IsBaselineOrInverted(analysisType)

    bTypes = ["", "EWKFakeB", "EWKGenuineB"]
    if bType not in bTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (bType, "\"" + "\", \"".join(bTypes) + "\"") )

    histoList = []

    folder = "FakeBPurity" + bType
    histoList.append("%s/%s_FailedBJetPt_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_FailedBJetEta_AfterAllSelections" % (folder, analysisType) )
    histoList.append("%s/%s_FailedBJetBDisc_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_FailedBJetPdgId_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_FailedBJetPartonFlavour_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_FailedBJetHadronFlavour_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_FailedBJetAncestry_AfterAllSelections" % (folder, analysisType) )

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
    # histoList.append("%s/%s_TopMassReco_LdgDijetPt_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_TopMassReco_LdgDijetM_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_TopMassReco_SubLdgDijetPt_AfterAllSelections" % (folder, analysisType) )
    # histoList.append("%s/%s_TopMassReco_SubLdgDijetM_AfterAllSelections" % (folder, analysisType) )
    return histoList


def getHistos(datasetsMgr, histoName, analysisType):
    
    datasetName = "Data"
    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-" + datasetName)

    datasetName = "EWK"
    h2 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h2.setName(analysisType + "-" + datasetName)
    return [h1, h2]


def IsBaselineOrInverted(analysisType):
    analysisTypes = ["Baseline", "Inverted"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        pass
    return


def PurityPlots(datasetsMgr, histoName, analysisType="Inverted"):
    '''
    Create plots with "FakeB=Data-EWKGenuineB"
    '''
    Verbose("Plotting histogram %s for Data, EWK, QCD for %s" % (histoName, analysisType), True)

    # Sanity check
    IsBaselineOrInverted(analysisType)

    defaultFolder  = "FakeBPurity" 
    genuineBFolder = defaultFolder + "EWKGenuineB"
    fakeBFolder    = defaultFolder + "EWKFakeB"

    # Get histos (Data, EWK) for Inclusive
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName, analysisType) )
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get histos (Data, EWK) for GenuineB
    p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName.replace(defaultFolder, genuineBFolder), analysisType) )
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Clone histograms 
    Data        = p1.histoMgr.getHisto(analysisType + "-Data").getRootHisto().Clone(analysisType + "-Data")
    EWK         = p1.histoMgr.getHisto(analysisType + "-EWK").getRootHisto().Clone(analysisType + "-EWK")
    EWKGenuineB = p2.histoMgr.getHisto(analysisType + "-EWK").getRootHisto().Clone(analysisType + "-EWK")
    FakeB       = p1.histoMgr.getHisto(analysisType + "-Data").getRootHisto().Clone(analysisType + "-FakeB")

    # Subtract EWKGEnuineB from Data to get FakeB
    FakeB.Add(EWKGenuineB, -1)
    #FakeB.Add(EWK, -1)
    
    # Dos not work
    # p1.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
    # p2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))

    # Comparison plot. The first argument is the reference histo. All other histograms are compared with respect to that. 
    FakeB_Purity, xMin, xMax = getPurityHisto(FakeB, Data, inclusiveBins=False, printValues=False)
    EWKGenuineB_Purity, xMin, xMax = getPurityHisto(EWKGenuineB, Data, inclusiveBins=False, printValues=False)
    p = plots.ComparisonManyPlot(FakeB_Purity, [EWKGenuineB_Purity], saveFormats=[])

    # Apply histo styles
    p.histoMgr.forHisto(analysisType + "-FakeB", styles.getInvertedLineStyle() )#styles.getFakeBLineStyle() )
    p.histoMgr.forHisto(analysisType + "-EWK"  , styles.getAltEWKLineStyle() ) #styles.getAltEWKStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle(analysisType + "-FakeB", "HIST")
    p.histoMgr.setHistoDrawStyle(analysisType + "-EWK"  , "HIST")

    # Set legend style
    p.histoMgr.setHistoLegendStyle(analysisType + "-FakeB", "L")
    p.histoMgr.setHistoLegendStyle(analysisType + "-EWK"  , "L")

    # p.histoMgr.setHistoLegendStyleAll("LP")

    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            analysisType + "-FakeB" : "FakeB",
            analysisType + "-EWK"   : "GenuineB (EWK)",
            })
    
    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.2}
    _format = "%0.0f"
    _opts["xmax"] = xMax
    _xlabel = None

    if "dijetm" in histoName.lower():
        _units  = "GeV/c^{2}" 
        _format = "%0.0f " + _units
        _xlabel = "m_{jj} (%s)" % (_units)
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    if "trijetm" in histoName.lower():
        _units  = "GeV/c^{2}" 
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 1500.0
    if "pt" in histoName.lower():
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
        _units  = "GeV/c^{2}" 
        _format = "%0.0f " + _units
        _xlabel = "m_{jjjb} (%s)" % (_units)
        _opts["xmax"] = 3500.0

    # Do the plot
    plots.drawPlot(p, 
                   histoName,  
                   xlabel        = _xlabel,
                   ylabel        = "Purity / {0}".format(_format),
                   log           = False, 
                   rebinX        = _rebinX, # Can only Rebin BEFORE calculating purity
                   cmsExtraText  = "Preliminary", 
                   createLegend  = {"x1": 0.60, "y1": 0.80, "x2": 0.92, "y2": 0.92},
                   opts          = _opts,
                   opts2         = {"ymin": 1e-5, "ymax": 1e0},
                   ratio         = False,
                   ratioInvert   = False, 
                   ratioYlabel   = "Ratio",
                   cutBox        = _cutBox,
                   )

    # Save plot in all formats
    SavePlot(p, histoName, os.path.join(opts.saveDir, "Purity", opts.optMode))#, saveFormats = [".png"] )
    return


def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".C", ".pdf"]):
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


def getPurityHisto(histo, refHisto, inclusiveBins=False, printValues=False):
    '''
    Return the FakeB purity as a histogram with splitted bins on x-axis
    '''

    h = histo.Clone()
    h.Reset("ICESM")
    ROOT.SetOwnership(h, True)
    
    rows   = []
    align  = "{:>10} {:>10} {:>10} {:>10} {:>10} {:>3} {:<10}"
    hLine  = "="*70
    header = align.format("Bin", "Bin-Center", "Numerator", "Denominator", "Purity", "", "Error")
    rows.append(hLine)
    rows.append("{:^55}".format(histo.GetName()) )
    rows.append(header)
    rows.append(hLine)

    # For-loop: Bins
    minPurity = 999.9
    for j in range(1, refHisto.GetNbinsX()+1, 1):

        # Get the numerator and denominator
        if inclusiveBins:
            nNumerator   = histo.Integral(j, histo.GetNbinsX()+1)
            nDenominator = refHisto.Integral(j, refHisto.GetNbinsX()+1)
        else:
            nNumerator   = histo.GetBinContent(j)
            nDenominator = refHisto.GetBinContent(j)

        # Calculate purity and error. Assume binomial error
        if (nDenominator > 0.0 and nNumerator > 0.0):
            myPurity = ((nNumerator) / (nDenominator) )
            myUncert = ROOT.TMath.Sqrt(myPurity * (1.0 - myPurity) / nDenominator)
        else:
            myPurity = 0.0
            myUncert = 0.0
            
        # Sanity check!
        if myPurity > 1.0 or myPurity < 0.0:
            myPurity = 1.0
            # raise Exception("Purity=%.1f/%.1f=%0.2f. This should never happen!" % (nNumerator, nDenominator, myPurity) )

        if myPurity < minPurity:
            minPurity = myPurity

        if 0:
            myPurity = myPurity*100
            myUncert = myUncert*100

        h.SetBinContent(j, myPurity)
        h.SetBinError(j, myUncert)

        row = align.format(j, "%.2f" % refHisto.GetXaxis().GetBinCenter(j), "%.1f" % nNumerator, "%.1f" % nDenominator, "%.2f" % (myPurity), "+/-", "%.3f" % (myUncert))
        rows.append(row)

    # Determine x-min and x-max
    xMinBin = histo.FindFirstBinAbove(0) # histo.GetBinCenter(1)
    xMaxBin = histo.FindLastBinAbove(minPurity) # histo.GetBinCenter(histo.GetNbinsX()+1)
    xMin    = refHisto.GetXaxis().GetBinCenter(xMinBin)
    xMax    = refHisto.GetXaxis().GetBinCenter(xMaxBin+1)

    if printValues:
        for r in rows:
            print r

    return h, xMin, xMax
            

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
