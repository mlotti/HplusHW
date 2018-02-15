#!/usr/bin/env python
'''
Usage:
./plot_Purity.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE1_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180108_043300/ --folder ForFakeBMeasurement --plotEWK
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE1_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180108_043300/ --folder ForFakeBMeasurement --plotEWK --doQCD --url
./plot_Purity.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170627_124436_BJetsGE2_TopChiSqrVar_AllSamples --plotEWK -e 'QCD|Charged'
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE0_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180107_122559/ --url --doQCD --plotEWK 

Last Used:
./plot_Purity.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE1_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180108_043300/ --folder ForFakeBMeasurement

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
import array
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


def GetListOfEwkDatasets(datasetsMgr):
    Verbose("Getting list of EWK datasets")
    if "noTop" in datasetsMgr.getAllDatasetNames():
        return ["TT", "noTop", "SingleTop", "ttX"]
    else:
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
        
        if 1:
            PrintPSet("TopologySelection", datasetsMgr)
            PrintPSet("FakeBMeasurement", datasetsMgr)

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
        #datasetsMgr.remove(filter(lambda name: "Charged" in name and not "M_500" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Re-order datasets (different for inverted than default=baseline)
        if 0:
            newOrder = ["Data"]
            newOrder.extend(GetListOfEwkDatasets(datasetsMgr))
            datasetsMgr.selectAndReorder(newOrder)

        # Print post-merged data dataset summary
        if 0:
            datasetsMgr.PrintInfo()

        # Merge EWK samples
        datasetsMgr.merge("EWK", GetListOfEwkDatasets(datasetsMgr))
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()
            
        # Print dataset information
        if 0:
            datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setGridX(True)
        style.setGridY(True)
        style.setOptStat(True)

        # Do the purity plots
        folder    = opts.folder 
        allHistos = datasetsMgr.getAllDatasets()[0].getDirectoryContent(folder)
        hList     = [h for h in allHistos if "CRSelections" in h and "_Vs" not in h]
        hList.extend([h for h in allHistos if "AllSelections" in h and "_Vs" not in h])
        if 0:
            hList.extend([h for h in allHistos if "StandardSelections" in h and "_Vs" not in h])

        # Only do these histos
        myHistos   = ["LdgTrijetM", "LdgTetrajetMass", "MVAmax2", "MVAmax1", "Njets", "NBjets", 
                      "Bjet3BtagDisc", "Bjet2BtagDisc", "Bjet1BtagDisc", "Bjet3Pt", "Bjet2Pt", "Bjet1Pt"]

        # For-loop: All histos
        for h in hList:
            continue
            if h.split("_")[1] not in myHistos:
                continue
            Print(h, True)
            #PlotPurity(datasetsMgr, folder, h)

        # For-loop: All histos
        for h in myHistos:
            hGraphList = []
            for b in ["Baseline_", "Inverted_"]:
                for r in ["_AfterCRSelections", "_AfterAllSelections" ]:
                    histoName = b + h + r
                    # Get the histoGraphs
                    hgQCD, hgEWK, kwargs = GetPurityHistoGraph(datasetsMgr, folder, histoName)
                    #kwargs["histoName"] = histoName
                    # Plot 
                    PlotHistoGraph(hgQCD, hgEWK, kwargs)
                    hGraphList.append(hgQCD)
            PlotHistoGraphs(hGraphList, kwargs)
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


def PlotPurity(datasetsMgr, folder, hName):
    '''
    Create plots with "FakeB=Data-EWKGenuineB"
    '''
    # Which folder
    genuineBFolder = folder + "EWKGenuineB"
    fakeBFolder    = folder + "EWKFakeB"
    histoName      = os.path.join(folder, hName)
    hNameGenuineB  = os.path.join(genuineBFolder, hName)
    Verbose("Creating purity plot for %s" % (histoName), True)

    # Get histogram customisations
    _kwargs  = GetHistoKwargs(histoName, opts)

    # Get histos (Data, EWK) for Inclusive
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName) )
    if opts.doQCD:
        p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName) )
    else:
        p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, hNameGenuineB) )

    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Clone histograms 
    Data = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    EWK  = p2.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK") # EWKGenuineB
    QCD  = p1.histoMgr.getHisto("Data").getRootHisto().Clone("QCD")

    # Rebin histograms (Before calculating Purity)
    if 0:
        Data.Rebin(_kwargs["rebinX"])
        EWK.Rebin(_kwargs["rebinX"])
        QCD.Rebin(_kwargs["rebinX"])

    # Rebin histograms (Before calculating Purity) # alex: FIXME - make it automatic
    if "binList" in _kwargs:
        xBins   = _kwargs["binList"]
        nx      = len(xBins)-1
        newName = "" 
        Verbose("Setting customly-selected bins %s" % (xBins), True)

        Data = Data.Rebin(nx, "", xBins)
        EWK  = EWK.Rebin(nx, "", xBins)
        QCD  = QCD.Rebin(nx, "", xBins)

    # Get QCD = Data-EWK
    QCD.Add(EWK, -1)

    # Create the Purity histos
    hQCD_Purity  = GetPurityHisto(Data, EWK, _kwargs, printValues=False, hideZeros=True)
    if opts.plotEWK:
        hEWK_Purity  = GetPurityHisto(Data, QCD, _kwargs, printValues=False, hideZeros=True)

    # Convert Purity histos to Purity TGraphs
    gQCD_Purity = convertHisto2TGraph(hQCD_Purity, printValues=False)
    if opts.plotEWK:
        gEWK_Purity = convertHisto2TGraph(hEWK_Purity, printValues=False)

    # Set legend labels
    if opts.doQCD:
        qcdLabel = "QCD (%s)" % GetControlRegionLabel(histoName)
        ewkLabel = "EWK (%s)" % GetControlRegionLabel(histoName)
    else:
        qcdLabel = "Fake-b (%s)"    % GetControlRegionLabel(histoName)
        ewkLabel = "Genuine-b (%s)" % GetControlRegionLabel(histoName)
        
    # Apply histo styles
    if opts.doQCD:        
        styles.qcdStyle.apply(gQCD_Purity)
        if opts.plotEWK:
            styles.altEwkStyle.apply(gEWK_Purity)
            # styles.ewkStyle.apply(gEWK_Purity)
    else:
        styles.fakeBStyle.apply(gQCD_Purity)
        if opts.plotEWK:
            styles.genuineBStyle.apply(gEWK_Purity)

    # Do the plots
    if opts.plotEWK:
        refGraph  = histograms.HistoGraph( gQCD_Purity, qcdLabel, "p", "P")
        comGraph1 = histograms.HistoGraph( gEWK_Purity, ewkLabel, "p", "P")
        p1 = plots.ComparisonManyPlot(refGraph, [comGraph1], saveFormats=[])
        # p1 = plots.PlotBase( [refGraph, comGraph1], saveFormats=[]) #also works
    else:
        refGraph  = histograms.HistoGraph( gQCD_Purity, qcdLabel, "p", "P")
        p1 = plots.PlotBase( [refGraph], saveFormats=[])

    # Also plot histograms used to calculate purity? (need custom kwargs for y-axis range)
    if 0:
        p2 = plots.ComparisonManyPlot(Data, [QCD, EWK], saveFormats=[])
 
    # Remember to remove the "rebinX" option (crashes otherwise)
    _kwargs.pop('rebinX', None)
    plots.drawPlot(p1, histoName,  **_kwargs)
    if 0:
        plots.drawPlot(p2, histoName,  **_kwargs)
    
    # Save plot in all formats
    histoName = histoName.replace("ForFakeBMeasurement/", "")
    histoName = GetSaveName(histoName) #introduced for ABCD method
    SavePlot(p1, histoName, os.path.join(opts.saveDir, "Purity", opts.optMode), saveFormats = [".png", ".pdf"] )
    if 0:
        SavePlot(p2, histoName, os.path.join(opts.saveDir, "Purity_Src", opts.optMode), saveFormats = [".png", ".pdf"] )
    return


def PlotHistoGraph(hgQCD, hgEWK, _kwargs):
    histoName = _kwargs["histoName"]

    # Make the plots
    if opts.plotEWK:
        p = plots.ComparisonManyPlot(hgQCD, [hgEWK], saveFormats=[])
    else:
        p = plots.PlotBase( [hgQCD], saveFormats=[])

    # Draw the plots
    plots.drawPlot(p, histoName,  **_kwargs)
    
    # Save plot in all formats
    histoName = histoName.replace("ForFakeBMeasurement/", "")
    histoName = GetSaveName(histoName) #introduced for ABCD method
    SavePlot(p, histoName, os.path.join(opts.saveDir, "Purity", opts.optMode), saveFormats = [".png", ".pdf"] )
    return

def GetPurityHistoGraph(datasetsMgr, folder, hName):
    '''
    Create plots with "FakeB=Data-EWKGenuineB"
    '''
    # Which folder
    genuineBFolder = folder + "EWKGenuineB"
    fakeBFolder    = folder + "EWKFakeB"
    histoName      = os.path.join(folder, hName)
    hNameGenuineB  = os.path.join(genuineBFolder, hName)
    Verbose("Creating purity plot for %s" % (histoName), True)

    # Get histogram customisations
    _kwargs  = GetHistoKwargs(histoName, opts)

    # Get histos (Data, EWK) for Inclusive
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName) )
    if opts.doQCD:
        p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, histoName) )
    else:
        p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, hNameGenuineB) )

    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Clone histograms 
    Data = p1.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    EWK  = p2.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK") # EWKGenuineB
    QCD  = p1.histoMgr.getHisto("Data").getRootHisto().Clone("QCD")

    # Rebin histograms (Before calculating Purity) # alex: FIXME - make it automatic
    if "binList" in _kwargs:
        xBins   = _kwargs["binList"]
        nx      = len(xBins)-1
        newName = "" 
        Verbose("Setting customly-selected bins %s" % (xBins), True)

        Data = Data.Rebin(nx, "", xBins)
        EWK  = EWK.Rebin(nx, "", xBins)
        QCD  = QCD.Rebin(nx, "", xBins)

    # Get QCD = Data-EWK
    QCD.Add(EWK, -1)

    # Create the Purity histos
    hQCD_Purity  = GetPurityHisto(Data, EWK, _kwargs, printValues=False, hideZeros=True)
    hEWK_Purity  = None
    if opts.plotEWK:
        hEWK_Purity  = GetPurityHisto(Data, QCD, _kwargs, printValues=False, hideZeros=True)

    # Convert Purity histos to Purity TGraphs
    gQCD_Purity = convertHisto2TGraph(hQCD_Purity, printValues=False)
    gEWK_Purity = None
    if opts.plotEWK:
        gEWK_Purity = convertHisto2TGraph(hEWK_Purity, printValues=False)

    # Set legend labels
    if opts.doQCD:
        qcdLabel = "QCD (%s)" % GetControlRegionLabel(histoName)
        ewkLabel = "EWK (%s)" % GetControlRegionLabel(histoName)
    else:
        qcdLabel = "Fake-b (%s)"    % GetControlRegionLabel(histoName)
        ewkLabel = "Genuine-b (%s)" % GetControlRegionLabel(histoName)

    # Apply random histo styles
    s = styles.getABCDStyle( GetControlRegionLabel(histoName) )
    s.apply(gQCD_Purity)        
        
    hgQCD_Purity = histograms.HistoGraph( gQCD_Purity, qcdLabel, "p", "P")
    hgEWK_Purity = None
    if gEWK_Purity:
        hgEWK_Purity = histograms.HistoGraph( gEWK_Purity, ewkLabel, "p", "P")

    # Save for future use
    _kwargs["histoName"] = histoName
    return hgQCD_Purity, hgEWK_Purity, _kwargs

def PlotHistoGraphs(hGraphList, _kwargs):

    histoName = _kwargs["histoName"]
    histoName = histoName.replace("ForFakeBMeasurement/", "")
    histoName = histoName.split("_")[1]

    # Overwrite some canvas options
    _kwargs["opts"]["ymin"] = 0.5
    _kwargs["opts"]["ymax"] = 1.02

    # Create & draw the plot    
    p = plots.PlotBase( hGraphList, saveFormats=[])
    plots.drawPlot(p, histoName, **_kwargs)

    # Save the plot
    SavePlot(p, histoName, os.path.join(opts.saveDir, "Purity", opts.optMode), saveFormats = [".png", ".pdf"] )
    return

def GetHistoKwargs(histoName, opts):
    '''
    Dictionary with
    key   = histogram name
    value = kwargs
    '''
    h = histoName.split("/")[-1]
    histoKwargs = {}
    _moveLegend = {"dx": -0.08, "dy": -0.42, "dh": -0.14}
    _yMin       = 0.0
    _yMax       = 1.09
    _cutBox     = None
    _cutBoxY    = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
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
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        # "opts"             : _opts,
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
        "moveLegend"       : _moveLegend,
        "cutBoxY"          : _cutBoxY
        }

    # Common bin settings
    myBins     = []
    ptBins     = []
    jetBins    = []
    bjetBins   = []
    btagBins   = []
    mvaBins    = []
    triMBins   = [] 
    tetraMBins = [] 
    step1      = 20
    step2      = 50
    step3      = 100
    step4      = 200
    step5      = 2000

    for i in range(0, 21, 1):
        mvaBins.append(i*0.05)

    for i in range(4, 21, 1):
        j = i*0.05
        btagBins.append(j)

    for i in range(6, 15, 1):
        jetBins.append(i)
    for i in range(0, 9, 1):
        bjetBins.append(i)

    for i in range(0, 100, 10):
        ptBins.append(i)
    for j in range(100, 200, step1):
        ptBins.append(j)
    for j in range(200, 300+step2, step2):
        ptBins.append(j)

    for j in range(0, 300, step1):
        triMBins.append(j)
    for j in range(300, 500+step2, step2):
        triMBins.append(j)

    for j in range(0, 1000, step3):
        tetraMBins.append(j)
    for k in range(1000, 2000, step4):
        tetraMBins.append(k)
    for l in range(2000, 4000+step5, step5):
        tetraMBins.append(l)

    # Set x-axis divisions
    n1 = 8 # primary divisions
    n2 = 5 # second order divisions
    n3 = 2 # third order divisions
    nDivs = n1 + 100*n2 + 10000*n3
    if 1:
        ROOT.gStyle.SetNdivisions(nDivs, "X")

    if "pt" in h.lower():# don't move further down!
        _xlabel           = "p_{T} (GeV/c)"
        myBins            = ptBins

    if "mvamax1" in h.lower():
        _xlabel = "Leading MVA"
        _cutBox = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        myBins  = mvaBins
    if "mvamax2" in h.lower():
        _xlabel = "Subleading MVA"
        _cutBox = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        myBins  = mvaBins
    if "trijetm" in h.lower():
        _units  = "GeV/c^{2}" 
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        myBins = triMBins
    if "bjet1pt" in h.lower():
        _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "p_{T} (GeV/c)"
        myBins  = ptBins
        myBins.extend([400, 600])
    if "bjet2pt" in h.lower():
        _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "p_{T} (GeV/c)"
        myBins.extend([400, 600])
    if "bjet3pt" in h.lower():
        _cutBox = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "p_{T} (GeV/c)"
    if "btagdisc" in h.lower():
        _units  = "" 
        _xlabel = "b-jet discriminator"
        # _cutBox = {"cutValue": 0.5426, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _cutBox = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        myBins  = btagBins
    if "nbjets" in h.lower():
        _units  = "" 
        _cutBox = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "b-jet multiplicity"
        myBins  = bjetBins
    if "njets" in h.lower():
        _units  = "" 
        _cutBox = {"cutValue": 7.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        _xlabel = "jet multiplicity"
        myBins  = jetBins
    if "tetrajetm" in h.lower():
        _units  = "GeV/c^{2}" 
        _xlabel = "m_{jjbb} (%s)" % (_units)
        myBins  = tetraMBins
        ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

    _kwargs["opts"]    = {"ymin": _yMin, "ymax": _yMax}
    _kwargs["xlabel"]  = _xlabel
    _kwargs["cutBox"]  = _cutBox
    _kwargs["cutBoxY"] = _cutBoxY

    if len(myBins) > 0:
        _kwargs["binList"] = array.array('d', myBins)
    return _kwargs

def GetSaveName(histoName):
    base = histoName.split("_")[0]#.lower()
    var  = histoName.split("_")[1]#.lower()
    sel  = histoName.split("_")[2]#.lower()

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
    
def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".C", ".pdf"]):
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


def convertHisto2TGraph(histo, printValues=False):

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

def GetPurityHisto(hData, hEWK, kwargs, printValues=False, hideZeros=True):

    # Prepare a new histo
    h = hData.Clone()    
    h.Reset("ICESM")
    ROOT.SetOwnership(h, True)

    # Construct info table (debugging)
    table  = []
    align  = "{:>6} {:^20} {:>10} {:>10} {:>10} {:^3} {:<10}"
    header = align.format("Bin", "Range", "EWK", "Data", "Purity", "+/-", "Error") #Purity = 1-EWK/Data
    hLine  = "="*70
    nBinsX = hData.GetNbinsX()
    table.append("{:^70}".format("Histogram"))
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # For-loop: All histogram bins
    for j in range (1, nBinsX+1):
        
        # Legeacy: No idea why the code snippet I copied used "j=j-1" instead of "i=j". 
        i = j

        # Declare variables
        myPurity       = 0.0
        myPurityUncert = 0.0
        ewkSum         = hEWK.GetBinContent(i)
        ewkSumUncert   = hEWK.GetBinError(i)
        dataSum        = hData.GetBinContent(i)
        dataSumUncert  = hData.GetBinContent(i)
        
        # Treat negative bins for EWK (possible if -ve weights are applied)
        if ewkSum < 0.0:
            Print("Sum is below 0 (Sum=%.3f +/- %.3f). Forcing value to 0.0." % (ewkSum,  ewkSumUncert), False)
            ewkSum = 0.0 

        # Ignore zero bins
        if abs(dataSum) > 0.000001:
            myPurity       = 1.0 - ewkSum / dataSum
            myPurityUncert = errorPropagation.errorPropagationForDivision(ewkSum, ewkSumUncert, dataSum, dataSumUncert)

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
            if myPurity < 1.1: # allow a generous 5% for -ve MC weights (TTbar)
                newPurity = 1.0
                newUncert = myPurityUncert
                Print("Purity exceeds 1.0 (P=%.3f +/- %.3f). Forcing value to P=%.3f +/- %.3f" % (myPurity,  myPurityUncert, newPurity, newUncert), False)
                myPurity  = newPurity                
            else:
                raise Exception("Purity cannot exceed 100%% (=%s +/- %s)" % (myPurity*100, myPurityUncert*100) )

        # Fill histogram
        h.SetBinContent(j, myPurity)
        h.SetBinError(j, myPurityUncert)

        # Save information in table
        row = align.format(j, binRange, "%.1f" % ewkSum, "%.1f" % dataSum, "%.3f" % myPurity, "+/-", "%.3f" % myPurityUncert)
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
    DOQCD        = False
    FOLDER       = "ForFakeBMeasurement" #"ForDataDrivenCtrlPlots"

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

    parser.add_option("--doQCD", dest="doQCD", action="store_true", default = DOQCD,
                      help="Plot QCD Purity instead of Fake-B purity [default: %s]" % (DOQCD))

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
        
    # Sanity check
    allowedFolders = ["ForDataDrivenCtrlPlots", "ForFakeBMeasurement"]
    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_Purity.py: Press any key to quit ROOT ...")
