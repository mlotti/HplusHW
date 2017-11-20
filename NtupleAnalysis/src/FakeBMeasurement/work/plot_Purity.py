#!/usr/bin/env python
'''
Usage:
./plot_Purity.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plot_Purity.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar -e "QCD|Charged" --plotEWK -o OptChiSqrCutValue100  
./plot_Purity.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar  -e "QCD|Charged" -plotEWK -o OptChiSqrCutValue100  
./plot_Purity.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170630_045528_IsGenuineBEventBugFix_TopChiSqrVar -e "QCD|Charged" --plotEWK -o OptChiSqrCutValue100  
./plot_Purity.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170627_124436_BJetsGE2_TopChiSqrVar_AllSamples --plotEWK -e 'QCD|Charged'

NOTE:
If unsure about the parameter settings a pseudo-multicrab do:
root -l /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170629_102740_FakeBBugFix_TopChiSqrVar/TT/res/histograms-TT.root
gDirectory->ls()
FakeBMeasurement_80to1000_Run2016->cd()
gDirectory->ls()
config->ls()
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


def MakeGraph(markerStyle, color, binList, valueDict, upDict, downDict):
    g = ROOT.TGraphAsymmErrors(len(binList))
    for i in range(len(binList)):
        g.SetPoint(i, i+0.5, valueDict[binList[i]])
        g.SetPointEYhigh(i, upDict[binList[i]])
        g.SetPointEYlow(i, downDict[binList[i]])
    g.SetMarkerSize(1.6)
    g.SetMarkerStyle(markerStyle)
    g.SetLineColor(color)
    g.SetLineWidth(3)
    g.SetMarkerColor(color)
    return g


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
    return ["TT", "noTop", "SingleTop", "ttX"]
    #return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


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
        
        PrintPSet("TopologySelection", datasetsMgr)

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

        # Print (merged) data
        datasetsMgr.PrintInfo()

        # Re-order datasets (different for inverted than default=baseline)
        if 0:
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

        # Do the Purity Triplets?
        if 0:
            bType  = ["", "EWKFakeB", "EWKGenuineB"]
            folder = "FakeBPurity" + bType[0]
            hList  = datasetsMgr.getDataset("EWK").getDirectoryContent(folder)
            for hName in hList:
                PlotPurity(datasetsMgr, os.path.join(folder, hName))

        # Do the Std Selections Purity plots
        folder    = "ForDataDrivenCtrlPlots"
        allHistos = datasetsMgr.getDataset("EWK").getDirectoryContent(folder)
        hList = [h for h in allHistos if "StandardSelections" in h and "_Vs" not in h]
        hList.extend([h for h in allHistos if "AllSelections" in h and "_Vs" not in h])

        # Only do these histos
        myHistos = ["Njets", "LdgTrijetMass", "TetrajetBjetPt", "LdgTetrajetMass", "LdgTetrajetMass"]

        # For-loop: All histos
        for h in hList:
                
            if h.split("_")[0] not in myHistos:
                continue
            if "JetEtaPhi" in h:
                continue
            PlotPurity(datasetsMgr, folder, h)

    return

def PrintPSet(selection, datasetsMgr):
    selection = "\"%s\":"  % (selection)
    thePSets = datasetsMgr.getAllDatasets()[0].getParameterSet()

    # First drop everything before the selection
    thePSet_1 = thePSets.split(selection)[-1]

    # Then drop everything after the selection
    thePSet_2 = thePSet_1.split("},")[0]

    # Final touch
    thePSet = selection + thePSet_2

    Print(thePSet, True)
    return

def getHistos(datasetsMgr, histoName):
    
    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]


def IsBaselineOrInverted(analysisType):
    analysisTypes = ["Baseline", "Inverted"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        pass
    return


def PlotPurity(datasetsMgr, folder, hName):
    '''
    Create plots with "FakeB=Data-EWKGenuineB"
    '''
    # Which folder
    genuineBFolder = folder + "EWKGenuineB"
    fakeBFolder    = folder + "EWKFakeB"
    histoName      = os.path.join(folder, hName)
    hNameGenuineB  = os.path.join(genuineBFolder, hName)

    # Customize the histograms (BEFORE calculating purity obviously otherwise numbers are nonsense)
    _cutBox = None
    _rebinX = 1
    _opts   = {"ymin": 1e-3, "ymax": 1.0} #"ymaxfactor": 1.2}
    _format = "%0.0f"
    #_opts["xmax"] = xMax
    _xlabel = None
    _ylabel = "Purity / "
    _format = "/ %.0f "

    h = histoName.split("/")[-1]
    if "dijetm" in h.lower():
        _units  = "GeV/c^{2}" 
        _format = "%0.0f " + _units
        _xlabel = "m_{jj} (%s)" % (_units)
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    if "trijetm" in h.lower():
        _rebinX = 2
        _units  = "GeV/c^{2}" 
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 1000.0
    if "pt" in h.lower():
        _format = "%0.0f GeV/c" 
    if "chisqr" in h.lower():
        _opts["xmax"] = 100.0
        if "allselections" in h.lower():
            _opts["xmax"] = 10.0            
    #if histo.lower().endswith("met_et"):
    if h.lower().startswith("ht_"):
        _rebinX = 5
        _units  = "GeV/c" 
        _format = "%0.0f " + _units
        _xlabel = "H_{T} (%s)" % _units
        _cutBox = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmin"] =  500.0
        _opts["xmax"] = 3500.0
    if "eta" in h.lower():
        _rebinX = 1
        _format = "%0.2f" 
        _cutBox = {"cutValue": 0., "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmin"] = -3.0
        _opts["xmax"] = +3.0
    if "deltaeta" in h.lower():
        _format = "%0.2f" 
        _opts["xmin"] =  0.0
        _opts["xmax"] = 6.0
    if "bdisc" in h.lower():
        _format = "%0.2f" 
    if "tetrajetm" in h.lower():
        _rebinX = 4
        _units  = "GeV/c^{2}" 
        _format = "%0.0f " + _units
        _xlabel = "m_{jjbb} (%s)" % (_units)
        _opts["xmax"] = 2500.0
    if "pt_" in h.lower():
        _rebinX = 2

    _ylabel += _format

    # Get histos (Data, EWK) for Inclusive
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName) )
    p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, hNameGenuineB) )
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Clone histograms 
    Data = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    EWK  = p2.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK")
    QCD  = p1.histoMgr.getHisto("Data").getRootHisto().Clone("QCD")

    # Rebin histograms (Before calculating Purity)
    Data.Rebin(_rebinX)
    EWK.Rebin(_rebinX)
    QCD.Rebin(_rebinX)

    # Get QCD = Data-EWK
    QCD.Add(EWK, -1)

    # Comparison plot. The first argument is the reference histo. All other histograms are compared with respect to that. 
    QCD_Purity, xMin, xMax, binList, valueDict, upDict, downDict = getPurityHisto(QCD, Data, inclusiveBins=False, printValues=False)
    EWK_Purity, xMin, xMax, binList, valueDict, upDict, downDict = getPurityHisto(EWK, Data, inclusiveBins=False, printValues=True)

    # Create TGraphs
    if 0:
        gQCD_Purity = MakeGraph(ROOT.kFullTriangleUp, ROOT.kOrange, binList, valueDict, upDict, downDict)
        gEWK_Purity = MakeGraph(ROOT.kFullTriangleDown, ROOT.kBlue, binList, valueDict, upDict, downDict)
        
    # Make the plots
    if opts.plotEWK:
        p = plots.ComparisonManyPlot(QCD_Purity, [EWK_Purity], saveFormats=[])
    else:
        p = plots.PlotBase([QCD_Purity], saveFormats=[])


    # Apply histo styles
    p.histoMgr.forHisto("QCD", styles.getQCDLineStyle() )
    if opts.plotEWK:
        p.histoMgr.forHisto("EWK"  , styles.getAltEWKLineStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("QCD", "P")
    if opts.plotEWK:
        p.histoMgr.setHistoDrawStyle("EWK", "HIST")

    # Set legend style
    p.histoMgr.setHistoLegendStyle("QCD", "P")
    if opts.plotEWK:
        p.histoMgr.setHistoLegendStyle("EWK", "F")

    # Set legend labels
    if opts.plotEWK:
        p.histoMgr.setHistoLegendLabelMany({
                "QCD" : "QCD",
                "EWK" : "EWK",
                })
    else:
        p.histoMgr.setHistoLegendLabelMany({
                "QCD" : "QCD",
                })
    
    # Do the plot
    plots.drawPlot(p, 
                   histoName,  
                   xlabel        = _xlabel,
                   ylabel        = _ylabel,
                   log           = False, 
                   rebinX       = 1, # must be done BEFORE calculating purity
                   cmsExtraText  = "Preliminary", 
                   createLegend  = {"x1": 0.76, "y1": 0.80, "x2": 0.92, "y2": 0.92},
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


def SavePlot(plot, plotName, saveDir, saveFormats = [".png"]): #[".png", ".C", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    #saveName = os.path.join(saveDir, plotName.replace("/", "_"))
    saveName = os.path.join(saveDir, plotName.replace("ForDataDrivenCtrlPlots/", ""))

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
    binList   = []
    valueDict = {}
    upDict    = {}
    downDict  = {}
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

        # Save the values
        binList.append(j)
        valueDict[j] = myPurity
        upDict[j]    = myUncert
        downDict[j]  = myUncert

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

    return h, xMin, xMax, binList, valueDict, upDict, downDict
            

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
    MCONLY       = False
    PLOTEWK      = False
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

    parser.add_option("--plotEWK", dest="plotEWK", action="store_true", default=PLOTEWK, 
                      help="Include EWK purity in all the plots (1-QCDPurity) [default: %s]" % (PLOTEWK) )

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
