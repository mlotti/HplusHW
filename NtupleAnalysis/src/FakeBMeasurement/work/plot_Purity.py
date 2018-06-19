#!/usr/bin/env python
'''
DESCRIPTION:
Plots purity of FakeB (or GenuineB or QCD or EWK) in all Control Regions (CR)
on the same cavnas. More specifically, this script plots the FakeB (or GenuineB or QCD or EWK) 
Purity for VR, CR1, and CR2.


USAGE:
./plot_Purity.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE1_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180108_043300/ --folder ForFakeBMeasurement --doEWK
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE1_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180108_043300/ --folder ForFakeBMeasurement --doEWK --doQCD
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE0_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180107_122559/ --url --doQCD
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE1_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180108_043300/ --folder ForFakeBMeasurement


LAST USED:
1) Fake-B
./plot_Purity.py -m FakeBMeasurement_180614_034501_NewTopAndBugFix_BDT_G0p00_BDT_L0p40_Pt55_110_AbsEta0p8_1p6/ 
2) Genuine-B
./plot_Purity.py -m FakeBMeasurement_180614_034501_NewTopAndBugFix_BDT_G0p00_BDT_L0p40_Pt55_110_AbsEta0p8_1p6/ --doEWK
3) QCD
./plot_Purity.py -m FakeBMeasurement_180614_034501_NewTopAndBugFix_BDT_G0p00_BDT_L0p40_Pt55_110_AbsEta0p8_1p6/ --doQCD
3) EWK
./plot_Purity.py -m FakeBMeasurement_180614_034501_NewTopAndBugFix_BDT_G0p00_BDT_L0p40_Pt55_110_AbsEta0p8_1p6/ --doEWK --doQCD


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
    style.setGridX(False)
    style.setGridY(False)
    style.setOptStat(False)
    
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
        
        # Print PSets used for FakeBMeasurement
        if 0:
            datasetsMgr.printSelections()
            PrintPSet("BJetSelection", datasetsMgr)
            PrintPSet("TopSelectionBDT", datasetsMgr)
            PrintPSet("FakeBMeasurement", datasetsMgr)
            sys.exit()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()
            datasetsMgr.PrintInfo()

        # Filter the datasets 
        datasetsMgr.remove(filter(lambda name: "Charged" in name, datasetsMgr.getAllDatasetNames()))
        # datasetsMgr.remove(filter(lambda name: "Charged" in name and not "M_500" in name, datasetsMgr.getAllDatasetNames()))

        # ZJets and DYJets overlap!
        if "ZJetsToQQ_HT600toInf" in datasetsMgr.getAllDatasetNames() and "DYJetsToQQ_HT180" in datasetsMgr.getAllDatasetNames():
            Print("Cannot use both ZJetsToQQ and DYJetsToQQ due to duplicate events? Investigate. Removing ZJetsToQQ datasets for now ..", True)
            datasetsMgr.remove(filter(lambda name: "ZJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Get Luminosity
        if opts.intLumi < 0:
            if "Data" in datasetsMgr.getAllDatasetNames():
                opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
            else:
                opts.intLumi = 1.0

        # Re-order datasets (different for inverted than default=baseline)
        if 0:
            newOrder = ["Data"]
            newOrder.extend(aux.GetListOfEwkDatasets())
            datasetsMgr.selectAndReorder(newOrder)

        # Print post-merged data dataset summary
        if 0:
            datasetsMgr.PrintInfo()

        # Merge EWK samples
        datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()
            
        # Print post EWK-merge dataset summary
        if 1:
            datasetsMgr.PrintInfo()

        # Get all histograms from the  in the selected folder inside the ROOT files 
        allHistos = datasetsMgr.getAllDatasets()[0].getDirectoryContent(opts.folder)
        hList     = [h for h in allHistos if "CRSelections" in h and "_Vs" not in h]
        hList.extend([h for h in allHistos if "AllSelections" in h and "_Vs" not in h])
        # hList.extend([h for h in allHistos if "StandardSelections" in h and "_Vs" not in h])

        # Create a list with strings included in the histogram names you want to plot
        myHistos = ["LdgTrijetPt", "LdgTrijetMass",  "TetrajetBJetPt", "TetrajetBJetEta", "LdgTetrajetPt", "LdgTetrajetMass", "MVAmax2", "MVAmax1", "HT", "MET"]
        
        # For-loop: All histos
        for i, h in enumerate(myHistos, 1):
            hGraphList = []
            for b in ["Baseline_", "Inverted_"]:
                for r in [ "_AfterCRSelections", "_AfterAllSelections"]:
                    histoName = b + h + r
                    hgQCD, kwargs = GetPurityHistoGraph(datasetsMgr, opts.folder, histoName)

                    # Do not draw SR in multigraph plot!
                    if GetControlRegionLabel(histoName) != "SR":
                        hGraphList.append(hgQCD)

                    # Plot individual purity graphs?
                    if 0:
                        PlotHistoGraph(hgQCD, kwargs)

            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i, "/", "%s:" % (len(myHistos)), h)
            if i>1:
                break
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)
            
            PlotHistoGraphs(hGraphList, kwargs)
    
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
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


def PlotHistoGraph(histoGraph, _kwargs):
    histoName = _kwargs["histoName"]

    # Make the plots
    p = plots.PlotBase( [histoGraph], saveFormats=[])
    # p = plots.ComparisonManyPlot(histoGraph, [histoGraph1, histoGraph2], saveFormats=[])

    # Draw the plots
    plots.drawPlot(p, histoName,  **_kwargs)
    
    # Save the plots
    histoName = histoName.replace("ForFakeBMeasurement/", "")
    histoName = GetSaveName(histoName)
    SavePlot(p, histoName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf", ".C"] )
    return


def GetPurityHistoGraph(datasetsMgr, folder, hName):

    # Which folder to use (Inclusive or GenuineB?)
    genuineBFolder = folder + "EWKGenuineB"
    fakeBFolder    = folder + "EWKFakeB"    
    histoName_Incl = os.path.join(folder, hName)
    histoName_Gen  = os.path.join(genuineBFolder, hName)
    
    # Get histogram customisations
    _kwargs  = GetHistoKwargs(histoName_Incl, opts)

    # Get histos (Data, EWK) for Inclusive
    pIncl = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName_Incl) )
    pGen  = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName_Gen) )

    # Save name for future use
    _kwargs["histoName"] = histoName_Incl

    # Normalise to luminosity
    pIncl.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())
    pGen.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Clone histograms 
    Data  = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    FakeB = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("FakeB")
    QCD   = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("QCD")
    EWK   = pIncl.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK")
    GenB  = pGen.histoMgr.getHisto("EWK").getRootHisto().Clone("GenuineB")

    # Rebin histograms (Before calculating Purity)
    if "binList" in _kwargs:
        xBins = _kwargs["binList"]
        nx    = len(xBins)-1
        Data  = Data.Rebin(nx , "", xBins)
        FakeB = FakeB.Rebin(nx, "", xBins)
        QCD   = QCD.Rebin(nx  , "", xBins)
        EWK   = EWK.Rebin(nx  , "", xBins)
        GenB  = GenB.Rebin(nx , "", xBins)

    # FakeB = Data - EWK_GenuineB ; QCD = Data-EWK
    FakeB.Add(GenB, -1)
    QCD.Add(EWK, -1)


    # Create the Purity histos
    if opts.type == "FakeB":
        if 1:
            hPurity = GetPurityHisto(Data, GenB, _kwargs, subtractFromOne=True, printValues=False, hideZeros=False) 
        else: #equivalent
            hPurity = GetPurityHisto(Data, FakeB, _kwargs, subtractFromOne=False, printValues=False, hideZeros=False) 
    elif opts.type == "GenuineB":
        if 1:
            hPurity = GetPurityHisto(Data, GenB, _kwargs, subtractFromOne=False, printValues=False, hideZeros=False)
        else:#equivalent
            hPurity = GetPurityHisto(Data, FakeB, _kwargs, subtractFromOne=True, printValues=False, hideZeros=False) 
    elif opts.type == "QCD":
        hPurity = GetPurityHisto(Data, EWK, _kwargs, subtractFromOne=True, printValues=False, hideZeros=False)
    elif opts.type == "EWK":
        hPurity = GetPurityHisto(Data, EWK, _kwargs, subtractFromOne=False, printValues=False, hideZeros=False)
    else:
        raise Exception("This should never be reached")
            
    # Convert histos to TGraph
    gPurity = convertHisto2TGraph(hPurity, _kwargs, printValues=False)

    # Set legend label    
    label = "%s (%s)" % (opts.type, GetControlRegionLabel(histoName_Incl))
    label = label.replace("FakeB", "Fake-b").replace("GenuineB", "Genuine-b")

    # Apply random histo styles
    s = styles.getABCDStyle( GetControlRegionLabel(histoName_Incl) )
    s.apply(gPurity)        

    # Create histoGraph object
    hgPurity = histograms.HistoGraph( gPurity, label, "p", "P")

    return hgPurity, _kwargs


def PlotHistoGraphs(hGraphList, _kwargs):

    histoName = _kwargs["histoName"]
    histoName = histoName.replace("ForFakeBMeasurement/", "")
    histoName = histoName.split("_")[1]

    # Overwrite some canvas options
    _kwargs["opts"]["ymin"] = 0.0
    _kwargs["opts"]["ymax"] = 1.02

    # Create & draw the plot    
    p = plots.PlotBase( hGraphList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    plots.drawPlot(p, histoName, **_kwargs)

    # Save the plot
    SavePlot(p, histoName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"] )
    return

def GetHistoKwargs(histoName, opts):
    '''
    Dictionary with
    key   = histogram name
    value = kwargs
    '''
    h = histoName.split("/")[-1]
    histoKwargs = {}
    _moveLegend = {"dx": -0.55, "dy": -0.55, "dh": -0.14}
    _yMin       = 0.0
    _yMax       = 1.09
    _cutBox     = None
    # _cutBoxY    = {"cutValue": 0.85, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
    _cutBoxY    = {"cutValue": 0.85, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
    _xlabel     = "x-axis"
    _bins       = None
    _kwargs     = {
        "xlabel"           : _xlabel,
        "ylabel"           : "Purity",
        #"rebinX"           : 1,
        "ratioYlabel"      : "Ratio",
        "ratio"            : False, #works (but not needed)
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : True,
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        # "opts"             : _opts,
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
        "moveLegend"       : _moveLegend,
        "cutBoxY"          : _cutBoxY
        }

    # Set x-axis divisions
    n1 = 8 # primary divisions
    n2 = 5 # second order divisions
    n3 = 2 # third order divisions
    nDivs = n1 + 100*n2 + 10000*n3
    myBins = []

    if 1:
        ROOT.gStyle.SetNdivisions(nDivs, "X")

    if "ldgtrijetpt" in h.lower():
        _xlabel = "p_{T} (GeV/c)"
        myBins  = systematics._dataDrivenCtrlPlotBinning["LdgTrijetPt_AfterAllSelections"]

    if "eta" in h.lower():
        _xlabel  = "#eta"
        #myBins   = [float(eta)/10.0 for eta in range(-25, 25+1, 1)]
        myBins   = [float(eta)/10.0 for eta in range(-25, 25+5, 5)]

    if "tetrajetbjetpt" in h.lower():
        _xlabel = "p_{T} (GeV/c)"
        myBins   = systematics._dataDrivenCtrlPlotBinning["TetrajetBjetPt_AfterAllSelections"]

    if "ht" in h.lower():
        _xlabel  = "H_{T} (GeV)"
        myBins   = systematics._dataDrivenCtrlPlotBinning["HT_AfterAllSelections"]
        _cutBox  = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    if "met" in h.lower():
        _xlabel  = "E_{T}^{miss} (GeV)"
        myBins   = systematics._dataDrivenCtrlPlotBinning["MET_AfterAllSelections"]
        
    if "mvamax1" in h.lower():
        _xlabel = "top-tag discriminant"
        _cutBox = {"cutValue": 0.40, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        myBins  = [float(mva)/10.0 for mva in range(-10, 11, 1)]

    if "mvamax2" in h.lower():
        _xlabel = "top-tag discriminant"
        _cutBox = {"cutValue": 0.40, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        myBins  = [float(mva)/10.0 for mva in range(-10, 11, 1)]

    if "trijetm" in h.lower():
        _units  = "GeV/c^{2}" 
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        myBins = systematics._dataDrivenCtrlPlotBinning["LdgTrijetMass_AfterAllSelections"]
        
    if "bdisc" in h.lower():
        _units  = "" 
        _xlabel = "b-tag discriminant"
        # _cutBox = {"cutValue": 0.5426, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _cutBox = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        myBins  = [float(i)/10 for i in range(0, 10)]

    if "nbjets" in h.lower():
        _units  = "" 
        _cutBox = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "b-jet multiplicity"
        myBins  = [i for i in range(3, 11)]

    if "njets" in h.lower():
        _units  = "" 
        _cutBox = {"cutValue": 7.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        _xlabel = "jet multiplicity"
        myBins  = [i for i in range(7, 16)]

    if "tetrajetpt" in h.lower():
        _units  = "GeV/c" 
        _xlabel = "p_{T} (%s)" % (_units)
        myBins  = systematics._dataDrivenCtrlPlotBinning["LdgTetrajetPt_AfterAllSelections"]
        #ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

    if "tetrajetm" in h.lower():
        _units  = "GeV/c^{2}" 
        _xlabel = "m_{jjbb} (%s)" % (_units)
        #myBins  = systematics._dataDrivenCtrlPlotBinning["LdgTetrajetMass_AfterAllSelections"]
        myBins  = systematics.getBinningForTetrajetMass(0)
        ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

    _kwargs["opts"]    = {"ymin": _yMin, "ymax": _yMax}
    _kwargs["xlabel"]  = _xlabel
    _kwargs["cutBox"]  = _cutBox
    _kwargs["cutBoxY"] = _cutBoxY

    if len(myBins) > 0:
        _kwargs["binList"] = array.array('d', myBins)
    return _kwargs


def GetSaveName(histoName):
    base = histoName.split("_")[0]
    var  = histoName.split("_")[1]
    sel  = histoName.split("_")[2]
    name = var + "_" + GetControlRegionLabel(histoName)
    return name


def GetControlRegionLabel(histoName):
    histoName = histoName.replace(opts.folder + "/", "")
    base = histoName.split("_")[0]
    var  = histoName.split("_")[1]
    sel  = histoName.split("_")[2]

    if base == "Baseline":
        if sel == "AfterAllSelections":
            return "SR"
        elif sel == "AfterCRSelections":
            return "CR1"
    elif base == "Inverted":
        if sel == "AfterAllSelections":
            return "VR"
        elif sel == "AfterCRSelections":
            return "CR2"
    else:
        raise Exception("Cannot determine Control Region label. Got unexpeted histogram name \"%s\". " % histoName)
    return
    
def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))
    
    # Append dataset name
    saveName += "_" + opts.type

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Verbose(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return

def convertHisto2TGraph(histo, kwargs, printValues=False):

    # Lists for values
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []

    # Other definitions
    xMin   = histo.GetXaxis().GetXmin()
    xMax   = histo.GetXaxis().GetXmax()
    nBinsX = histo.GetNbinsX()
    hName  = kwargs["histoName"]
    title  = "%s (%s)" % (hName.replace(opts.folder+"/", "").rsplit("_")[1], GetControlRegionLabel(hName))


    # For-loop: All histogram bins
    for i in range(1, nBinsX+1):
        
        # Get values
        xVal  = histo.GetBinLowEdge(i) +  0.5*histo.GetBinWidth(i)
        xLow  = 0.5*histo.GetBinWidth(i)
        xHigh = 0.5*histo.GetBinWidth(i)
        yVal  = histo.GetBinContent(i)
        yLow  = histo.GetBinError(i)
        yHigh = yLow            

        # Store values
        x.append(xVal)
        xerrl.append(xLow)
        xerrh.append(xHigh)

        y.append(yVal)
        yerrl.append(yLow)
        yerrh.append(yHigh)

    # Create the TGraph with asymmetric errors
    tgraph = ROOT.TGraphAsymmErrors(nBinsX,
                                    array.array("d",x),
                                    array.array("d",y),
                                    array.array("d",xerrl),
                                    array.array("d",xerrh),
                                    array.array("d",yerrl),
                                    array.array("d",yerrh))

    # Construct info table (debugging)
    table  = []
    align  = "{:>6} {:^10} {:>10} {:>10} {:>10} {:^3} {:<10}"
    header = align.format("#", "xLow", "x", "xUp", "Purity", "+/-", "Error") #Purity = 1-EWK/Data
    hLine  = "="*70
    table.append("")
    table.append(hLine)
    table.append("{:^70}".format(title))
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


def GetPurityHisto(hData, hOther, kwargs, subtractFromOne=True, printValues=False, hideZeros=True):
    '''
    if subtractFromOne:
    P = 1.0 - (EWK / Data)

    if not subtractFromOne:
    P = (EWK / Data)
    '''

    # Prepare a new histo
    h = hData.Clone()    
    h.Reset("ICESM")
    ROOT.SetOwnership(h, True)
    histoName = kwargs["histoName"]
    title = "%s (%s)" % (histoName.replace(opts.folder+"/", "").rsplit("_")[1], GetControlRegionLabel(histoName))

    # Construct info table (debugging)
    table  = []
    align  = "{:>6} {:^20} {:>10} {:>10} {:>10} {:^3} {:<10}"
    header = align.format("Bin", "Range", "%s" % hOther.GetName(), "Data", "Purity", "+/-", "Error") #Purity = 1-EWK/Data
    hLine  = "="*70
    nBinsX = hData.GetNbinsX()
    table.append("{:^70}".format(title))
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # For-loop: All histogram bins
    for j in range (1, nBinsX+1):
        
        # Legacy: No idea why the code snippet I copied used "j=j-1" instead of "i=j". 
        i = j

        # Declare variables
        myPurity       = 0.0
        myPurityUncert = 0.0
        otherSum       = hOther.GetBinContent(i)
        otherSumUncert = hOther.GetBinError(i)
        dataSum        = hData.GetBinContent(i)
        dataSumUncert  = hData.GetBinError(i)  # hData.GetBinContent(i)
        
        # Treat negative bins for EWK (possible if -ve weights are applied)
        if otherSum < 0.0:
            Verbose("Sum is below 0 (Sum=%.3f +/- %.3f). Forcing value to 0.0." % (otherSum,  otherSumUncert))
            otherSum = 0.0 

        # Ignore zero bins
        if abs(dataSum) > 0.000001:
            if subtractFromOne:
                myPurity = 1.0 - otherSum / dataSum
            else:
                myPurity = otherSum / dataSum
            myPurityUncert = errorPropagation.errorPropagationForDivision(otherSum, otherSumUncert, dataSum, dataSumUncert)

        # Bin-range or overflow bin?
        binRange = "%.1f -> %.1f" % (hData.GetXaxis().GetBinLowEdge(j), hData.GetXaxis().GetBinUpEdge(j) )
        if j >= nBinsX:
            binRange = "> %.1f"   % (hData.GetXaxis().GetBinLowEdge(j) )

        # WARNING! Ugly trick so that zero points are not visible on canvas 
        if hideZeros:
            if myPurity == 0.0:
                myPurity       = -0.1
                myPurityUncert = +0.0001

        # Sanity check
        if myPurity > 1.0:
            Print ("Bin %d) %.3f/%.3f = %.3f" % (i, otherSum, dataSum, myPurity), True)
            newPurity = 1.0
            newUncert = myPurityUncert
            Print("Purity exceeds 1.0 (P=%.3f +/- %.3f). Forcing value to P=%.3f +/- %.3f" % (myPurity,  myPurityUncert, newPurity, newUncert), False)
            myPurity  = newPurity                
#            if myPurity < 1.5: # allow a generous 10% for -ve MC weights (TTbar)
#                newPurity = 1.0
#                newUncert = myPurityUncert
#                Print("Purity exceeds 1.0 (P=%.3f +/- %.3f). Forcing value to P=%.3f +/- %.3f" % (myPurity,  myPurityUncert, newPurity, newUncert), False)
#                myPurity  = newPurity                
#            else:
#                raise Exception("Purity cannot exceed 100%% (=%s +/- %s)" % (myPurity*100, myPurityUncert*100) )

        # Fill histogram
        h.SetBinContent(j, myPurity)
        h.SetBinError(j, myPurityUncert)

        # Save information in table
        row = align.format(j, binRange, "%.1f" % otherSum, "%.1f" % dataSum, "%.3f" % myPurity, "+/-", "%.3f" % myPurityUncert)
        table.append(row)
        
    # Finalise table
    table.append(hLine)

    # Print purity as function of final shape bins
    if printValues:
        for i, line in enumerate(table):
            Print(line, i==0)

    return h

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
    ANALYSISNAME = "FakeBMeasurement"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    FOLDER       = "ForFakeBMeasurement"
    BATCHMODE    = True
    INTLUMI      = -1.0
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    DOEWK        = False    
    DOQCD        = False
    TYPE         = "FakeB" 

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("--doEWK", dest="doEWK", action="store_true", default=DOEWK, 
                      help="Plot EWK purity instead of FakeB purity [default: %s]" % (DOEWK) )

    parser.add_option("--doQCD", dest="doQCD", action="store_true", default = DOQCD,
                      help="Plot QCD purity instead of FakeB purity [default: %s]" % (DOQCD))

    parser.add_option("--type", dest="type", type="string", default=TYPE,
                      help="Type of dataset to plot (FakeB, Genuine-b, EWK, QCD) [default: %s]" % (TYPE) )

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
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="Purity")
        
    
    # Sanity checks
    allowedFolders = ["ForDataDrivenCtrlPlots", "ForFakeBMeasurement"]
    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

    allowedTypes = ["FakeB", "GenuineB", "EWK", "QCD"]
    if opts.type not in allowedTypes:
        Print("Invalid type \"%s\"! Please select one of the following:" % (opts.type), True)
        for m in allowedTypes:
            Print(m, False)
        sys.exit()
    

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_Purity.py: Press any key to quit ROOT ...")
