#!/usr/bin/env python
'''
DESCRIPTION:
Script for plotting the significance of several histos


USAGE:
./plotSignif.py -m <pseudo-mcrab> [--options]


EXAMPLES:
./plotSignif.py -m Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442 --intLumi 35800 --logY --cutDir "<="
./plotSignif.py -m Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442 --cutDir ">=" --url --intLumi 35800
./plotSignif.py -m Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442 --cutDir ">=" --url
./plotSignif.py -m Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442 --cutDir ">=" --signalMas "300, 500, 800, 1000"

LAST USED:
./plotSignif.py -m Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40_SigSel_MVA0p85_180214_074442 --cutDir ">=" --signalMass "180, 400, 500"

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
import math
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
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.statisticalFunctions as stat
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
        
    # Apply TDR style
    global style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
    style.setLogX(opts.logX)
    style.setLogY(opts.logY)

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
            datasetsMgr.PrintInfo()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Print merged datasets and MC samples
        if 0:
            datasetsMgr.PrintInfo()

        # Get Luminosity
        if opts.intLumi == 0.0:
            if "Data" in datasetsMgr.getAllDatasetNames():
                opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
            else:
                opts.intLumi = GetLumi(datasetsMgr)

        # Set/Overwrite cross-sections. Remove all but 1 signal mass
        signalsList = []
        for s in opts.signalList:
            signalsList.append("ChargedHiggs_HplusTB_HplusToTB_M_%s" % s)

        # Remove datasets with overlap?
        removeList = ["QCD-b"]
        dsetDY     = "DYJetsToQQ_HT180"
        dsetZJ     = "ZJetsToQQ_HT600toInf"
        dsetRM     = dsetZJ # datasets with overlap
        removeList.append(dsetRM)
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
                if d.getName() not in signalsList:
                    removeList.append(d.getName())

        # Custom filtering of datasets
        for i, d in enumerate(removeList, 1):
            msg = "Removing datasets %s from dataset manager" % (ShellStyles.NoteStyle() + d + ShellStyles.NormalStyle())
            Verbose(msg, i==1)
            datasetsMgr.remove(filter(lambda name: d == name, datasetsMgr.getAllDatasetNames()))


        # Merge EWK samples
        if opts.mergeEWK == "EWK":
            datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        if 1:
            datasetsMgr.PrintInfo()
            
        # Get list of histogram paths
        folder      = opts.folder
        histoList   = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)
        histoPaths  = [os.path.join(folder, h) for h in histoList if "AllSelections" in h]
        myHistos    = []
        skipStrings = ["StandardSelections", "JetPt", "JetEta", "JetEtaPhi", "BJetPt", "BJetEta", 
                       "BtagDiscriminator", "Eta", "LdgTrijetTopMassWMassRatio", "Subldg", "Dijet", 
                       "MET", "MHT", "MinDeltaPhiJetMHT", "MaxDeltaPhiJetMHT", "MinDeltaRJetMHT", "MinDeltaRJetMHTReversed"]

        for h in histoPaths:
            bSkip = False
            for s in skipStrings:
                if s in h:
                    bSkip = True
                    break
            if bSkip:
                continue
            else:
                myHistos.append(h)

        # For-loop: All histograms
        for i, h in enumerate(myHistos, 1):

            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i, "/", "%s:" % (len(myHistos)), h)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)
            PlotHistograms(datasetsMgr, h, signalsList, opts.cutDir)

    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
    return

def GetHistoKwargs(h, opts):

    # Defaults
    if opts.cutDir == ">=":
        xDir = "#geq"
    else:
        xDir = "#leq"
    yMaxF  = 1.2
    yMin   = 0.0
    ylabel = "S/#sqrt{S+B}"
    if opts.logX:
        xMin = 1e-3
    if opts.logY:
        yMin    = 1e-2
        yMaxF   = 2
    cutBox      = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True} #box = True works
    cutBoxY     = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True,
                   "mainCanvas": True, "ratioCanvas": False} # box = True not working
    kwargs = {
        "ylabel"           : ylabel,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "ymin"             : yMin,
        "logy"             : opts.logY,
        "cutBox"           : cutBox,
        "cutBoxY"          : cutBoxY,
        #"opts"             : {"xmin": None, "xmax": None},
        "moveLegend"       : {"dx": -0.08, "dy": -0.01, "dh": +0.15}, #hack to remove legend (tmp)
        }

    if "njets" in h.lower():
        units             = ""
        kwargs["xlabel"]  = "jet multiplicity"
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        #kwargs["opts"]    = {"xmin": 0.0, "xmax": +14.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["opts"]    = {"ymin": yMin, "ymaxfactor": yMaxF}
        ROOT.gStyle.SetNdivisions(8, "X")
        ROOT.gStyle.SetNdivisions(8, "Y")

    if "nbjets" in h.lower():
        units             = ""
        kwargs["xlabel"]  = "b-jet multiplicity"
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax":10.0, "ymin": yMin, "ymaxfactor": yMaxF}
        
    if "nvertices" in h.lower():
        units             = ""
        kwargs["xlabel"]  = "vertex multiplicity"
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]    = {"ymin": yMin, "ymaxfactor": yMaxF}

    if "pt" in h.lower():
        units             = "GeV/c"
        kwargs["xlabel"]  = "p_{T} (%s)" % (units)
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 800.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "trijetmass" in h.lower():
        units             = "GeV/c^{2}"
        kwargs["xlabel"]  = "m_{jjb} (%s)" % (units)
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 300.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "tetrajetmass" in h.lower():
        units             = "GeV/c^{2}"
        kwargs["xlabel"]  = "m_{jjbb} (%s)" % (units)
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]    = {"xmin": 0.0, "xmax": 2000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        ROOT.gStyle.SetNdivisions(8, "X")
        ROOT.gStyle.SetNdivisions(8, "Y")

    if "ht_" in h.lower():
        units             = "GeV"
        kwargs["xlabel"]  = "H_{T} (%s)" % (units)
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1 #[500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000]#, 5000]
        kwargs["opts"]    = {"xmin": 500.0, "xmax": 3000.0, "ymin": yMin, "ymaxfactor": yMaxF}

    # Additional tweeks
    kwargs["xlabel"] += " (%s)" % (xDir)        
    return kwargs
    

def PlotHistograms(datasetsMgr, histoName, signalsList, cutDir):

    # Get Histogram name and its kwargs
    saveName = histoName.rsplit("/")[-1]
    kwargs   = GetHistoKwargs(saveName, opts)

    # Create the plot    
    if "Data" in datasetsMgr.getAllDatasetNames():
        p1 = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])
    else:
        if opts.normalizeToLumi:
            p1 = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi, saveFormats=[])
        #elif opts.normalizeByCrossSection:
        #    p1 = plots.MCPlot(datasetsMgr, histoName, normalizeByCrossSection=True, saveFormats=[], **{})
        else:
            raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")
            
    # Create significance plots
    hList = []
    for s in signalsList:
        hList.append(GetSignificanceHisto(p1, datasetsMgr, cutDir=cutDir, signalDataset=s))
    #p2 = plots.ComparisonManyPlot(hList[0], hList[1:])
    p2 = plots.PlotBase(hList, saveFormats=[])
    p2.setLuminosity(opts.intLumi)

    # Drawing style
    # p2.histoMgr.setHistoDrawStyleAll("LP")
    # p2.histoMgr.setHistoLegendStyleAll("LP")
    p2.histoMgr.setHistoDrawStyleAll("HIST")
    p2.histoMgr.setHistoLegendStyleAll("L")
    p2.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerSize(1.0))
    p2.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
    p2.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetMarkerStyle(ROOT.kFullCircle))

    # Draw the plot
    style.setLogX(opts.logX)
    style.setLogY(opts.logY)
    plots.drawPlot(p1, saveName, **kwargs)
    # SavePlot(p1, saveName, os.path.join(opts.saveDir), [".png", ".pdf"] )

    # Draw the significance
    xMax, yMax = getXMaxYMax(hList)
    kwargs["opts"]["ymax"] = yMax*kwargs["opts"]["ymaxfactor"]
    kwargs["cutBox"]       = {"cutValue": xMax, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    kwargs["cutBoxY"]      = {"cutValue": yMax, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
    kwargs["moveLegend"]["dh"] = -0.15
    
    for s in signalsList:
        p2.histoMgr.setHistoLegendLabelMany({
                s:  plots._legendLabels[s]
                })

    if cutDir == ">=":
        name = saveName + "_Signif" + "GE"
    else:
        name = saveName + "_Signif" + "LE"
    plots.drawPlot(p2, name, **kwargs) 
    SavePlot(p2, name, os.path.join(opts.saveDir), [".png"])#, ".pdf"] )
    return

     
def getXMaxYMax(refList):
    
    nBins = refList[0].GetNbinsX()+1
    yMax  = -999.9
    xMax  = 0.0

    # For-loop: All histos
    for i, h in enumerate(refList, 1):
        # For-loop: All histo bins
        for j in range(0, nBins+1):
            y = h.GetBinContent(j)
            if y >= yMax:
                yMax = y
                #xMax = h.GetBinCenter(j)
                xMax = h.GetBinLowEdge(j)
    return xMax, yMax

def GetSignificanceHisto(p, datasetsMgr, cutDir=">=", signalDataset="ChargedHiggs_HplusTB_HplusToTB_M_500"):
    allowedDirs = [">=", "<="]
    if cutDir not in allowedDirs:
        raise Exception("Unsupported cut direction \"%s\". Please select from > and <" % (cutDir))

    p.setLuminosity(opts.intLumi)
    if type(signalDataset) != str:
        siganlDataset = str(signalDataset)

    hSignal = p.histoMgr.getHisto(signalDataset).getRootHisto().Clone(signalDataset + "_Histo")
    hSignif = p.histoMgr.getHisto(signalDataset).getRootHisto().Clone(signalDataset)
    hSignif.Reset()
    hBkg = p.histoMgr.getHisto(signalDataset).getRootHisto().Clone("Bkg")
    hBkg.Reset()
    
    # For-loop: All dataset names
    for dset in datasetsMgr.getAllDatasets():
        d = dset.getName()
        if dset.isData():
            continue
        if "Charged" in d:
            continue
        
        # Add up all bkg MC
        hBkg.Add(p.histoMgr.getHisto(d).getRootHisto(), +1)
        
    nBins = hSignif.GetNbinsX()+1
    # For-loop: All histo bins
    for i in range (1, nBins+1):
        sigmaB = ROOT.Double(0)
        if cutDir == ">=":
            s = hSignal.Integral(i, nBins)
            b = hBkg.IntegralAndError(i, nBins, sigmaB)
        else:
            s = hSignal.Integral(0, i)
            b = hBkg.IntegralAndError(0, i, sigmaB)
            
        # Calculate the significance
        signif = stat.significance(s, b, sigmaB, option="Asimov")
        Verbose("%s, bin %i: Signif = %.3f" % (hSignif.GetName(), i, signif), i==0)

        if 0:
            Print("%s, bin %i: Signif = %.3f" % (hSignif.GetName(), i, signif), True)
            signif = stat.significance(s, b, sigmaB=0.0, option="Simple")
            signif = stat.significance(s, b, sigmaB=0.0, option="Asimov")
            signif = stat.significance(s, b, sigmaB, option="Simple")
            signif = stat.significance(s, b, sigmaB, option="Asimov")

        # Set signif for this bin
        hSignif.SetBinContent(i, signif)
        
    # Apply style
    s = styles.getSignalStyleHToTB_M(hSignif.GetName().split("_")[-1])
    s.apply(hSignif)
    return hSignif

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
    OPTMODE      = None
    BATCHMODE    = True
    GRIDX        = True
    GRIDY        = True
    LOGX         = False
    LOGY         = False
    MERGEEWK     = False
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    FOLDER       = "ForDataDrivenCtrlPlots" #"topbdtSelection_" #jetSelection_
    CUTDIR       = ">=" # "<="
    SIGNALMASS   = "200, 500, 800" #"800"
    SIGNAL       = None
    INTLUMI      = 0.0
    #NORM2XSEC    = False
    NORM2LUMI    = True

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

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--cutDir", dest="cutDir", type="string", default=CUTDIR, 
                      help="Cut direction for significance plots [default: %s]" % CUTDIR)

    parser.add_option("--signalMass", dest="signalMass", type=str, default=SIGNALMASS,
                     help="Mass value(s) of signal to use. Separate several values with a comma [default: %s]" % SIGNALMASS)

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--logX", dest="logX", action="store_true", default=LOGX, 
                      help="Set x-axis to logarithm scale [default: %s]" % LOGX)

    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY,
                      help="Set y-axis to logarithm scale [default: %s]" % LOGY)

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

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default = MERGEEWK,
                      help="Merge EWK datasets into a single dataset? [default: %s]" % (MERGEEWK) )

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    #parser.add_option("--normalizeByCrossSection", dest="normalizeByCrossSection", action="store_true", default=NORM2XSEC,
     #                 help="Normalise plot by cross-section [default: %s]" % NORM2XSEC)

    parser.add_option("--normalizeToLumi", dest="normalizeToLumi", action="store_true", default=NORM2LUMI,
                      help="Normalise plot to luminosity [default: %s]" % NORM2LUMI)

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
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="Significance")

    #if opts.normalizeByCrossSection == False and opts.normalizeToLumi == False:
        #raise Exception("One of the options --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")

    # Sanity check
    allowedFolders = ["counters", "counters/weighted", "PUDependency", "Weighting", 
                      "eSelection_Veto", "muSelection_Veto", "tauSelection_Veto",
                      "ForDataDrivenCtrlPlotsEWKFakeB", "ForDataDrivenCtrlPlotsEWKGenuineB",
                      "jetSelection_", "bjetSelection_", "metSelection_", 
                      "topologySelection_", "topbdtSelection_", "ForDataDrivenCtrlPlots"]

    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

     # Sanity check
    allowedMass = ["180", "200", "220", "250", "300", "350", "400", 
                   "500", "650", "800", "1000", "1500", "2000", "2500", "3000", "5000", "7000"]
    opts.signalList = opts.signalMass.split(",")
    # Remove spaces from mass points
    for i, s in enumerate(opts.signalList, 0):
        opts.signalList[i] = s.replace(" ", "")

    for s in opts.signalList:
        if s not in allowedMass:
            Print("Invalid signal mass point (=%s) selected! Please select one of the following:" % (s), True)
            for m in allowedMass:
                Print(m, False)
            sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotTH1.py: Press any key to quit ROOT ...")
