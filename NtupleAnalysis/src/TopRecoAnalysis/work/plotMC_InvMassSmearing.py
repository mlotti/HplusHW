#!/usr/bin/env python
'''
DESCRIPTION:
https://twiki.cern.ch/twiki/bin/view/CMS/HPlus2tbHadronicResolvedQA2018


USAGE:
./plotMC_InvMassSmearing.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plotMC_InvMassSmearing.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400_wSignal/TopRecoAnalysis_180422_BDT40/ --signalMass  500
./plotMC_InvMassSmearing.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400_wSignal/TopRecoAnalysis_180422_BDT40/ --signalMass 1000
./plotMC_InvMassSmearing.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400_wSignal/TopRecoAnalysis_180422_BDT40/ --signalMass 1000


LAST USED:
/plotMC_InvMassSmearing.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400_wSignal/TopRecoAnalysis_180422_BDT40/ --signalMass 500 --url -n

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
            if "ChargedHiggs_HplusTB_HplusToTB_M_%s" % (opts.signalMass) in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
            else:
                datasetsMgr.remove(d.getName())
                
        # Determine integrated Lumi before removing data
        if "Data" in datasetsMgr.getAllDatasetNames():
            opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        else:
            opts.intLumi = 35920

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            
            if str(opts.signalMass) not in d.getName():
            #if d not in "%s" % (opts.signalMass):
                continue
            datasetOrder.append(d.getName())

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setGridX(False)
        style.setGridY(False)

        # Do the histograms
        PlotHistograms(datasetsMgr)

    return

def getHistos(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]

def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf", ".png"]):
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

def PlotHistograms(datasetsMgr):

    # Definitions
    kwargs = {}
    histos = []

    # For-loop: All histos in list
    dName =  "ChargedHiggs_HplusTB_HplusToTB_M_%s" % (opts.signalMass)

    # Matched Leading Trijet
    p0 = plots.MCPlot(datasetsMgr, "AnalysisTriplets/TetrajetMass_LdgTopIsHTop", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    hTopTrue = p0.histoMgr.getHisto(dName).getRootHisto().Clone("Matched-LdgTrijet")
    histos.append(hTopTrue)

    # Matched Bjet
    p1 = plots.MCPlot(datasetsMgr, "AnalysisTripletsTrue/TetrajetMass", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    hBjetTrue = p1.histoMgr.getHisto(dName).getRootHisto().Clone("Matched-Bjet")
    histos.append(hBjetTrue)

    # Matched Leading Trijet + Bjet
    p2 = plots.MCPlot(datasetsMgr, "AnalysisTripletsTrue/TetrajetMass_LdgTopIsHTop", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    hAllTrue = p2.histoMgr.getHisto(dName).getRootHisto().Clone("Matched-LdgTrijet-Bjet")
    histos.append(hAllTrue)
        
    # Inclusive
    p3 = plots.MCPlot(datasetsMgr, "AnalysisTriplets/TetrajetMass", normalizeToLumi=opts.intLumi, saveFormats=[], **kwargs)
    hInclusive = p3.histoMgr.getHisto(dName).getRootHisto().Clone("Inclusive")
    histos.append(hInclusive)

    # Unmatched
    hUnmatched = p3.histoMgr.getHisto(dName).getRootHisto().Clone("Unmatched")
    hUnmatched.Add(hAllTrue , +1)
    hUnmatched.Add(hBjetTrue, -1)
    hUnmatched.Add(hTopTrue , -1)
    histos.append(Unmatched)

    # Make comparison plot
    nTotal = hInclusive.Integral()
    align  = "{:>25} {:>25}"
    title  = align.format("Histogram", "Percentage (%)")
    hLine  = 50*"="
    table  = []
    table.append(hLine)
    table.append(title)
    table.append(hLine)
    for h in histos:
        n     = h.Integral()
        perc  = (n/nTotal)*100
        table.append(align.format(h.GetName(), " %.1f" % (perc) ))

        if opts.normaliseToOne:
            h = h.Scale(1/h.Integral())

    # Print table info
    table.append(hLine)
    for row in table:
        print row

    # Make comparison plot
    p = plots.ComparisonManyPlot(hInclusive, [hBjetTrue, hTopTrue, hAllTrue, hUnmatched], saveFormats=[])
    p.setLuminosity(opts.intLumi)

    # Overwite signal style?
    style  = [200, 500, 800, 1000, 2000, 5000]
    lstyle = [ROOT.kSolid, ROOT.kDashed, ROOT.kDashDotted, ROOT.kDotted, ROOT.kDotted, ROOT.kSolid]
    p.histoMgr.forHisto("Matched-LdgTrijet-Bjet" , styles.getFakeBStyle())
    p.histoMgr.forHisto("Matched-Bjet"           , styles.mcStyle) #getInvertedLineStyle()) 
    p.histoMgr.forHisto("Matched-LdgTrijet"      , styles.stylesCompound[-1])
    p.histoMgr.forHisto("Inclusive"              , styles.getGenuineBLineStyle())
    p.histoMgr.forHisto("Unmatched"              , styles.errorRatioStatStyle)
        
    # Set draw style
    p.histoMgr.setHistoDrawStyle("Inclusive", "AP")
    p.histoMgr.setHistoDrawStyle("Matched-Bjet", "AP")
    p.histoMgr.setHistoDrawStyle("Matched-LdgTrijet", "HIST")
    p.histoMgr.setHistoDrawStyle("Matched-LdgTrijet-Bjet", "HIST")
    p.histoMgr.setHistoDrawStyle("Unmatched", "HIST")

    # Set legend style    
    p.histoMgr.setHistoLegendStyle("Inclusive", "LP")
    p.histoMgr.setHistoLegendStyle("Matched-Bjet", "LP")
    p.histoMgr.setHistoLegendStyle("Matched-LdgTrijet", "F")
    p.histoMgr.setHistoLegendStyle("Matched-LdgTrijet-Bjet", "F")
    p.histoMgr.setHistoLegendStyle("Unmatched", "F")

    p.histoMgr.setHistoLegendLabelMany({
            "Inclusive"              : "Inclusive",
            "Matched-Bjet"           : "b-jet match",
            "Matched-LdgTrijet"      : "top match",
            "Matched-LdgTrijet-Bjet" : "top + b-jet match",
            "Unmatched"              : "Combinatoric",
            })
    
    
    # Draw customised plot
    saveName = "TetrajetMass"
    _units   = "GeV/c^{2}"
    if opts.signalMass > 500:
        _leg     = {"x1": 0.20, "y1": 0.65, "x2": 0.45, "y2": 0.87}
    else:
        _leg     = {"x1": 0.60, "y1": 0.65, "x2": 0.85, "y2": 0.87}

    if opts.normaliseToOne:
        yLabel = "Arbitrary Units / %0.0f " + _units
    else:
        yLabel = "Events / %0.0f " + _units

    plots.drawPlot(p, 
                   saveName,
                   xlabel       = "m_{jjbb} (%s)" % (_units),
                   ylabel       = yLabel,
                   log          = False,
                   rebinX       = 5,
                   cmsExtraText = "Preliminary",
                   createLegend = _leg,
                   opts         = {"xmin": 0.0, "xmax": 1500.0, "ymin": 0.0, "ymaxfactor": 1.2},
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = {"cutValue": opts.signalMass, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
                   )

    # Save plot in all formats    
    savePath = os.path.join(opts.saveDir, opts.optMode)
    SavePlot(p, "%s_M%s" % (saveName, opts.signalMass), savePath) 

    return


def SavePlot(plot, saveName, saveDir, saveFormats = [".C", ".pdf", ".png"]):
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
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    SIGNALMASS   = 500
    INTLUMI      = -1.0
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    VERBOSE      = False
    NORMALISE    = False
    ANALYSISNAME = "TopRecoAnalysis"
    SAVEDIR      = "/publicweb/a/aattikis/" + ANALYSISNAME


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

    parser.add_option("--signalMass", dest="signalMass", type=int, default=SIGNALMASS,
                     help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

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
    if opts.signalMass not in allowedMass:
        raise Exception("Signal mass invalid")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotMC_InvMassSmearing.py: Press any key to quit ROOT ...")
