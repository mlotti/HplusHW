#!/usr/bin/env python
'''
DESCRIPTION:
Script that plots the Signal Significance Vs Cut Value for all histograms under a given folder (passsed as option to the script)
Good for sanity checks for key points in the cut-flow

USAGE:
./plotSignificance.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plotSignificance.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_TopCut10_171012_011451 --folder jetSelection_ --url

LAST USED:
./plotSignificance.py -m FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p50to085_180129_133455/ --folder counters/weighted --url --ratio

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import re
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *
import array

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
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

def rchop(myString, endString):
  if myString.endswith(endString):
    return myString[:-len(endString)]
  return myString

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

def GetListOfEwkDatasets(datasetsMgr):
    Verbose("Getting list of EWK datasets")
    if "noTop" in datasetsMgr.getAllDatasetNames():
        return  ["TT", "noTop", "SingleTop", "ttX"]
    else: # TopSelectionBDT
        return  ["TT", "WJetsToQQ_HT_600ToInf", "SingleTop", "DYJetsToQQHT", "TTZToQQ",  "TTWJetsToQQ", "Diboson", "TTTT"]

def GetSignalDatasets(opts):
    Verbose("Getting signal datasets")
    return dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                dataEra=opts.dataEra,
                                                searchMode=opts.searchMode,
                                                analysisName=opts.analysisName,
                                                includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_",
                                                optimizationMode=opts.optMode)

def GetTTBackgroundDatasets(opts):
    Verbose("Getting TT background datasets")
    return dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                dataEra=opts.dataEra,
                                                searchMode=opts.searchMode,
                                                analysisName=opts.analysisName,
                                                includeOnlyTasks="TT|ST_t|ttbb|TTZToQQ|TTWJetsToQQ|TTTT",
                                                optimizationMode=opts.optMode)
def GetQCDBackgroundDatasets(opts):
    Verbose("Getting QCD background datasets")
    return dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                dataEra=opts.dataEra,
                                                searchMode=opts.searchMode,
                                                analysisName=opts.analysisName,
                                                includeOnlyTasks="QCD_HT",
                                                optimizationMode=opts.optMode)

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
    

#======================
def main(opts):
#======================
    
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
        datasetsToRemove = ["QCD-b", "TTTT"]#, "QCD_HT50to100", "QCD_HT100to200"]#, "QCD_HT200to300"]#, "QCD_HT300to500"]
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0) # ATLAS 13 TeV H->tb exclusion limits
                    
        # Re-order datasets 
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            if "M_" in d.getName():
                if d not in signalMass:
                    continue
            datasetOrder.append(d.getName())    
        for m in signalMass:
            datasetOrder.insert(0, m)
        datasetsMgr.selectAndReorder(datasetOrder)
        

        datasetsMgr.PrintCrossSections()
        datasetsMgr.PrintLuminosities()

        # Custom Filtering of datasets 
        for i, d in enumerate(datasetsToRemove, 0):
            msg = "Removing dataset %s" % d
            Print(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
            datasetsMgr.remove(filter(lambda name: d in name, datasetsMgr.getAllDatasetNames()))
        if opts.verbose:
            datasetsMgr.PrintInfo()

        # ZJets and DYJets overlap
        if "ZJetsToQQ_HT600toInf" in datasetsMgr.getAllDatasetNames() and "DYJetsToQQ_HT180" in datasetsMgr.getAllDatasetNames():
            Print("Cannot use both ZJetsToQQ and DYJetsToQQ due to duplicate events? Investigate. Removing ZJetsToQQ datasets for now ..", True)
            datasetsMgr.remove(filter(lambda name: "ZJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Get Luminosity
        intLumi = datasetsMgr.getDataset("Data").getLuminosity()

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets(datasetsMgr))
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()
        
        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(opts.gridX)
        style.setGridY(opts.gridY)

        # Get histogram list
        folder     = opts.folder
        histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)
        histoPaths1 = [os.path.join(folder, h) for h in histoList]
        histoPaths2 = [h for h in histoPaths1 if "jet" not in h.lower()]
        nHistos     = len(histoPaths2)
        
        # Calculate Signal Significance for all histograms
        for h in histoList:
            PlotSignificance(h, datasetsMgr, intLumi) 
    return


def getHisto(datasetsMgr, histoName, dataset, intLumi):
    h = datasetsMgr.getDataset(dataset).getDatasetRootHisto(opts.folder+"/"+histoName)
    h.normalizeToLuminosity(intLumi)
    return h.getHistogram()

def PlotSignificance(h, datasetsMgr, intLumi):
    Verbose("Plotting Significance")
    
    significanceList = [] 
    
    for mass in signalMass:
        
        xValues = []
        yValues = []
        
        maxSignificance = 0.0
    
        hSignal     = getHisto(datasetsMgr, h, mass, intLumi)
        hBackground = getHisto(datasetsMgr, h, "QCD", intLumi)
        
        for i in range (0, hSignal.GetXaxis().GetNbins()):
        
            # Cut value 
            cut = hSignal.GetBinCenter(i)
        
            s = hSignal.Integral(i, hSignal.GetXaxis().GetNbins())
            b = hBackground.Integral(i, hSignal.GetXaxis().GetNbins())
            
            significance = float(s)/math.sqrt(float(b+s))
            
            if (significance > maxSignificance):
                maxSignificance = significance
                maxSignificanceCut = cut
                
            xValues.append(cut)
            yValues.append(significance)
        
        # Create the Significance Plot
        tGraph = ROOT.TGraph(len(xValues), array.array("d", xValues), array.array("d", yValues))
        styles.getSignalStyleHToTB_M(mass.split("_")[-1]).apply(tGraph)
        

        drawStyle = "CPE"
        legName   = plots._legendLabels[mass]
        significanceGraph = histograms.HistoGraph(tGraph, legName, "lp", drawStyle)
        significanceList.append(significanceGraph)
        
    saveName = "QGLRSignificance"
    
    # Create the plot with all the significance plots
    p = plots.PlotBase(significanceList, saveFormats=["pdf"])
    p.createFrame(saveName)
    
    # Customise frame
    p.setEnergy("13")
    p.getFrame().GetYaxis().SetLabelSize(18)
    p.getFrame().GetXaxis().SetLabelSize(20)
    
    p.getFrame().GetYaxis().SetTitle("S/#sqrt{S+B} / 0.01")
    p.getFrame().GetXaxis().SetTitle("QGLR Cut")
    
    # Add Standard Texts to plot
    histograms.addStandardTexts()
    
    # Customise Legend                                                                                                                                                                                   
    moveLegend = {"dx": -0.15, "dy": -0.5, "dh": -0.1}
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    p.draw()
    
    savePath = opts.saveDir
    if opts.url:
        savePath = opts.saveDir.replace("/publicweb/m/mkolosov/", "http://home.fnal.gov/~mkolosov/")
        
    savePath = os.path.join(opts.saveDir, opts.folder, saveName, opts.optMode)
    SavePlot(p, saveName, savePath)
            
    return 


def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h = tefficiency.GetCopyTotalHisto()
    n = h.GetNbinsX()
    for i in range(1,n+1):
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
        
        # Hack to prevent error going above 1
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
    return ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                  array.array("d",y),
                                  array.array("d",xerrl),
                                  array.array("d",xerrh),
                                  array.array("d",yerrl),
                                  array.array("d",yerrh))




def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):
    
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) )) 

    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_").replace(" ", "").replace("(", "").replace(")", "") )

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/publicweb/m/mkolosov/", "http://home.fnal.gov/~mkolosov/")
        if opts.url:
            Verbose(saveNameURL, i==0)
        else:
            Verbose(saveName + ext, i==0)
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
    ANALYSISNAME = "TestQGLR"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    GRIDX        = False
    GRIDY        = False
    OPTMODE      = None
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    SIGNALMASS   = [200, 500, 800, 1000]
    MERGEEWK     = False
    URL          = True
    NOERROR      = True
    SAVEDIR      = "/publicweb/m/mkolosov/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug' 
    FOLDER       = "TestQGLR_"
    ONLYMC       = False
    RATIO        = False
    NOSTACK      = False

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

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--signalMass", dest="signalMass", type=int, default=SIGNALMASS, 
                     help="Mass value of signal to use [default: %s]" % SIGNALMASS)

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

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--onlyMC", dest="onlyMC", action="store_true", default = ONLYMC,
                      help="Only draw MC datasets, no data: [default: %s]" % (ONLYMC) )

    parser.add_option("--ratio", dest="ratio", action="store_true", default = RATIO,
                      help="Draw ratio canvas for Data/MC curves? [default: %s]" % (RATIO) )

    parser.add_option("--nostack", dest="nostack", action="store_true", default = NOSTACK,
                      help="Do not stack MC histograms [default: %s]" % (NOSTACK) )

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
    else:
        mcrabDir = rchop(opts.mcrab, "/")
        if len(mcrabDir.split("/")) > 1:
            mcrabDir = mcrabDir.split("/")[-1]
        opts.saveDir += mcrabDir


    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Sanity check
    allowedFolders = ["counters", "counters/weighted", "Weighting", "ForDataDrivenCtrlPlots", 
                      "ForDataDrivenCtrlPlotsEWKFakeB", "ForDataDrivenCtrlPlotsEWKGenuineB", "PUDependency", 
                      "Selection_Veto", "muSelection_Veto", "tauSelection_Veto", 
                      "jetSelection_", "bjetSelection_", "metSelection_Baseline",
                      "topologySelection_Baseline", "topbdtSelection_Baseline", 
                      "topbdtSelectionTH2_Baseline", "metSelection_Inverted", 
                      "topologySelection_Inverted", "topbdtSelection_Inverted",
                      "topbdtSelectionTH2_Inverted", "ForFakeBNormalization", 
                      "ForFakeBNormalizationEWKFakeB", "ForFakeBNormalizationEWKGenuineB",
                      "FailedBJet", "FailedBJetFakeB", "FailedBJetGenuineB", "ForFakeBMeasurement", 
                      "ForFakeBMeasurementEWKFakeB", "ForFakeBMeasurementEWKGenuineB",
                      "TestQGLR_", "QuarkGluonLikelihoodRatio_"]

    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()
    
    # Overwrite if certain strings found in folder name
    if 0:
        opts.onlyMC = "EWKFakeB" in opts.folder
        opts.onlyMC = "EWKGenuineB" in opts.folder

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotSignificance.py: Press any key to quit ROOT ...")
