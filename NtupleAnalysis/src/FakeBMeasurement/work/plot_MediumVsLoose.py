#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plot_MediumVsLoose.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:



LAST USED:
./plot_MediumVsLoose.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDTm0p80_AllSelections_BDT0p90_RandomSort_171115_101036 -e "Charged" --url --plotEWK

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
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
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


def rchop(myString, endString):
  if myString.endswith(endString):
    return myString[:-len(endString)]
  return myString


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

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(True) #opts.gridX)
    style.setGridY(True) #opts.gridY)
    style.setLogX(False) #opts.logX)
    style.setLogY(False) #opts.logY)

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

        if 0:
            datasetsMgr.printSelections()
        
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

        # ZJets and DYJets overlap!
        if "ZJetsToQQ_HT600toInf" in datasetsMgr.getAllDatasetNames() and "DYJetsToQQ_HT180" in datasetsMgr.getAllDatasetNames():
            Print("Cannot use both ZJetsToQQ and DYJetsToQQ due to duplicate events? Investigate. Removing ZJetsToQQ datasets for now ..", True)
            datasetsMgr.remove(filter(lambda name: "ZJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        datasetsMgr.PrintInfo()
   
        # Get Luminosity
        if opts.intLumi < 0:
            if "Data" in datasetsMgr.getAllDatasetNames():
                opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
            else:
                opts.intLumi = 1.0

        # Re-order datasets (different for inverted than default=baseline)
        if 1:
            newOrder = ["Data"]
            newOrder.extend(aux.GetListOfEwkDatasets())
            datasetsMgr.selectAndReorder(newOrder)

        # Merge EWK samples
        datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Get all histogram names in the given ROOT folder
        histoNames = datasetsMgr.getAllDatasets()[0].getDirectoryContent(opts.folder)
        histoList  = [os.path.join(opts.folder, h) for h in histoNames if "_SR" in h]

        # For-loop: All histos in SR
        nHistos = len(histoList)
        for i, h in enumerate(histoList, 1):

            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i,"/", "%s:" % (nHistos), h)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)
            PlotHistograms(datasetsMgr, h)

    # Inform user where the plots where saved
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
    return


def GetHistoKwargs(h, opts):

    # Defaults    
    yMaxF = 1.2
    _opts = {"ymin": 0.0, "ymaxfactor": yMaxF}
    if opts.normalizeToLumi:
        yLabel = "Events"
        _opts  = {"ymin": 1e-1, "ymaxfactor": yMaxF}
    elif opts.normalizeByCrossSection:
        yLabel  = "#sigma (pb)"
        _opts  = {"ymin": 1e-3, "ymaxfactor": yMaxF}
    elif opts.normalizeToOne:
        yLabel  = "Arbitrary Units"
        _opts  = {"ymin": 1e-4, "ymax": 1.2}
    else:
        yLabel = "Unknown"
    cutBox     = {"cutValue": 400.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True} #box = True works
    cutBoxY    = {"cutValue": 200.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True,
                   "mainCanvas": True, "ratioCanvas": False} # box = True not working

    kwargs = {
        #"xlabel"           : xlabel,
        "ylabel"           : yLabel,
        #"ratioYlabel"      : "Ratio",
        "ratio"            : True,
        #"ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": opts.normalizeToLumi,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : _opts,
        "opts2"            : {"ymin": 0.3, "ymax": 1.7},
        "log"              : True,
        "cutBox"           : cutBox,
        "cutBoxY"          : cutBoxY,
        "moveLegend"       : {"dx": 0.02, "dy": -0.01, "dh": -0.12}, #hack to remove legend (tmp)
        }

    if "nbjetsmedium" in h.lower():
        units             = ""
        kwargs["xlabel"]  = "b-jet multiplicity (CSVv2-M)"
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]["xmax"] = 10.0
        #ROOT.gStyle.SetNdivisions(8, "X")
        #ROOT.gStyle.SetNdivisions(8, "Y")

    if "nbjetsloose" in h.lower():
        units             = ""
        kwargs["xlabel"]  = "b-jet multiplicity (CSVv2-L)"
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = cutBox
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]["xmax"] = 10.0

    if "bdisc" in h.lower():
        kwargs["ylabel"] += " / %.2f"
        kwargs["cutBox"]  = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True} # Loose = 0.5426, Medium = 0.8484, Tight = 0.9535
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]["xmin"] = 0.5
        if "medium" in h.lower():
            kwargs["opts"]["xmin"] = 0.8
        kwargs["opts"]["xmax"] = 1.0
        #kwargs["moveLegend"]   = {"dx": 0.05, "dy": -0.41, "dh": -0.12}
        ROOT.gStyle.SetNdivisions(8, "X")
        ROOT.gStyle.SetNdivisions(8, "Y")

    if "bjetseta" in h.lower():
        kwargs["ylabel"] += " / %.2f"
        kwargs["cutBox"]  = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True} # Loose = 0.5426, Medium = 0.8484, Tight = 0.9535
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = 1
        kwargs["opts"]["xmin"] = -2.5
        kwargs["opts"]["xmax"] = +2.5
        #ROOT.gStyle.SetNdivisions(8, "X")
        #ROOT.gStyle.SetNdivisions(8, "Y")

    if "bjetspt" in h.lower():
        units             = "GeV/c"
        kwargs["ylabel"] += " / %.0f " + units
        kwargs["cutBox"]  = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        kwargs["cutBoxY"] = cutBoxY
        kwargs["rebinX"]  = [b for b in range(0, 600, 20)]
    return kwargs


