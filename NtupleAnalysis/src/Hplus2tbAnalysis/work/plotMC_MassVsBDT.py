#!/usr/bin/env python
'''
DESCRIPTIONM:
Script that plots Data/MC for all histograms under a given folder (passsed as option to the script)
Good for sanity checks for key points in the cut-flow


USAGE:
./plotMC_MassVsBDT.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plotMC_MassVsBDT.py -m Hplus2tbAnalysis_Preapproval_MVA0p30to0p70_Syst_22Apr2018 --signalMass 180
./plotMC_MassVsBDT.py -m Hplus2tbAnalysis_Preapproval_MVA0p30to0p70_Syst_22Apr2018 --signalMass 200
./plotMC_MassVsBDT.py -m Hplus2tbAnalysis_Preapproval_MVA0p30to0p70_Syst_22Apr2018 --signalMass 300
./plotMC_MassVsBDT.py -m Hplus2tbAnalysis_Preapproval_MVA0p30to0p70_Syst_22Apr2018 --signalMass 500
./plotMC_MassVsBDT.py -m Hplus2tbAnalysis_Preapproval_MVA0p30to0p70_Syst_22Apr2018 --signalMass 1000
./plotMC_MassVsBDT.py -m Hplus2tbAnalysis_Preapproval_MVA0p30to0p70_Syst_22Apr2018 --signalMass 500


LAST USED:
%./plotMC_MassVsBDT.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/BDTcutComparisonPlots_BjetPt40_MassCut400_wSignal  --signalMass 500
./plotMC_MassVsBDT.py -m Hplus2tbAnalysis_Preapproval_MVA0p40_Syst_28Apr2018 --signalMass 500 --url

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import array
import re
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
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
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
        
    # For-loop: All opt Mode
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities(fname="lumi.json")

        # Get Luminosity
        if opts.intLumi < 0:
            if "Data" in datasetsMgr.getAllDatasetNames():
                opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
            else:
                opts.intLumi =  datasetsMgr.loadLumi()

        # Set/Overwrite cross-sections
        datasetsToRemove = []
        for d in datasetsMgr.getAllDatasets():
            mass = "M_%s" % (opts.signalMass)
            if mass in d.getName():
                if ("%s" % opts.signalMass) != d.getName().split("M_")[-1]:
                    datasetsMgr.remove(d.getName())
                else:
                    datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
            else:
                #datasetsToRemove.append(d.getName())
                datasetsMgr.remove(d.getName())

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

#         # Custom Filtering of datasets 
#         for i, d in enumerate(datasetsToRemove, 0):
#             msg = "Removing dataset %s" % d
#             Verbose(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
#             datasetsMgr.remove(filter(lambda name: d == name, datasetsMgr.getAllDatasetNames()))

        if opts.verbose:
            datasetsMgr.PrintInfo()
  
        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(opts.gridX)
        style.setGridY(opts.gridY)

        # Do Data-MC histograms with DataDriven QCD
        folder     = opts.folder
        histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)        
        histoPaths = [os.path.join(folder, h) for h in histoList]
        keepList   = ["LdgTetrajetMass_AfterAllSelections"]
        #keepList   = ["LdgTetrajetMass_AfterStandardSelections"]
        myHistos   = []
        for h in histoPaths:
            if h.split("/")[-1] not in keepList:
                continue
            else:
                myHistos.append(h)

        for i, h in enumerate(myHistos, 1):
            PlotHistograms(datasetsMgr, h)
        
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)    
    return

def GetHistoKwargs(h, opts):

    # Common bin settings
    if opts.signalMass > 500:
        _mvLeg  = {"dx": -0.55, "dy": -0.01, "dh": -0.1}
    else:
        _mvLeg  = {"dx": -0.25, "dy": -0.01, "dh": -0.1}

    _logy   = False
    _yLabel = "Events / %.0f "
    _yMin   = 1e-1
    _yMaxF  = 1.2
    if _logy:
        yMaxF = 20

    _kwargs = {
        "ylabel"           : _yLabel,
        "rebinX"           : 1,
        "rebinY"           : None,
        "ratioType"        : "errorScale",
        "ratioErrorOptions": {"numeratorStatSyst": False},
        "ratioYlabel"      : "Data/MC",
        "ratio"            : opts.ratio, 
        "stackMCHistograms": True,
        "ratioInvert"      : False, 
        "addMCUncertainty" : False, 
        "addLuminosityText": opts.normalizeToLumi,
        "addCmText"        : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": _yMin, "ymaxfactor": _yMaxF},
        "opts2"            : {"ymin": 0.59, "ymax": 1.41},
        "log"              : _logy,
        "moveLegend"       : _mvLeg,
        }

    kwargs = copy.deepcopy(_kwargs)
    
    if "TetrajetMass" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 10 #10
        kwargs["xlabel"] = "m_{jjbb} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +1400.0, "ymin": _yMin, "ymaxfactor": _yMaxF}
        kwargs["cutBox"] = {"cutValue": opts.signalMass, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        ROOT.gStyle.SetNdivisions(8, "X")

    return kwargs
    

def GetBinWidthMinMax(binList):
    if not isinstance(binList, list):
        raise Exception("Argument is not a list instance!")

    minWidth = +1e6
    maxWidth = -1e6
    # For-loop: All bin values (centre)
    for i in range(0, len(binList)-1):
        j = i + 1
        iBin = binList[i]
        jBin = binList[j]
        wBin = jBin-iBin
        if wBin < minWidth:
            minWidth = wBin

        if wBin > maxWidth:
            maxWidth = wBin
    return minWidth, maxWidth

def getHistos(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]

def PlotHistograms(datasetsMgr, histoName):

    # Get Histogram name and its kwargs
    saveName = histoName.rsplit("/")[-1] # histoName.replace("/", "_")
    kwargs_  = GetHistoKwargs(saveName, opts)

    # Create the plotting object
    if "Data" in datasetsMgr.getAllDatasetNames():
        p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])
    else:
        if opts.normalizeToLumi:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi, saveFormats=[])
        elif opts.normalizeByCrossSection:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeByCrossSection=True, saveFormats=[], **{})
        elif opts.normalizeToOne:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToOne=True, saveFormats=[], **{})
        else:
            raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")


    # Overwite signal style?
    style  = [200, 500, 800, 1000, 2000, 3000, 5000]
    lstyle = [ROOT.kSolid, ROOT.kDashed, ROOT.kDashDotted, ROOT.kDotted, ROOT.kDotted, ROOT.kSolid]
    for i, d in enumerate(datasetsMgr.getAllDatasets(), 0):
        p.histoMgr.forHisto(d.getName(), styles.getSignalStyleHToTB_M(style[i]))
    if 1:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))

    p.histoMgr.setHistoLegendLabelMany({
            #"ChargedHiggs_HplusTB_HplusToTB_M_500_MVA0p30": "H^{+} m_{H^{+}} = 500 GeV (BDT #geq 0.3)",
            "ChargedHiggs_HplusTB_HplusToTB_M_%s_MVA0p30" % (opts.signalMass): "m_{H^{+}}=%s GeV (BDT #geq 0.3)" % (opts.signalMass),
            "ChargedHiggs_HplusTB_HplusToTB_M_%s_MVA0p40" % (opts.signalMass): "m_{H^{+}}=%s GeV (BDT #geq 0.4)" % (opts.signalMass),
            "ChargedHiggs_HplusTB_HplusToTB_M_%s_MVA0p50" % (opts.signalMass): "m_{H^{+}}=%s GeV (BDT #geq 0.5)" % (opts.signalMass),
            "ChargedHiggs_HplusTB_HplusToTB_M_%s_MVA0p60" % (opts.signalMass): "m_{H^{+}}=%s GeV (BDT #geq 0.6)" % (opts.signalMass),
            "ChargedHiggs_HplusTB_HplusToTB_M_%s_MVA0p70" % (opts.signalMass): "m_{H^{+}}=%s GeV (BDT #geq 0.7)" % (opts.signalMass),
            })
    
    # Apply blinding of signal region
    if "blindingRangeString" in kwargs_:
        startBlind = float(kwargs_["blindingRangeString"].split("-")[1])
        endBlind   = float(kwargs_["blindingRangeString"].split("-")[0])
        plots.partiallyBlind(p, maxShownValue=startBlind, minShownValue=endBlind, invert=True, moveBlindedText=kwargs_["moveBlindedText"])

    # Draw and save the plot
    saveName += "_M%s" % (opts.signalMass)
    plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary

    # Save the plots in custom list of saveFormats
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode, opts.folder), [".png", ".pdf"] )
    return

def replaceBinLabels(p, histoName):
    '''
    https://root.cern.ch/doc/master/classTAttText.html#T5
    '''
    myBinList = []
    if histoName == "counter" or histoName == "weighted/counter":
        #myBinList = ["#geq 7 jets", "#geq 3 b-jets", "b-jets SF", "#geq 2 tops", "fat-jet veto", "All"]
        myBinList = ["#geq 7 jets", "#geq 3 b-jets", "b-jets SF", "#geq 2 tops", "fat-jet veto", "All"]
    elif "bjet" in histoName:
        myBinList = ["All", "#eta", "p_{T}", "CSVv2 (M)", "Trg Match", "#geq 3"]
    elif "jet" in histoName:
        myBinList = ["All", "jet ID", "PU ID", "#tau match", "#eta", "p_{T}", "#geq 7", "H_{T}", "J_{T}", "MHT"]
    else:
        pass
    for i in range(0, len(myBinList)):
        p.getFrame().GetXaxis().SetBinLabel(i+1, myBinList[i])
        #p.getFrame().GetXaxis().GetBinLabel(i+1).SetTextAngle(90) #not correct
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))
    saveName = saveName.replace(" ", "_")
    saveName = saveName.replace(")", "")
    saveName = saveName.replace("(", "")

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Print(saveNameURL, i==0)
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
    ANALYSISNAME = "Hplus2tbAnalysis"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    GRIDX        = False
    GRIDY        = False
    OPTMODE      = None
    BATCHMODE    = True
    INTLUMI      = -1.0
    SIGNALMASS   = 500
    MERGEEWK     = False
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    RATIO        = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug' 
    FOLDER       = "ForDataDrivenCtrlPlots"
    NORM2LUMI     = True
    NORM2XSECTION = False
    NORM2ONE      = False
    
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

    parser.add_option("--ratio", dest="ratio", action="store_true", default=RATIO,
                      help="Enable ratio pad for Data/Bkg comparison [default: %s]" % RATIO)

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

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--normalizeToLumi", dest="normalizeToLumi", action="store_true", default = NORM2LUMI,
                      help="Normalize MC to luminosity [default: %s]" % (NORM2LUMI) )

    parser.add_option("--normalizeByCrossSection", dest="normalizeByCrossSection", action="store_true", default = NORM2XSECTION,
                      help="Normalize MC to cross-section [default: %s]" % (NORM2XSECTION) )

    parser.add_option("--normalizeToOne", dest="normalizeToOne", action="store_true", default = NORM2ONE,
                      help="Normalize MC to unity [default: %s]" % (NORM2LUMI) )

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

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="DataMC")

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 650, 800, 1000, 2000, 3000]
    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()
    else:
        #opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%i_ext1" % opts.signalMass
        opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotDataMC_ControlPlots.py: Press any key to quit ROOT ...")
