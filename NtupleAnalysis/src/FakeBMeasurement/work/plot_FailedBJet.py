#!/usr/bin/env python
'''
Description:
Plots properties of all failed b-jets (aka inverted b-jets) in triplets:
a) Inclusive
b) GenuineB
c) FakeB
Thesee b-jets are taken from topData.getFailedBJetsUsedAsBJetsInFit() and 
include the b-jets with a "Loose" (instead of "Medium") discriminator WP.

Usage:
./plot_FailedBJet.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plot_FailedBJet.py -m FakeBMeasurement_GE2MediumPt40Pt30_GE1LooseMaxDiscr0p7_StdSelections_TopCut100_AllSelections_TopCut10_RandomFailedBJetSort_171012_012105/ --plotEWK --url

Last Used::
./plot_FailedBJet.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDTm0p80_AllSelections_BDT0p90_RandomSort_171115_101036 -e "Charged" --url --plotEWK

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
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]
    #return ["TT", "noTop", "SingleTop", "ttX"]


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

        # Only do these histos
        myHistos = ["FailedBJet1BDisc",
                    "FailedBJet1Pt", 
                    #"FailedBJet1Eta", 
                    #"FailedBJet1PdgId", 
                    #"FailedBJet1PartonFlavour", 
                    #"FailedBJet1HadronFlavour", 
                    #
                    "FailedBJet2BDisc",
                    "FailedBJet2Pt", 
                    #"FailedBJet2Eta", 
                    #"FailedBJet2PdgId", 
                    #"FailedBJet2PartonFlavour", 
                    #"FailedBJet2HadronFlavour", 
                    #
                    "FailedBJet3BDisc",
                    "FailedBJet3Pt", 
                    #"FailedBJet3Eta", 
                    #"FailedBJet3PdgId", 
                    #"FailedBJet3PartonFlavour", 
                    #"FailedBJet3HadronFlavour", 
                    ]
        
        # For-loop: All histos
        folders = ["", "FakeB", "GenuineB"]
        for f in folders:

            folder = "FailedBJet" + f
            hList  = datasetsMgr.getDataset("EWK").getDirectoryContent(folder)
            
            for hName in hList:
                if hName.split("_")[-2] not in myHistos:
                    continue
                PlotHisto(datasetsMgr, os.path.join(folder, hName))
    return

def getHistos(datasetsMgr, histoName):
    
    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]


def PlotHisto(datasetsMgr, histoName):
    Verbose("Plotting histogram %s for Data, EWK, QCD " % (histoName), True)

    # Customize the histograms (BEFORE calculating purity obviously otherwise numbers are nonsense)
    _cutBox = None
    _rebinX = 1
    logY    = True
    yMaxF   = 1.2
    yMax    = 0.5
    if logY:
        yMaxF = 10        
    _opts   = {"ymin": 1e-4, "ymax": yMax} #"ymaxfactor": yMaxF}
    _format = "%0.0f"
    _xlabel = None
    _ylabel = "Events / "
    _format = "/ %.0f "
    h = histoName.split("/")[-1]
    if "pt" in h.lower():
        _units  = "GeV/c" 
        _format = "%0.0f " + _units
        _xlabel = "p_{T} (%s)" % (_units)
        _cutBox = {"cutValue": 40., "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 500.0
    if "eta" in h.lower():
        _rebinX = 1
        _format = "%0.2f" 
        _cutBox = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmin"] = -3.0
        _opts["xmax"] = +3.0
    if "bdisc" in h.lower():
        _format = "%0.2f" 
        _opts["xmin"] = 0.0
        _opts["xmax"] = 1.2
        _cutBox = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    if "pt_" in h.lower():
        _rebinX = 2

    _ylabel += _format

    # Get histos (Data, EWK) for Inclusive
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName) )
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Clone histograms 
    Data = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    EWK  = p1.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK")
    QCD  = p1.histoMgr.getHisto("Data").getRootHisto().Clone("QCD")

    # Rebin histograms (Before calculating Purity)
    Data.Rebin(_rebinX)
    EWK.Rebin(_rebinX)
    QCD.Rebin(_rebinX)

    # Get QCD = Data-EWK
    QCD.Add(EWK, -1)

    # Normalize histograms to unit area?
    if opts.normaliseToOne:
        if Data.Integral() > 0:
            Data.Scale(1.0/Data.Integral())
        if QCD.Integral() > 0:
            QCD.Scale( 1.0/QCD.Integral())
        if EWK.Integral() > 0:
            EWK.Scale( 1.0/EWK.Integral())

    # Make the plots
    if opts.plotEWK:
        p = plots.ComparisonManyPlot(QCD, [EWK], saveFormats=[])
    else:
        p = plots.PlotBase([QCD], saveFormats=[])

    # Apply histo styles
    p.histoMgr.forHisto("QCD", styles.getQCDLineStyle() )
    if opts.plotEWK:
        p.histoMgr.forHisto("EWK", styles.getEWKStyle() )
        #p.histoMgr.forHisto("EWK", styles.getAltEWKLineStyle() )

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
                   log           = logY, 
                   rebinX       = 1,
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
    SavePlot(p, histoName, os.path.join(opts.saveDir, "FailedBJet", opts.optMode), saveFormats = [".png"] )
    return


def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".pdf", ".png"]):
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
    NORMALISE    = True

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
                      help="Also plot EWK distribution on canvas [default: %s]" % PLOTEWK)

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
    
    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", default=NORMALISE,
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
        
    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotQCD_FailedBJet.py: Press any key to quit ROOT ...")