def PlotHistograms(datasetsMgr, histoName):

    # Get Histogram name and its kwargs
    rootHistos  = []
    regionsList = ["SR", "VR", "CRone", "CRtwo"]
    hRegion     = histoName.split("_")[-1]
    saveName    = histoName.rsplit("/")[-1]
    saveName    = saveName.replace("_" + hRegion, "")
    kwargs      = GetHistoKwargs(saveName, opts)
    myRegions   = []

    # For-loop: All histograms in all regions
    for region in regionsList:
        hName = histoName.replace(hRegion, region)
        if "Data" in datasetsMgr.getAllDatasetNames():
            p = plots.DataMCPlot(datasetsMgr, hName, saveFormats=[])
        else:
            if opts.normalizeToLumi:
                p = plots.MCPlot(datasetsMgr, hName, normalizeToLumi=opts.intLumi, saveFormats=[])
            elif opts.normalizeByCrossSection:
                p = plots.MCPlot(datasetsMgr, hName, normalizeByCrossSection=True, saveFormats=[], **{})
            elif opts.normalizeToOne:
                p = plots.MCPlot(datasetsMgr, hName, normalizeToOne=True, saveFormats=[], **{})
            else:
                raise Exception("One of the options --normalizeToOne, --normalizeByCrossSection, --normalizeToLumi must be enabled (set to \"True\").")
            
        # Append (non-emptty) dataset ROOT histos to a list for plotting
        drh = datasetsMgr.getDataset(opts.dataset).getDatasetRootHisto(hName)
        if drh._getSumHistogram().getRootHisto().Integral() > 0.0:
            drh.setName(region)
            rootHistos.append(drh)
            myRegions.append(region)

    # Create a comparison plot for a given dataset in all CRs
    if len(rootHistos) == 0:
        return
    else:
        p = plots.ComparisonManyPlot(rootHistos[0], rootHistos[1:], saveFormats=[])
        p.setLuminosity(opts.intLumi)

    if opts.normalizeToOne:
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().Scale(1.0/h.getRootHisto().Integral()))

    # Drawing style
    p.histoMgr.setHistoDrawStyleAll("AP")
    p.histoMgr.setHistoLegendStyleAll("LP")

    # Apply styles
    for h in rootHistos:
        region = h.getName()
        if region == "SR":
            styles.fakeBLineStyle1.apply(p.histoMgr.getHisto(region).getRootHisto())
            p.histoMgr.setHistoDrawStyle(region, "HIST")
            p.histoMgr.setHistoLegendStyle(region, "L")
        else:
            styles.getABCDStyle(region).apply(p.histoMgr.getHisto(region).getRootHisto())

    # Add dataset name on canvas
    p.appendPlotObject(histograms.PlotText(0.18, 0.88, plots._legendLabels[opts.dataset], bold=True, size=22))

    # Set legend labels
    if "CRone" in myRegions:
        p.histoMgr.setHistoLegendLabelMany({
                "CRone" : "CR1",
                })
    if "CRtwo" in myRegions:
        p.histoMgr.setHistoLegendLabelMany({
                "CRtwo" : "CR2",
                })

    # Draw the plot
    plots.drawPlot(p, saveName, **kwargs) #the "**" unpacks the kwargs_ dictionary

    # Save the plots in custom list of saveFormats
    SavePlot(p, saveName, os.path.join(opts.saveDir), [".png"])#, ".pdf"] )
    return

def GetCRLabel(region):
    if "CRone":
        return "CR1"
    elif "CRtwo":
        return "CR2"
    else:
        return region

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
    ANALYSISNAME = "FakeBMeasurement"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    DATASET      = "Data"
    OPTMODE      = ""
    BATCHMODE    = True
    INTLUMI      = -1.0
    NORM2ONE     = False
    NORM2XSEC    = False
    NORM2LUMI    = False
    MCONLY       = False
    PLOTEWK      = True
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    FOLDER       = "ForFakeBMediumVsLoose"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("--normalizeToOne", dest="normalizeToOne", action="store_true", default=NORM2ONE,
                      help="Normalise plot to one [default: %s]" % NORM2ONE)

    parser.add_option("--normalizeByCrossSection", dest="normalizeByCrossSection", action="store_true", default=NORM2XSEC,
                      help="Normalise plot by cross-section [default: %s]" % NORM2XSEC)

    parser.add_option("--normalizeToLumi", dest="normalizeToLumi", action="store_true", default=NORM2LUMI,
                      help="Normalise plot to luminosity [default: %s]" % NORM2LUMI)

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("--dataset", dest="dataset", type="string", default=DATASET, 
                      help="Dataset to consider when plotting all 4 Control Regions (CRs) [default: %s]" % DATASET)

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

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="MediumVsLoose")

        
    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotQCD_FailedBJet.py: Press any key to quit ROOT ...")
