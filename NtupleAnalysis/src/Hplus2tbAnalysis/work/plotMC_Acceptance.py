#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plotMC_Acceptance.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plotMC_Acceptance.py -m Hplus2tbAnalysis_Preapproval_MVA0p40_Syst_28Apr2018/ -r "passed trigger" 


LAST USED:
./plotMC_Acceptance.py  -m Hplus2tbAnalysis_Preapproval_MVA0p40_Syst_28Apr2018/ -r "passed PV" --gridX --yMin 0.00001

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import array
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.NtupleAnalysis.tools.errorPropagation as errorPropagation

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
        # Add lumis
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

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
    
    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab)

    # Get list of eras, modes, and optimisation modes
    erasList      = dsetMgrCreator.getDataEras()
    modesList     = dsetMgrCreator.getSearchModes()
    optList       = dsetMgrCreator.getOptimizationModes()
    sysVarList    = dsetMgrCreator.getSystematicVariations()
    sysVarSrcList = dsetMgrCreator.getSystematicVariationSources()

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
        
        # Print PSets used for FakeBMeasurement
        if 0:
            datasetsMgr.printSelections()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()
            datasetsMgr.PrintInfo()
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Get Luminosity
        if opts.intLumi < 0:
            if "Data" in datasetsMgr.getAllDatasetNames():
                opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
            else:
                opts.intLumi = 1.0

        # Filter the datasets 
        if 0:
            datasetsMgr.remove(filter(lambda name: "Charged" not in name, datasetsMgr.getAllDatasetNames()))

        # Re-order datasets (different for inverted than default=baseline)
        if 0:
            newOrder = ["Data"]
            newOrder.extend(aux.GetListOfEwkDatasets())
            datasetsMgr.selectAndReorder(newOrder)

        # Merge EWK samples
        if 1:
            datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()
            
        # Print post EWK-merge dataset summary
        datasetsMgr.PrintInfo()

        # Get the efficiency graphs
        hGraphList = []
        histoName  = os.path.join(opts.folder, "counter")
        hGraphList, _kwargs = GetEfficiencyHistoGraphs(datasetsMgr, opts.folder, histoName)

        # Plot the efficiencies
        PlotHistoGraphs(hGraphList, _kwargs)

    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
    return


