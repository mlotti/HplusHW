#!/usr/bin/env python
'''
DESCRIPTION:
Plots various histograms found under the opts.folder
comparing the Control Region (CR) used in the ABCD 
FakeB background measurement. In particular, 
it creates normalised to unity histograms of CR1 and CR2.


USAGE:
./plot_Closure.py -m <pseudo_mcrab> [opts]


EXAMPLES:
./plot_Closure.py -m FakeBMeasurement_170728_040545/ -o "" --url
./plot_Closure.py -m FakeBMeasurement_170728_040545/ -o "" --url --normaliseToOne
./plot_Closure.py -m FakeBMeasurement_SRCR1VR_CSV2M_EE2_CSV2L_GE0_StdSelections_MVA_GE0p40_AllSelections_LdgTopMVA_GE0p80_SubldgMVA_GE0p80_RandomSort_180107_122559 --normaliseToOne --url


LAST USED:
./plot_Closure.py -m FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p50to085_180129_133455

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

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
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
            # PrintPSet("BJetSelection", datasetsMgr)
            # PrintPSet("TopSelectionBDT", datasetsMgr)
            # PrintPSet("FakeBMeasurement", datasetsMgr)
            sys.exit()

        # Print dataset info?
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set signal cross-section
        if 0:
            datasetsMgr.getDataset(opts.signal).setCrossSection(1.0)

        # Remove unwanted datasets
        if 0:
            datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Get Luminosity
        opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
   
        # Merge EWK samples
        datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Get all the histograms and their paths (e.g. ForFakeBMeasurement/Baseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections)
        hList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        hPaths = [os.path.join(opts.folder, h) for h in hList]

        # Create two lists of paths: one for "Baseline" (SR)  and one for "Inverted" (CR)
        path_SR  = []  # baseline, _AfterAllSelections
        path_CR1 = []  # baseline, _AfterCRSelections
        path_VR  = []  # inverted, _AfterAllSelections
        path_CR2 = []  # inverted, _AfterCRSelections
        
        # For-loop: All histogram paths
        for p in hPaths:
            if "AfterStandardSelections" in p:
                continue
            
            if "Baseline" in p:
                if "AllSelections" in p:
                    path_SR.append(p)
                if "CRSelections" in p:
                    path_CR1.append(p)
            if "Inverted" in p:
                if "AllSelections" in p:
                    path_VR.append(p)
                if "CRSelections" in p:
                    path_CR2.append(p)

        # For-loop: All histogram pairs
        for hVR, hCR2, hCR1 in zip(path_VR, path_CR2, path_CR1):
            break
            if "IsGenuineB" in hVR:
                continue
            PlotComparison(datasetsMgr, hVR, hCR2, "VRvCR2")

        # For-loop: All histogram pairs
        counter = 1
        for hCR1, hCR2 in zip(path_CR1, path_CR2):
            if "IsGenuineB" in hCR1:
                continue
            
            hName = hCR1.replace("_AfterCRSelections", "_CR1vCR2").replace("ForFakeBMeasurement/Baseline_", "")
            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (len(path_CR1)), hName)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)
            PlotComparison(datasetsMgr, hCR1, hCR2, "CR1vCR2")
            counter+=1

        # For-loop: All histogram pairs
        for hSR, hVR in zip(path_SR, path_VR):
            break
            # Print("UNBLINDING SR! Are you nuts ? BREAK!", False)
            if "IsGenuineB" in hSR:
                continue
            PlotComparison(datasetsMgr, hSR, hVR, "SRvVR")

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
    thePSet = selection + thePSet_2 + "}"

    Print(thePSet, True)
    return

def getHistos(datasetsMgr, dataset, hBaseline, hInverted):
    
    h1 = datasetsMgr.getDataset(dataset).getDatasetRootHisto(hBaseline)
    h1.setName("Baseline-" + dataset)

    h2 = datasetsMgr.getDataset(dataset).getDatasetRootHisto(hInverted)
    h2.setName("Inverted-" + dataset)
    return [h1, h2]

def PlotComparison(datasetsMgr, hBaseline, hInverted, ext):

    # Create corresponding paths for GenuineB and FakeB histograms (not only Inclusive) 
    hBaseline_Inclusive = hBaseline #no extra string 
    hInverted_Inclusive = hInverted #no extra string 
    hBaseline_GenuineB  = hBaseline_Inclusive.replace(opts.folder, opts.folder + "EWKGenuineB")
    hInverted_GenuineB  = hInverted_Inclusive.replace(opts.folder, opts.folder + "EWKGenuineB")
    hBaseline_FakeB     = hBaseline_Inclusive.replace(opts.folder, opts.folder + "EWKFakeB")
    hInverted_FakeB     = hInverted_Inclusive.replace(opts.folder, opts.folder + "EWKFakeB")

    # Create the histograms in the Baseline (SR) and Inverted (CR) regions
    pBaseline_Inclusive = plots.DataMCPlot(datasetsMgr, hBaseline_Inclusive)
    pBaseline_GenuineB  = plots.DataMCPlot(datasetsMgr, hBaseline_GenuineB )
    pBaseline_FakeB     = plots.DataMCPlot(datasetsMgr, hBaseline_FakeB    )
    pInverted_Inclusive = plots.DataMCPlot(datasetsMgr, hInverted_Inclusive)
    pInverted_GenuineB  = plots.DataMCPlot(datasetsMgr, hInverted_GenuineB )
    pInverted_FakeB     = plots.DataMCPlot(datasetsMgr, hInverted_FakeB )

    # Extract the correct SR and CR histograms
    baseline_Data        = pBaseline_Inclusive.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline-Data")
    if opts.useMC: 
        baseline_QCD     = pBaseline_Inclusive.histoMgr.getHisto("QCD").getRootHisto().Clone("Baseline-QCD")
    baseline_EWKGenuineB = pBaseline_GenuineB.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKGenuineB")
    baseline_EWKFakeB    = pBaseline_FakeB.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKFakeB")
    inverted_Data        = pInverted_Inclusive.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted-Data")
    if opts.useMC:    
        inverted_QCD     = pInverted_Inclusive.histoMgr.getHisto("QCD").getRootHisto().Clone("Inverted-QCD")
    inverted_EWKGenuineB = pInverted_GenuineB.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKGenuineB") 
    inverted_EWKFakeB    = pInverted_FakeB.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKFakeB")

    # Subtract EWKGenuineB from Data to get FakeB (= QCD_inclusive + EWK_genuineB)
    if opts.useMC: 
        # FakeB = QCD + EWKFakeB
        baseline_FakeB = baseline_QCD.Clone("Baseline-FakeB")
        inverted_FakeB = inverted_QCD.Clone("Inverted-FakeB")

        # Add the EWKFakeB
        baseline_FakeB.Add(baseline_EWKFakeB, +1)
        inverted_FakeB.Add(inverted_EWKFakeB, +1)
    else:
        # FakeB = Data -EWKGenuineB
        baseline_FakeB = baseline_Data.Clone("Baseline-FakeB")
        inverted_FakeB = inverted_Data.Clone("Inverted-FakeB")

        # Subtract the EWK GenuineB
        baseline_FakeB.Add(baseline_EWKGenuineB, -1)
        inverted_FakeB.Add(inverted_EWKGenuineB, -1)

    # Normalize histograms to unit area
    if opts.normaliseToOne:
        baseline_FakeB.Scale(1.0/baseline_FakeB.Integral())
        inverted_FakeB.Scale(1.0/inverted_FakeB.Integral())

    # Create the final plot object
    p = plots.ComparisonManyPlot(baseline_FakeB, [inverted_FakeB], saveFormats=[])
    #p = plots.ComparisonPlot(baseline_FakeB, inverted_FakeB, saveFormats=[]) #also works!
    p.setLuminosity(opts.intLumi)

    # Apply histogram styles
    p.histoMgr.forHisto("Baseline-FakeB" , styles.getABCDStyle(ext.split("v")[0]))
    p.histoMgr.forHisto("Inverted-FakeB" , styles.getABCDStyle(ext.split("v")[1]))
        
    # Set draw/legend style
    p.histoMgr.setHistoDrawStyle("Baseline-FakeB", "AP")
    p.histoMgr.setHistoDrawStyle("Inverted-FakeB", "HIST")
    p.histoMgr.setHistoLegendStyle("Baseline-FakeB", "LP")
    p.histoMgr.setHistoLegendStyle("Inverted-FakeB", "F")
        
    # Set legend labels
    if opts.useMC:
        p.histoMgr.setHistoLegendLabelMany({
                #"Baseline-FakeB" : "Fake-B (Baseline)",
                #"Inverted-FakeB" : "Fake-B (Inverted)",
                "Baseline-FakeB" : "Baseline (MC)",
                "Inverted-FakeB" : "Inverted (MC)",
         
       })
    else:
        p.histoMgr.setHistoLegendLabelMany({
                #"Baseline-FakeB" : "Baseline",
                #"Inverted-FakeB" : "Inverted",
                "Baseline-FakeB" : ext.split("v")[0],
                "Inverted-FakeB" : ext.split("v")[1],
                })

    # Get histogram keyword arguments
    kwargs_ = GetHistoKwargs(hBaseline_Inclusive, ext, opts)

    # Draw the histograms
    plots.drawPlot(p, hBaseline_Inclusive, **kwargs_)

    # Save plot in all formats    
    saveName = hBaseline_Inclusive.split("/")[-1]
    saveName = saveName.replace("Baseline_", "")
    saveName = saveName.replace("Inverted_", "")
    saveName = saveName.replace("_AfterAllSelections", "_" + ext)
    saveName = saveName.replace("_AfterCRSelections", "_" + ext)

    if opts.useMC:
        savePath = os.path.join(opts.saveDir, "MC", opts.optMode)
    else:
        savePath = os.path.join(opts.saveDir, opts.optMode)
    SavePlot(p, saveName, savePath, saveFormats = [".png", ".pdf"])
    return

def GetHistoKwargs(histoName, ext, opts):
    hName   = histoName.lower()
    _cutBox = None
    _rebinX = 1
    _ylabel = None
    _yNorm  = "Events"
    divideByBinWidth = False

    if opts.normaliseToOne:
        _yNorm  = "Arbitrary units"
        #_opts   = {"ymin": 0.7e-4, "ymaxfactor": 2.0}
        _opts   = {"ymin": 1e-6, "ymaxfactor": 2.0}
    else:
        _opts   = {"ymin": 1e0, "ymaxfactor": 2.0}
    _format = "%0.0f"
    _xlabel = None
    _ratio  = True
        
    if "dijetm" in hName:
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jj} (%s)" % (_units)
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTrijetDijetMass_AfterAllSelections"]
        _ylabel = _yNorm + " / %.0f " + _units
        #_opts["xmax"] = 200.0
        #_ylabel = "<%s / %s>" % (_yNorm, _units)
        #divideByBinWidth = True

    if "met" in hName:
        _units  = "GeV"
        _rebinX = systematics._dataDrivenCtrlPlotBinning["MET_AfterAllSelections"]  #2
        binWmin, binWmax = GetBinWidthMinMax(_rebinX)
        #_ylabel = _yNorm + " / %.0f-%.0f %s" % (binWmin, binWmax, _units)
        _ylabel = "<%s / %s>" % (_yNorm, _units)
        divideByBinWidth = True

    if "ht_" in hName:
        _units  = "GeV"
        _rebinX = systematics._dataDrivenCtrlPlotBinning["HT_AfterAllSelections"]  #2
        _cutBox       = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        binWmin, binWmax = GetBinWidthMinMax(_rebinX)
        #_ylabel = _yNorm + " / %.0f-%.0f %s" % (binWmin, binWmax, _units)
        _ylabel = "<%s / %s>" % (_yNorm, _units)
        divideByBinWidth = True

    if "mvamax1" in hName:
        _rebinX = 1
        _units  = ""
        _format = "%0.2f " + _units
        _xlabel = "top-tag discriminant"
        _opts["xmin"] =  0.0 #0.45
        _cutBox = {"cutValue": 0.40, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "mvamax2" in hName:
        _rebinX = 1
        _units  = ""
        _format = "%0.2f " + _units
        _xlabel = "top-tag discriminant"
        #_opts["xmin"] = -1.0 #0.45
        _cutBox = {"cutValue": 0.40, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "nbjets" in hName:
        _units  = ""
        _format = "%0.0f " + _units
        _cutBox = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmin"] =  2.0
        _opts["xmax"] = 10.0

    if "njets" in hName:
        _units  = ""
        _format = "%0.0f " + _units
        _rebinX = systematics._dataDrivenCtrlPlotBinning["Njets_AfterAllSelections"]

    if "btagdisc" in hName:
        _rebinX = 4
        _units  = ""
        _format = "%0.2f " + _units
        _cutBox = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "ldgdijetpt" in hName:
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _xlabel = "p_{T} (%s)" % _units
        _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTrijetDijetPt_AfterAllSelections"]
        #_opts["xmax"] = 800.0
        _ylabel = "<%s / %s>" % (_yNorm, _units)
        divideByBinWidth = True

    if "trijetm" in hName:
        # _rebinX = 2
        # _opts["xmax"] = 1000.0
        _rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTrijetMass_AfterAllSelections"]
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTrijetMass_AfterAllSelections"]
        _ylabel = "<%s / %s>" % (_yNorm, _units)
        divideByBinWidth = True
        ROOT.gStyle.SetNdivisions(8, "X")

    if "pt" in hName:
        _units  = "GeV/c"
        _rebinX = 1        
        _format = "%0.0f " + _units
        _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "jet1" in hName:
            _opts["xmax"] = 1000.0
        elif "jet2" in hName:
            _opts["xmax"] = 800.0
        elif "jet3" in hName:
            _opts["xmax"] = 600.0
        elif "jet4" in hName:
            _opts["xmax"] = 400.0
        elif "jet5" in hName:
            _opts["xmax"] = 300.0
        elif "jet6" in hName:
            _opts["xmax"] = 250.0
        elif "jet7" in hName:
            _opts["xmax"] = 200.0
        elif "tetrajet" in hName:
            _opts["xmax"] = 1000.0
            _cutBox = {"cutValue": 200.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            ROOT.gStyle.SetNdivisions(8, "X")
        elif "trijet" in hName:
            _rebinX  = systematics._dataDrivenCtrlPlotBinning["LdgTrijetPt_AfterAllSelections"]
            ROOT.gStyle.SetNdivisions(8, "X")
            _cutBox = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        else:
            _opts["xmax"] = 600.0
        _ylabel = "<%s / %s>" % (_yNorm, _units)
        divideByBinWidth = True
        ROOT.gStyle.SetNdivisions(10, "X")

    if "eta" in hName:
        _format = "%0.2f"
        _cutBox = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmin"] = -2.4
        _opts["xmax"] = +2.4
        _rebinX = 1
        #ROOT.gStyle.SetNdivisions(10, "X")

    if "deltaeta" in hName:
        _format = "%0.2f"
        _opts["xmin"] = 0.0
        _opts["xmax"] = 6.0
        if "tetrajetbjet" in hName:
            _xlabel = "#Delta#eta (b_{jjb}, b_{free})"

    if "deltaphi" in hName:
        _units  = "rads"
        _format = "%0.2f " + _units
        _opts["xmin"] = 0.0
        _opts["xmax"] = 3.2
        if "tetrajetbjet" in hName:
            _xlabel = "#Delta#phi (b_{jjb}, b_{free}) (%s)" % (_units)

    if "deltar" in hName:
        _format = "%0.2f"
        _opts["xmin"] = 0.0
        _opts["xmax"] = 6.0
        if "tetrajetbjet" in hName:
            _xlabel = "#DeltaR (b_{jjb}, b_{free})"

    if "bdisc" in hName:
        _format = "%0.2f"
        _rebinX = 2
        _opts["xmin"] = 0.0
        _opts["xmax"] = 1.0
        #_cutBox = {"cutValue": 0.5426, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _cutBox = {"cutValue": +0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "b-tag discriminant"
        if "trijet" in hName:
            #_opts["xmin"] = 0.7
            _opts["xmin"] = 0.0

    if "tetrajetm" in hName:
        _units  = "GeV/c^{2}"
        #_rebinX = systematics.getBinningForTetrajetMass(9)
        _rebinX  = systematics._dataDrivenCtrlPlotBinning["LdgTetrajetMass_AfterAllSelections"]
        binWmin, binWmax = GetBinWidthMinMax(_rebinX)
        #_ylabel = _yNorm + " / %.0f-%.0f %s" % (binWmin, binWmax, _units)
        _xlabel = "m_{jjbb} (%s)" % (_units)
        _ylabel = "<%s / %s>" % (_yNorm, _units)
        divideByBinWidth = True

    if _ylabel == None:
        _ylabel = "Arbitrary Units/ %s" % (_format)

    _kwargs = {
        "ratioCreateLegend": True,
        "ratioType"        : opts.ratioType, #"errorPropagation", "errorScale", "binomial"
        "divideByBinWidth" : divideByBinWidth,
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False}, # Include "stat.+syst." in legend? (if False just "stat.")
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.08},
        "errorBarsX"       : True,
        "xlabel"           : _xlabel,
        "ylabel"           : _ylabel,
        "rebinX"           : _rebinX, 
        "rebinY"           : None,
        "ratioYlabel"      : "Ratio ", #ext.split("v")[0] + "/" + ext.split("v")[1],
        "ratio"            : _ratio,
        "ratioInvert"      : True,  #CR1/CR2
        "addMCUncertainty" : True,
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : _opts,
        #"opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "opts2"            : {"ymin": 0.30, "ymax": 1.70},
        "log"              : True,
        "createLegend"     : {"x1": 0.80, "y1": 0.78, "x2": 0.98, "y2": 0.92},
        #"moveLegend"       : {"dx": -0.1, "dy": -0.01, "dh": 0.1},
        "cutBox"           : _cutBox,
        }
    return _kwargs
        
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

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists
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
    OPTMODE      = ""
    BATCHMODE    = True
    MERGEEWK     = True
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    NORMALISE    = True
    FOLDER       = "ForFakeBMeasurement"
    RATIOTYPE    = "errorPropagation" # "errorPropagation", "errorScale", "binomial"
    GRIDX        = False
    GRIDY        = False
    SIGNALMASS   = 500
    USEMC        = False

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

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", default=NORMALISE, 
                      help="Normalise the baseline and inverted shapes to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable x-axis grid? [default: %s]" % (GRIDX) )

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable y-axis grid? [default: %s]" % (GRIDY) )

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--ratioType", dest="ratioType", type="string", default = RATIOTYPE,
                      help="Error type for to be used for the ratio [default: %s]" % (RATIOTYPE) )

    parser.add_option("--signalMass", dest="signalMass", type=int, default=SIGNALMASS,
                      help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--useMC", dest="useMC", action="store_true", default=USEMC, 
                      help="Use QCD MC instead of QCD=Data-EWK? [default: %s]" % (USEMC) )

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
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="Closure")

    # Sanity check
    if not opts.mergeEWK:
        Print("Cannot draw the Baseline Vs Inverted histograms without the option --mergeEWK. Exit", True)
        sys.exit()

    # Sanity check
    allowedFolders = ["ForFakeBMeasurement", "ForFakeBMeasurementEWKFakeB", "ForFakeBMeasurementEWKGenuineB"]


    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()
    else:
        opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass

    ratioTypes = ["errorPropagation", "errorScale", "binomial"]
    if opts.ratioType not in ratioTypes:
        raise Exception("Invalid ration type \"%s\". Please select from:%s" % (opts.ratioType, ", ".join(ratioTypes)  ))

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_Closure.py: Press any key to quit ROOT ...")
