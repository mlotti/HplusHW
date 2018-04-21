#!/usr/bin/env python
'''
DESCRIPTION:
Try to prove that there is not systematics associated with the
definition of the Control Region (CR). In the FakeB measurement
we define the CR2 and VR by inverting both the b-jet selection
and the 2nd top BDT. 

Here i need to show that moving the BDT of the second top to smaller
values than the maximum allowable one (default) does not change
the closure tests.


USAGE:
./plot_ClosurePerturbation.py -m <pseudo_mcrab1> -n <pseudo_mcrab2> -l <pseudo_mcrab3> [opts]


EXAMPLES:
./plot_ClosurePerturbation.py -m FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p40_6BinsAbsEta_0PtBins_NoFatjetVeto_180326_062820 -n FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p38_6BinsAbsEta_0PtBins_NoFatjetVeto_180328_142550 -l FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p36_6BinsAbsEta_0PtBins_NoFatjetVeto_180328_142751
./plot_ClosurePerturbation.py -m FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p40_6BinsAbsEta_0PtBins_NoFatjetVeto_180326_062820 -n FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p36_6BinsAbsEta_0PtBins_NoFatjetVeto_180328_142751 -l FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p34_6BinsAbsEta_0PtBins_NoFatjetVeto_180328_142923/

LAST USED:
./plot_ClosurePerturbation.py -m FakeBMeasurement_Preapproval_MVAm1p00to0p40_6AbsEtaBins_0PtBins_NoFatjetVeto_Systematics_12Apr2018 -n FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p30_6BinsAbsEta_0PtBins_NoFatjetVeto_180331_001547 -l FakeBMeasurement_PreSel_3CSVv2M_b3Pt40_InvSel_3CSVv2L_2CSVv2M_MVAm1p00to0p20_6BinsAbsEta_0PtBins_NoFatjetVeto_180331_001221 --logY

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

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

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

def GetDatasetsFromDir(mcrab, opts):
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
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
    style.setGridX(False)
    style.setGridY(False)

    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab1)
    
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

        # Get the datasets from the directory
        datasetsMgr1 = GetDatasetsFromDir(opts.mcrab1, opts)
        datasetsMgr2 = GetDatasetsFromDir(opts.mcrab2, opts)
        datasetsMgr3 = GetDatasetsFromDir(opts.mcrab3, opts)
        
        # Setup the dataset managers
        datasetsMgr1.updateNAllEventsToPUWeighted()
        datasetsMgr1.loadLuminosities() # from lumi.json
        datasetsMgr2.updateNAllEventsToPUWeighted()
        datasetsMgr2.loadLuminosities() # from lumi.json
        datasetsMgr3.updateNAllEventsToPUWeighted()
        datasetsMgr3.loadLuminosities() # from lumi.json

        # Print dataset info?
        if opts.verbose:

            datasetsMgr1.PrintCrossSections()
            datasetsMgr1.PrintLuminosities()

            datasetsMgr2.PrintCrossSections()
            datasetsMgr2.PrintLuminosities()

            datasetsMgr2.PrintCrossSections()
            datasetsMgr2.PrintLuminosities()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr1) 
        plots.mergeRenameReorderForDataMC(datasetsMgr2) 
        plots.mergeRenameReorderForDataMC(datasetsMgr3) 
        
        # Get Luminosity
        lumi1 = datasetsMgr1.getDataset("Data").getLuminosity()
        lumi2 = datasetsMgr2.getDataset("Data").getLuminosity()
        lumi3 = datasetsMgr3.getDataset("Data").getLuminosity()
        if lumi1 != lumi2 != lumi3:
            raise Exception("Lumi1 (=%.2f) != Lumi2 (=%.2f) != Lumi3 (=%.2f" % (lumi1, lumi2, lumi3))
        else:
            opts.intLumi = datasetsMgr1.getDataset("Data").getLuminosity()
   
        # Merge EWK samples
        datasetsMgr1.merge("EWK", aux.GetListOfEwkDatasets())
        datasetsMgr2.merge("EWK", aux.GetListOfEwkDatasets())
        datasetsMgr3.merge("EWK", aux.GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr1.PrintInfo()
        if 0:
            datasetsMgr2.PrintInfo()
            datasetsMgr3.PrintInfo()

        # Get all the histograms and their paths (e.g. ForFakeBMeasurement/Baseline_DeltaRLdgTrijetBJetTetrajetBJet_AfterCRSelections)
        hList  = datasetsMgr1.getDataset(datasetsMgr1.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        hPaths = [os.path.join(opts.folder, h) for h in hList]

        # Create a smaller list with only histos of interest
        hListS = []
        for h in hList:
            if "StandardSelections" in h:
                continue
            if "IsGenuineB" in h:
                continue
            if "_Bjet" in h:
                continue
            if "_Jet" in h:
                continue
            if "_SubLdg" in h:
                continue
            if "_Njets" in h:
                continue
            if "_NBjets" in h:
                continue
            if "_Delta" in h:
                continue
            if "Dijet" in h:
                continue
            if "Bdisc" in h:
                continue
            #if "MVA" in h:
            #    continue
            if "MET" in h:
                continue
            if "HT" in h:
                continue
            # Otherwise keep the histogram
            hListS.append(h)

        hPathsS = [os.path.join(opts.folder, h) for h in hListS]
        
        # Create two lists of paths: one for "Baseline" (SR)  and one for "Inverted" (CR)
        path_SR  = []  # baseline, _AfterAllSelections
        path_CR1 = []  # baseline, _AfterCRSelections
        path_VR  = []  # inverted, _AfterAllSelections
        path_CR2 = []  # inverted, _AfterCRSelections

        # For-loop: All histogram paths
        for p in hPathsS: #hPaths:
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

        counter = 1
        # For-loop: All histogram pairs
        for hCR1, hCR2 in zip(path_CR1, path_CR2):
            if "IsGenuineB" in hCR1:
                continue
            #hName = hCR1.replace("_AfterCRSelections", "_CR1vCR2").replace("ForFakeBMeasurement/Baseline_", "")
            hName = hCR1.replace("_AfterCRSelections", " (CR1 and R2)").replace("ForFakeBMeasurement/Baseline_", "")
            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (len(path_CR1)), hName)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)

            PlotComparison(datasetsMgr1, datasetsMgr2, datasetsMgr3, hCR1, hCR2, "CR1")
            PlotComparison(datasetsMgr1, datasetsMgr2, datasetsMgr3, hCR1, hCR2, "CR2") #iro
            counter+=1

        
        # WARNING! This unblinds the Signal Region (SR)        
        for hSR, hVR in zip(path_SR, path_VR):
            if "IsGenuineB" in hSR:
                continue
            if 1:
                continue
            #hName = hCR1.replace("_AfterCRSelections", "_SRvVR").replace("ForFakeBMeasurement/Baseline_", "")
            hName = hCR1.replace("_AfterCRSelections", " (SR and VR)").replace("ForFakeBMeasurement/Baseline_", "")
            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % counter, "/", "%s:" % (len(path_CR1)), hName)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), counter==1)

            PlotComparison(datasetsMgr1, datasetsMgr2, datasetsMgr3, hSR, hVR, "SR")
            PlotComparison(datasetsMgr1, datasetsMgr2, datasetsMgr3, hSR, hVR, "VR")
            counter+=1

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

def PlotComparison(datasetsMgr1, datasetsMgr2, datasetsMgr3, hBaseline, hInverted, ext):

    # Create corresponding paths for GenuineB and FakeB histograms (not only Inclusive) 
    hBaseline_Inclusive = hBaseline #no extra string 
    hInverted_Inclusive = hInverted #no extra string 
    hBaseline_GenuineB  = hBaseline_Inclusive.replace(opts.folder, opts.folder + "EWKGenuineB")
    hInverted_GenuineB  = hInverted_Inclusive.replace(opts.folder, opts.folder + "EWKGenuineB")
    hBaseline_FakeB     = hBaseline_Inclusive.replace(opts.folder, opts.folder + "EWKFakeB")
    hInverted_FakeB     = hInverted_Inclusive.replace(opts.folder, opts.folder + "EWKFakeB")

    # Create the histograms in the Baseline (SR) and Inverted (CR) regions
    pBaseline_Inclusive1 = plots.DataMCPlot(datasetsMgr1, hBaseline_Inclusive)
    pBaseline_GenuineB1  = plots.DataMCPlot(datasetsMgr1, hBaseline_GenuineB )
    pBaseline_FakeB1     = plots.DataMCPlot(datasetsMgr1, hBaseline_FakeB    )
    pInverted_Inclusive1 = plots.DataMCPlot(datasetsMgr1, hInverted_Inclusive)
    pInverted_GenuineB1  = plots.DataMCPlot(datasetsMgr1, hInverted_GenuineB )
    pInverted_FakeB1     = plots.DataMCPlot(datasetsMgr1, hInverted_FakeB )

    pBaseline_Inclusive2 = plots.DataMCPlot(datasetsMgr2, hBaseline_Inclusive)
    pBaseline_GenuineB2  = plots.DataMCPlot(datasetsMgr2, hBaseline_GenuineB )
    pBaseline_FakeB2     = plots.DataMCPlot(datasetsMgr2, hBaseline_FakeB    )
    pInverted_Inclusive2 = plots.DataMCPlot(datasetsMgr2, hInverted_Inclusive)
    pInverted_GenuineB2  = plots.DataMCPlot(datasetsMgr2, hInverted_GenuineB )
    pInverted_FakeB2     = plots.DataMCPlot(datasetsMgr2, hInverted_FakeB )

    pBaseline_Inclusive3 = plots.DataMCPlot(datasetsMgr3, hBaseline_Inclusive)
    pBaseline_GenuineB3  = plots.DataMCPlot(datasetsMgr3, hBaseline_GenuineB )
    pBaseline_FakeB3     = plots.DataMCPlot(datasetsMgr3, hBaseline_FakeB    )
    pInverted_Inclusive3 = plots.DataMCPlot(datasetsMgr3, hInverted_Inclusive)
    pInverted_GenuineB3  = plots.DataMCPlot(datasetsMgr3, hInverted_GenuineB )
    pInverted_FakeB3     = plots.DataMCPlot(datasetsMgr3, hInverted_FakeB )

    # Extract the correct SR and CR histograms
    baseline_Data1        = pBaseline_Inclusive1.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline-Data1")
    baseline_EWKGenuineB1 = pBaseline_GenuineB1.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKGenuineB1")
    baseline_EWKFakeB1    = pBaseline_FakeB1.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKFakeB1")
    inverted_Data1        = pInverted_Inclusive1.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted-Data1")
    inverted_EWKGenuineB1 = pInverted_GenuineB1.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKGenuineB1") 
    inverted_EWKFakeB1    = pInverted_FakeB1.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKFakeB1")

    baseline_Data2        = pBaseline_Inclusive2.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline-Data2")
    baseline_EWKGenuineB2 = pBaseline_GenuineB2.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKGenuineB2")
    baseline_EWKFakeB2    = pBaseline_FakeB2.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKFakeB2")
    inverted_Data2        = pInverted_Inclusive2.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted-Data2")
    inverted_EWKGenuineB2 = pInverted_GenuineB2.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKGenuineB2") 
    inverted_EWKFakeB2    = pInverted_FakeB2.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKFakeB2")

    baseline_Data3        = pBaseline_Inclusive3.histoMgr.getHisto("Data").getRootHisto().Clone("Baseline-Data3")
    baseline_EWKGenuineB3 = pBaseline_GenuineB3.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKGenuineB3")
    baseline_EWKFakeB3    = pBaseline_FakeB3.histoMgr.getHisto("EWK").getRootHisto().Clone("Baseline-EWKFakeB3")
    inverted_Data3        = pInverted_Inclusive3.histoMgr.getHisto("Data").getRootHisto().Clone("Inverted-Data3")
    inverted_EWKGenuineB3 = pInverted_GenuineB3.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKGenuineB3") 
    inverted_EWKFakeB3    = pInverted_FakeB3.histoMgr.getHisto("EWK").getRootHisto().Clone("Inverted-EWKFakeB3")

    # FakeB = Data -EWKGenuineB
    baseline_FakeB1 = baseline_Data1.Clone("Baseline-FakeB1")
    inverted_FakeB1 = inverted_Data1.Clone("Inverted-FakeB1")

    baseline_FakeB2 = baseline_Data2.Clone("Baseline-FakeB2")
    inverted_FakeB2 = inverted_Data2.Clone("Inverted-FakeB2")

    baseline_FakeB3 = baseline_Data3.Clone("Baseline-FakeB3")
    inverted_FakeB3 = inverted_Data3.Clone("Inverted-FakeB3")


    # Subtract the EWK GenuineB
    baseline_FakeB1.Add(baseline_EWKGenuineB1, -1)
    inverted_FakeB1.Add(inverted_EWKGenuineB1, -1)

    baseline_FakeB2.Add(baseline_EWKGenuineB2, -1)
    inverted_FakeB2.Add(inverted_EWKGenuineB2, -1)

    baseline_FakeB3.Add(baseline_EWKGenuineB3, -1)
    inverted_FakeB3.Add(inverted_EWKGenuineB3, -1)

    # Normalize histograms to unit area
    if opts.normaliseToOne:
        baseline_FakeB1.Scale(1.0/baseline_FakeB1.Integral())
        inverted_FakeB1.Scale(1.0/inverted_FakeB1.Integral())

        baseline_FakeB2.Scale(1.0/baseline_FakeB2.Integral())
        inverted_FakeB2.Scale(1.0/inverted_FakeB2.Integral())

        baseline_FakeB3.Scale(1.0/baseline_FakeB3.Integral())
        inverted_FakeB3.Scale(1.0/inverted_FakeB3.Integral())

    # Create the final plot object
    if ext == "CR1" or ext == "SR":
        p = plots.ComparisonManyPlot(baseline_FakeB1, [baseline_FakeB2, baseline_FakeB3], saveFormats=[])
    elif ext == "CR2" or ext == "VR":
        p = plots.ComparisonManyPlot(inverted_FakeB1, [inverted_FakeB2, inverted_FakeB3], saveFormats=[])
    else:
        raise Exception("Unexpected extension %s" % (ext))
    p.setLuminosity(opts.intLumi)

    # Get the BDT cut values from the multicrab name
    BDT1 = find_between(opts.mcrab1, "MVAm1p00to", "_").replace("p", ".")
    BDT2 = find_between(opts.mcrab2, "MVAm1p00to", "_").replace("p", ".")
    BDT3 = find_between(opts.mcrab3, "MVAm1p00to", "_").replace("p", ".")

    # Apply histogram styles
    if ext == "CR1" or ext == "SR":
        p.histoMgr.forHisto("Baseline-FakeB1" , styles.getFakeBLineStyle()) # getABCDStyle("SR") , getABCDStyle("VR")
        p.histoMgr.forHisto("Baseline-FakeB2" , styles.genuineBAltStyle) 
        p.histoMgr.forHisto("Baseline-FakeB3" , styles.getABCDStyle("SR") )

        # Set drawing style
        p.histoMgr.setHistoDrawStyle("Baseline-FakeB1"  , "HIST")
        p.histoMgr.setHistoDrawStyle("Baseline-FakeB2"  , "AP")
        p.histoMgr.setHistoDrawStyle("Baseline-FakeB3"  , "AP")

        # Set legend styles
        p.histoMgr.setHistoLegendStyle("Baseline-FakeB1", "L")
        p.histoMgr.setHistoLegendStyle("Baseline-FakeB2", "LP")
        p.histoMgr.setHistoLegendStyle("Baseline-FakeB3", "LP")

        # Set legend labels
        p.histoMgr.setHistoLegendLabelMany({
                "Baseline-FakeB1" : "%s (BDT < %s)" % (ext, BDT1),
                "Baseline-FakeB2" : "%s (BDT < %s)" % (ext, BDT2),
                "Baseline-FakeB3" : "%s (BDT < %s)" % (ext, BDT3),
                })        
    else:
        p.histoMgr.forHisto("Inverted-FakeB1" , styles.getFakeBLineStyle())
        p.histoMgr.forHisto("Inverted-FakeB2" , styles.genuineBAltStyle)
        p.histoMgr.forHisto("Inverted-FakeB3" , styles.getABCDStyle("SR") )
        # Set drawing styles
        p.histoMgr.setHistoDrawStyle("Inverted-FakeB1"  , "HIST")
        p.histoMgr.setHistoDrawStyle("Inverted-FakeB2"  , "AP")
        p.histoMgr.setHistoDrawStyle("Inverted-FakeB3"  , "AP")
        
        # Set legend styles
        p.histoMgr.setHistoLegendStyle("Inverted-FakeB1", "L")
        p.histoMgr.setHistoLegendStyle("Inverted-FakeB2", "LP")
        p.histoMgr.setHistoLegendStyle("Inverted-FakeB3", "LP")
        # Set legend labels
        p.histoMgr.setHistoLegendLabelMany({
                "Inverted-FakeB1" : "%s (BDT < %s)" % (ext, BDT1),
                "Inverted-FakeB2" : "%s (BDT < %s)" % (ext, BDT2),
                "Inverted-FakeB3" : "%s (BDT < %s)" % (ext, BDT3),
            })


    # Get histogram keyword arguments
    kwargs_ = GetHistoKwargs(hBaseline_Inclusive, ext, opts)

    # Draw the histograms
    plots.drawPlot(p, hBaseline_Inclusive, **kwargs_) #iro
    
    # Save plot in all formats    
    saveName = hBaseline_Inclusive.split("/")[-1]
    saveName = saveName.replace("Baseline_", "")
    saveName = saveName.replace("Inverted_", "")
    saveName = saveName.replace("_AfterAllSelections", "_" + ext)
    saveName = saveName.replace("_AfterCRSelections", "_" + ext)
    savePath = os.path.join(opts.saveDir, opts.optMode)
    SavePlot(p, saveName, savePath, saveFormats = [".png", ".pdf"])
    return

def GetHistoKwargs(histoName, ext, opts):
    hName   = histoName.lower()
    _cutBox = None
    _rebinX = 1
    _ylabel = None
    _yNorm  = "Events"
    _logY   = opts.logY
    if _logY:
        maxFactorY = 4.0
    else:
        maxFactorY = 1.2
    if opts.normaliseToOne:
        _yNorm  = "Arbitrary units"
        _opts   = {"ymin": 0.7e-4, "ymaxfactor": maxFactorY}
    else:
        _opts   = {"ymin": 1e0, "ymaxfactor": maxFactorY}
    _format = "%0.0f"
    _xlabel = None
    _ratio  = True

    if "dijetm" in hName:
        _rebinX = 2
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jj} (%s)" % (_units)
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmax"] = 200.0

    if "met" in hName:
        _units  = "GeV"
        _rebinX = systematics._dataDrivenCtrlPlotBinning["MET_AfterAllSelections"]  #2
        _opts["xmax"] = 300.0
        binWmin, binWmax = GetBinWidthMinMax(_rebinX)
        _ylabel = _yNorm + " / %.0f-%.0f %s" % (binWmin, binWmax, _units)

    if "ht_" in hName:
        _units  = "GeV"
        #_rebinX = 5 #2
        _rebinX = systematics._dataDrivenCtrlPlotBinning["HT_AfterAllSelections"]  #2
        _opts["xmin"] =  400.0
        _opts["xmax"] = 3000.0
        _cutBox       = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        binWmin, binWmax = GetBinWidthMinMax(_rebinX)
        _ylabel = _yNorm + " / %.0f-%.0f %s" % (binWmin, binWmax, _units)

    if "mvamax1" in hName:
        _rebinX = 1
        _units  = ""
        _format = "%0.2f " + _units
        _xlabel = "top-tag discriminant"
        _opts["xmin"] =  0.4 #0.45
        _cutBox = {"cutValue": 0.40, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    if "mvamax2" in hName:
        _rebinX = 1
        _units  = ""
        _format = "%0.2f " + _units
        _xlabel = "top-tag discriminant"
        #_opts["xmin"] = -1.0 #0.45
        _cutBox = {"cutValue": 0.40, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    if "nbjets" in hName:
        _units  = ""
        _format = "%0.0f " + _units
        _cutBox = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmin"] =  2.0
        _opts["xmax"] = 10.0

    if "njets" in hName:
        _units  = ""
        _format = "%0.0f " + _units
        #_cutBox = {"cutValue": 7.0, "fillColor": 16, "box": True, "line": False, "greaterThan": True}
        _opts["xmin"] = 7.0
        _opts["xmax"] = 20.0

    if "btagdisc" in hName:
        _rebinX = 2
        _units  = ""
        _format = "%0.2f " + _units
        _cutBox = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": False, "greaterThan": True}

    if "ldgdijetpt" in hName:
        _rebinX = 1
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _xlabel = "p_{T} (%s)" % _units
        _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmax"] = 800.0

    if "ldgdijetm" in hName:
        _rebinX = 1
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jj} (%s)" % _units
        _cutBox = {"cutValue": 80.385, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmax"] = 200.0

    if "trijetm" in hName:
        _rebinX = 2
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmax"] = 500.0 # 300

    if "eta" in hName:
        _rebinX = 2 
        _units  = ""
        _format = "%0.2f " + _units
        _cutBox = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmin"] = -2.5
        _opts["xmax"] = +2.5

    if "pt" in hName:
        _rebinX = 2 
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
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
            _cutBox = {"cutValue": 200.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            #_rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTetrajetPt_AfterAllSelections"]
            _rebinX = 5
            #_rebinX = 10
            _opts["xmax"] = 800.0
            if isinstance(_rebinX, list):
                binWmin, binWmax = GetBinWidthMinMax(_rebinX)
                _ylabel = _yNorm + " / %.0f-%.0f %s" % (binWmin, binWmax, _units)
            else:
                _ylabel = _yNorm + " / %.0f " + _units
        
            ROOT.gStyle.SetNdivisions(8, "X")
        elif "dijet" in hName:
            _cutBox = {"cutValue": 200.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        elif "trijet" in hName:
            _rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTrijetPt_AfterAllSelections"]
            _rebinX = [i for i in range(0, 600+50, 50)]
        else:
            _opts["xmax"] = 600.0
        #ROOT.gStyle.SetNdivisions(8, "X")

    if "bdisc" in hName:
        _format = "%0.2f"
        _rebinX = 1 #2
        _opts["xmin"] = 0.0
        _opts["xmax"] = 1.0
        _cutBox = {"cutValue": +0.8484, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _xlabel = "b-tag discriminant"
        if "trijet" in hName:
            _opts["xmin"] = 0.7

    if "trijetmass" in hName:
        _rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTrijetMass_AfterAllSelections"]
        _opts["xmax"] = 350.0
    if "tetrajetm" in hName:
        _units  = "GeV/c^{2}"
        #_rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTetrajetMass_AfterAllSelections"]
        #_rebinX = systematics.getBinningForTetrajetMass(0)
        #_rebinX = systematics.getBinningForTetrajetMass(9)
        #_rebinX = 5
        _rebinX = 10
        _opts["xmax"] = 3000.0
        if isinstance(_rebinX, list):
            binWmin, binWmax = GetBinWidthMinMax(_rebinX)
            _ylabel = _yNorm + " / %.0f-%.0f %s" % (binWmin, binWmax, _units)
        else:
            _ylabel = _yNorm + " / %.0f " + _units
        _xlabel = "m_{jjbb} (%s)" % (_units)
        ROOT.gStyle.SetNdivisions(6, "X")

    if _ylabel == None:
        _ylabel = "Arbitrary Units/ %s" % (_format)

    _kwargs = {
        "ratioCreateLegend": True,
        "ratioType"        : "errorScale", # None, "errorScale", "binomial", "errorPropagation"
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False}, # Include stat.+syst. to numerator (if syst globally enabled)
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.05},
        "errorBarsX"       : True,
        "xlabel"           : _xlabel,
        "ylabel"           : _ylabel,
        "rebinX"           : _rebinX, 
        "rebinY"           : None,
        "ratioYlabel"      : "Ratio ", #space intentional
        "ratio"            : _ratio,
        "ratioInvert"      : True, 
        "addMCUncertainty" : True,
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : _opts,
        "opts2"            : {"ymin": 0.30, "ymax": 1.70},
        #"opts2"            : {"ymin": 0.6, "ymax": 2.0-0.6},
        #"opts2"            : {"ymin": 0.80, "ymax": 2.0-0.80},
        "log"              : _logY,
        "createLegend"     : {"x1": 0.58, "y1": 0.78, "x2": 0.98, "y2": 0.92},
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
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    NORMALISE    = True
    SIGNALMASS   = 500
    FOLDER       = "ForFakeBMeasurement"
    LOGY         = False

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab1", dest="mcrab1", action="store", 
                      help="Path to the multicrab directory (1) for input")

    parser.add_option("-n", "--mcrab2", dest="mcrab2", action="store", 
                      help="Path to the multicrab directory (2) for input")

    parser.add_option("-l", "--mcrab3", dest="mcrab3", action="store", 
                      help="Path to the multicrab directory (3) for input")

    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY, 
                      help="Set y-axis to logarithmic scalen [default: %s]" % LOGY)

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

    parser.add_option("--normaliseToOne", dest="normaliseToOne", action="store_true", default=NORMALISE, 
                      help="Normalise the baseline and inverted shapes to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--signalMass", dest="signalMass", type=int, default=SIGNALMASS,
                      help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab1 == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)

    if opts.mcrab2 == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)

    if opts.mcrab3 == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab1, prefix="", postfix="ClosurePerturbation")

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 650, 800, 1000, 2000, 3000]

    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()
    else:
        opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_test.py: Press any key to quit ROOT ...")