def PlotHistoGraph(hGraphList, _kwargs):

    # Make the plots
    #p = plots.PlotBase( [histoGraphList], saveFormats=[])
    p = plots.ComparisonManyPlot(hGraphList[0], hGraphList[1:], saveFormats=[])

    # Draw the plots
    histoName = "SignalAcceptance"
    plots.drawPlot(p, histoName,  **_kwargs)
    
    # Save the plots
    SavePlot(p, histoName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"] )
    return


def GetEfficiencyHistoGraphs(datasetsMgr, folder, hName):

    # Get histogram customisations
    _kwargs  = GetHistoKwargs(opts)

    # Get histos (Data, EWK) for Inclusive
    p1 = plots.DataMCPlot(datasetsMgr, hName )

    # Clone histograms 
    histoList = []
    graphList = []
    hgList    = []

    opts.signal.append("EWK")
    opts.signal.append("QCD")

    for s in opts.signal:
        h = p1.histoMgr.getHisto(s).getRootHisto().Clone(s)
        #p1.histoMgr.setHistoLegendStyles(s, "AP")
        histoList.append(h)

    # Create the Efficiency histos
    for i, h in enumerate(histoList, 1):
        hEfficiency = GetEfficiencyHisto(histoList[i-1], opts.refCounter, _kwargs, printValues=True, hideZeros=True)
        hEfficiency.SetName("Efficiency_%d" % (i))
        
        # Convert histos to TGraph
        gEfficiency = convertHisto2TGraph(hEfficiency, printValues=False)

        # Apply random histo styles  and append
        if "charged" in h.GetName().lower():
            s = styles.getSignalStyleHToTB_M(h.GetName().split("M_")[-1])
            s.apply(gEfficiency)
            
        if "QCD" in  h.GetName():
            styles.qcdStyle.apply(gEfficiency)
        if "EWK" in  h.GetName():
            s = styles.ttStyle.apply(gEfficiency)
            
        graphList.append(gEfficiency)
        
        # Create histoGraph object
        hgEfficiency = histograms.HistoGraph( gEfficiency, plots._legendLabels[opts.signal[i-1]], "LP", "LP")
        hgList.append(hgEfficiency)
        
    return hgList, _kwargs
    #return graphList, _kwargs


def PlotHistoGraphs(hGraphList, _kwargs):

    histoName = "SignalAcceptance"

    # Create & draw the plot    
    #p = plots.PlotBase( hGraphList, saveFormats=[])
    p = plots.ComparisonManyPlot(hGraphList[0], hGraphList[1:], saveFormats=[])
    p.setLuminosity(opts.intLumi)

    if 0:
        p.histoMgr.setHistoLegendStyleAll("P")
        p.histoMgr.setHistoDrawStyleAll("L")
        p.histoMgr.setHistoDrawStyle(hGraphList[0].GetName(), "L")

    # Draw the plot
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
    # p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerStyle(ROOT.kOpenCircle))
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerSize(1.2))
    plots.drawPlot(p, histoName, **_kwargs)

    # Add some text
    for i, b in enumerate(opts.binLabels, 0):
        dx     = 0.116*(i)
        dy     = 0.0
        if _kwargs["ratio"]:
            dy = -0.4

        b      = b.replace("passed ", "").replace(")", "").replace("selection", "").replace("(", "").replace("Selection", "").replace("PV", "pv")
        label  = b.replace("mu", "#mu").replace("Passed", "").replace("tau", "#tau").replace("  Veto", "-veto").replace("Selected Events", "selected")
        label  = label.replace("jet", "jets")
        histograms.addText(0.18+dx, 0.08+dy, label, 19)

    # Save the plot
    SavePlot(p, histoName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"] )
    return


def GetHistoKwargs(opts):
    histoKwargs = {}
    _kwargs     = {
        "xlabel"           : None,
        "ylabel"           : "Efficiency",
        "ratioYlabel"      : "Ratio ",
        "ratio"            : True,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : True,
        "addLuminosityText": True,
        "addCmsText"       : True,
        "errorBarsX"       : False,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": opts.yMin, "ymax": opts.yMax},
        "opts2"            : {"ymin": 0.0, "ymax": 3.0, "log": True},
        "log"              : True,
        "moveLegend"       : {"dx": -0.53, "dy": -0.1, "dh": -0.10},
        "cutBox"           : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
        # "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False},
        "xlabelsize"       : 0                                                                                                                                                                                        
        }

    # Set x-axis divisions
    n1 = 10 # primary divisions (8)
    n2 = 0 # second order divisions (5)
    n3 = 0 # third order divisions (@)
    nDivs = n1 + 100*n2 + 10000*n3
    ROOT.gStyle.SetNdivisions(nDivs, "X")
    return _kwargs


def GetSaveName(histoName):
    base = histoName.split("_")[0]
    var  = histoName.split("_")[1]
    sel  = histoName.split("_")[2]
    name = var + "_" + GetControlRegionLabel(histoName)
    return name


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

def convertHisto2TGraph(histo, printValues=False):

    # Lists for values
    x      = []
    y      = []
    xerrl  = []
    xerrh  = []
    yerrl  = []
    yerrh  = []
    nBinsX = histo.GetNbinsX()

    # For-loop: All histogram bins
    nBinsX_ = 0
    for i in range(1, nBinsX+1):

        # Get values
        xVal  = histo.GetBinLowEdge(i) +  0.5*histo.GetBinWidth(i)
        # Visually better to have zero x-bar
        if 1:
            xLow  = 0.0001
            xHigh = 0.0001
        else:
            xLow  = 0.5*histo.GetBinWidth(i)
            xHigh = 0.5*histo.GetBinWidth(i)
        yVal  = histo.GetBinContent(i)
        yLow  = histo.GetBinError(i)
        yHigh = yLow            

        if yVal == 0:
            continue

        # Update the number of bins
        nBinsX_ += 1

        # Store values
        x.append(xVal)
        xerrl.append(xLow)
        xerrh.append(xHigh)

        y.append(yVal)
        yerrl.append(yLow)
        yerrh.append(yHigh)

    # Create the TGraph with asymmetric errors
    tgraph = ROOT.TGraphAsymmErrors(nBinsX_,
                                    array.array("d", x),
                                    array.array("d", y),
                                    array.array("d", xerrl),
                                    array.array("d", xerrh),
                                    array.array("d", yerrl),
                                    array.array("d", yerrh))

    # Construct info table (debugging)
    table  = []
    align  = "{:>6} {:^10} {:>10} {:>10} {:>10} {:^3} {:<10}"
    header = align.format("#", "xLow", "x", "xUp", "Efficiency", "+/-", "Error") #Purity = 1-EWK/Data
    hLine  = "="*70
    table.append("")
    table.append(hLine)
    table.append("{:^70}".format("TGraph"))
    table.append(header)
    table.append(hLine)
    
    # For-loop: All values x-y and their errors
    for i, xV in enumerate(x, 0):
        row = align.format(i+1, "%.2f" % xerrl[i], "%.2f" %  x[i], "%.2f" %  xerrh[i], "%.3f" %  y[i], "+/-", "%.3f" %  yerrh[i])
        table.append(row)
    table.append(hLine)

    if printValues:
        for i, line in enumerate(table, 1):
            Print(line, False) #i==1)
    return tgraph


def GetEfficiencyHisto(histo, refCounter, kwargs, printValues=False, hideZeros=True):
    
    # Define histos here
    xMax = histo.GetXaxis().GetXmax()
    hEff = ROOT.TH1D('Eff','Eff', int(xMax), 0, xMax)
    hNum = ROOT.TH1D('Num','Num', 1, 0, 1)
    hDen = ROOT.TH1D('Den','Den', 1, 0, 1)

    # Construct info table (debugging)
    table  = []
    align  = "{:>6} {:^20} {:<40} {:>10} {:>10} {:>10} {:^3} {:<10}"
    header = align.format("Bin", "Range", "Selection", "Numerator", "Denominator", "Eff Value", "+/-", "Eff Error")
    hLine  = "="*120
    nBinsX = histo.GetNbinsX()
    table.append("{:^100}".format("Histogram"))
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # First determine the bin number
    binNumber = -1
    for j in range (0, nBinsX+1):

        # Skip this counter?
        binLabel = histo.GetXaxis().GetBinLabel(j)

        if binLabel == refCounter:
            binNumber = j
        else:
            continue

    if binNumber == -1:
        raise Exception("Could not find reference counter \"%s\"" % refCounter)

    if binNumber > nBinsX:
        raise Exception("Invalid bin selected (bin = %d" % (binNumber) ) 

    # First get numerator
    denValue = ROOT.Double(0.0)
    denError = ROOT.Double(0.0)
    denValue = histo.IntegralAndError(binNumber, binNumber, denError)
    ROOT.gErrorIgnoreLevel = ROOT.kFatal #kPrint = 0,  kInfo = 1000, kWarning = 2000, kError = 3000, kBreak = 4000, kSysError = 5000, kFatal = 6000   

    # For-loop: All histogram bins
    binCounter = 0
    opts.binLabels = []
    for j in range (binNumber, nBinsX+1):

        # Skip this counter?
        binLabel = histo.GetXaxis().GetBinLabel(j)
        if binLabel in opts.skipList:
            Verbose("Skipping counter with name \"%s\"" % (binLabel), True)
            continue

        # Declare variables
        numValue    = ROOT.Double(0.0)
        numError    = ROOT.Double(0.0)
        numValue    = histo.IntegralAndError(j, j, numError)
        effValue    = 0
        effError    = 0

        # Sanity
        if numValue < 0.0:
            raise Exception("Integral is less than zero!")
        if numError < 0.0:
            raise Exception("Error is less than zero!")
        
        # Numerator and Denominator histos
        Verbose("Evaluating efficiency for \"%s\"" % (binLabel), j==binNumber)
        hNum.SetBinContent(1, numValue)
        hNum.SetBinError(1, numError)
        hDen.SetBinContent(1, denValue)
        hDen.SetBinError(1, denError)


        # Calculate Efficiency
        teff = ROOT.TEfficiency(hNum, hDen)
        teff.SetStatisticOption(ROOT.TEfficiency.kFNormal) #statistic option is 'normal approximation'
        effValue = teff.GetEfficiency(1)
        effError = teff.GetEfficiencyErrorLow(1)

        # Bin-range or overflow bin?
        binRange = "%.1f -> %.1f" % (histo.GetXaxis().GetBinLowEdge(j), histo.GetXaxis().GetBinUpEdge(j) )
        if j >= nBinsX:
            binRange = "> %.1f"   % (histo.GetXaxis().GetBinLowEdge(j) )

        # Fill histogram
        binCounter+= 1
        hEff.SetBinContent(binCounter, effValue)
        hEff.SetBinError(binCounter, effError)

        # Save bin labels 
        opts.binLabels.append(binLabel)

        # Save information in table
        row = align.format(binCounter, binRange, binLabel, "%.1f" % numValue, "%.1f" % denValue, "%.3f" % effValue, "+/-", "%.3f" % effError)
        table.append(row)

        # Reset histos 
        hNum.Reset()
        hDen.Reset()               

    # Finalise table
    table.append(hLine)

    # Print purity as function of final shape bins
    if printValues:
        for i, line in enumerate(table):
            Print(line, i==0)

    ROOT.gErrorIgnoreLevel = ROOT.kWarning #kPrint = 0,  kInfo = 1000, kWarning = 2000, kError = 3000, kBreak = 4000, kSysError = 5000, kFatal = 6000   
    return hEff

#================================================================================================ 
# Main
#================================================================================================ 
if __name__ == "__main__":
    '''g1

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
    OPTMODE      = ""
    BATCHMODE    = True
    INTLUMI      = -1.0
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    FOLDER       = "counters/weighted/"
    #SIGNALMASS   = [200, 300, 500]
    SIGNALMASS   = [200, 500]
    REFCOUNTER   = "passed trigger"
    SKIPLIST     = ["Passed tau selection and genuine (Veto)", "b tag SF", "passed fat jet selection (Veto)", "Selected Events",  "passed METFilter selection ()"]
    GRIDX        = False
    GRIDY        = False
    YMIN         = 1e-4
    YMAX         = 1.2
    
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

    parser.add_option("-r", "--refCounter", dest="refCounter", type="string", default=REFCOUNTER,
                      help="Counter name to use as reference for calculating the relative efficiency of all other cuts [default: %s]" % REFCOUNTER)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--yMin", dest="yMin", type=float, default=YMIN,
                      help="Minimum value of y-axis [default: %s]" % YMIN)

    parser.add_option("--yMax", dest="yMax", type=float, default=YMAX,
                      help="Maxmimum value of y-axis [default: %s]" % YMAX)

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX,
                      help="Enable the grid in x-axis [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY,
                      help="Enable the grid in y-axis [default: %s]" % GRIDY)

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
        
    # Define counters to skip (if for example empty)
    opts.skipList = SKIPLIST

    # Define save directory
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="Acceptance")
        
    # Sanity check
    allowedFolders = ["counters", "counters/weighted/"]
    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

    # Signal list
    opts.signal     = []
    opts.signalMass = SIGNALMASS
    for m in SIGNALMASS:
        signal = "ChargedHiggs_HplusTB_HplusToTB_M_%i" % m
        opts.signal.append(signal)


    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_Eff.py: Press any key to quit ROOT ...")
