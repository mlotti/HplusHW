#!/usr/bin/env python
'''
Description:
This scipt plots the TH1 histograms that compare EWK with QCD shapes, 
for Baseline and Inverted analysis modes.

For the definition of the counter class see:
HiggsAnalysis/NtupleAnalysis/scripts

For more counter tricks and optios see also:
HiggsAnalysis/NtupleAnalysis/scripts/hplusPrintCounters.py

Usage:
./plotTest.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotTest.py -m FakeBMeasurement_170627_124436_BJetsGE2_TopChiSqrVar_AllSamples --mergeEWK -o "OptChiSqrCutValue100p0" -e 'Charged|QCD'
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


def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


def GetHistoKwargs(histoName):
    '''
    '''
    Verbose("Creating a map of histoName <-> kwargs")

    _opts = {}

    if "pt" in histoName.lower():
        _format = "%0.0f GeV/c"
        _rebin  = 2
        _logY   = True
        _cutBox = None
        _opts["xmax"] = 800.0
    elif "eta" in histoName.lower():
        _format = "%0.2f"
        _rebin  = 1
        _logY   = True
        _cutBox = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    elif "bdisc" in histoName.lower():
        _format = "%0.2f"
        _rebin  = 1
        _logY   = True
        _cutBox = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    elif "deta" in histoName.lower():
        _format = "%0.2f"
        _rebin  = 1
        _logY   = True
        _cutBox = None
    elif "dphi" in histoName.lower():
        _format = "%0.2f"
        _rebin  = 1
        _logY   = True
        _cutBox = None
    elif "dr" in histoName.lower():
        _format = "%0.2f"
        _rebin  = 1
        _logY   = True
        _cutBox = None
    elif "dijetmass" in histoName.lower():
        _format = "%0.0f GeV/c^{2}"
        _rebin  = 1
        _logY   = True
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    elif "tetrajetmass" in histoName.lower():
        _format = "%0.0f GeV/c^{2}"
        _rebin  = 5
        _logY   = True
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 3000.0
    elif "tetrajet2mass" in histoName.lower():
        _format = "%0.0f GeV/c^{2}"
        _rebin  = 5
        _logY   = True
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 3000.0
    elif "mass" in histoName.lower():
        _format = "%0.0f GeV/c^{2}"
        _rebin  = 1
        _logY   = False
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    elif "numberoffits" in histoName.lower():
        _format = "%0.0f"
        _rebin  = 1
        _logY   = True
        _cutBox = None
    elif "njets" in histoName.lower():
        _format = "%0.0f"
        _rebin  = 1
        _logY   = True 
        _cutBox = _cutBox = {"cutValue": 3, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    elif "chisqr" in histoName.lower():
        _format = "%0.0f"
        _rebin  = 10
        _logY   = True
        _cutBox = _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    else:
        raise Exception("The kwargs have not been prepared for the histogram with name \"%s\"." % (histoName) )

    # Customise options (main pad) for with/whitout logY scale 
    if _logY:
        _opts["ymin"] = 2e-4
        _opts["ymaxfactor"] = 5
    else:
        _opts["ymin"] = 0.0
        _opts["ymaxfactor"] = 1.2

    # Draw the histograms
    if "trijetm" in histoName.lower():
        _opts["xmax"] = 800.0

    # Define plotting options    
    kwargs = {"ylabel"      : "Arbitrary Units / %s" % (_format),
              "log"         : _logY,
              "opts"        : _opts,
              "opts2"       : {"ymin": 0.0, "ymax": 2.0},
              "rebinX"      : _rebin,
              "ratio"       : False, 
              "cutBox"      : _cutBox,
              "cmsExtraText": "Preliminary",
              "ratioYlabel" : "Ratio",
              "ratioInvert" : False, 
              "addCmsText"  : True,
              "createLegend": {"x1": 0.58, "y1": 0.80, "x2": 0.92, "y2": 0.92},
              }
    return kwargs


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
    
    optModes = ["", "OptChiSqrCutValue50p0", "OptChiSqrCutValue100p0", "OptChiSqrCutValue200p0"]
    # optModes = ["", "OptChiSqrCutValue40", "OptChiSqrCutValue60", "OptChiSqrCutValue80", "OptChiSqrCutValue100", "OptChiSqrCutValue120", "OptChiSqrCutValue140"] 
    # optModes = ["OptChiSqrCutValue250", "OptChiSqrCutValue150", "OptChiSqrCutValue200", "OptChiSqrCutValue180", "OptChiSqrCutValue300"]

    if opts.optMode != None:
        optModes = [opts.optMode]
        
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

        if 0:
            datasetsMgr.remove(filter(lambda name: "ST" in name, datasetsMgr.getAllDatasetNames()))
               
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
   
        # Get Integrated Luminosity
        if 0:
            datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))

        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"]
        newOrder.extend(GetListOfEwkDatasets())
        datasetsMgr.selectAndReorder(newOrder)

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()
        else:
            Print("Cannot draw the histograms without the option --mergeEWK. Exit", True)            
                    
        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)

        # Do the template comparisons
        #for hName in getTopSelectionHistos(opts.histoLevel, "Baseline"):
        for hName in getTopMassRecoHistos(opts.histoLevel, "Baseline", "ForFakeBMeasurement"):
            PlotTemplates(datasetsMgr, hName)
            #PlotTemplates(datasetsMgr, hName.split("/")[-1])
    return


def getTopSelectionHistos(histoLevel="Vital", analysisType="Baseline"):
    '''
    Returns the list of histograms created by
    the TopSelection class
    '''
    
    Verbose("Creating histogram list for %s" % analysisType, True)

    # Entire list
    hList = [        
        "topSelection_%s/Tetrajet1Mass_Before" % (analysisType),
        "topSelection_%s/Tetrajet1Mass_After" % (analysisType),
        "topSelection_%s/Tetrajet2Mass_Before" % (analysisType),
        "topSelection_%s/Tetrajet2Mass_After" % (analysisType),
        "topSelection_%s/LdgTetrajetMass_Before" % (analysisType),
        "topSelection_%s/LdgTetrajetMass_After" % (analysisType),
        "topSelection_%s/SubldgTetrajetMass_Before" % (analysisType),
        "topSelection_%s/SubldgTetrajetMass_After" % (analysisType),
        "topSelection_%s/Trijet2Mass_Before" % (analysisType),
        "topSelection_%s/Trijet1Mass_After" % (analysisType),
        "topSelection_%s/Trijet2Mass_After" % (analysisType),
        "topSelection_%s/Trijet1DijetMass_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetMass_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetMass_After" % (analysisType),
        "topSelection_%s/Trijet2DijetMass_After" % (analysisType),
        "topSelection_%s/LdgTrijetMass_Before" % (analysisType),
        "topSelection_%s/LdgTrijetMass_After" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetMass_Before" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetMass_After" % (analysisType),
        "topSelection_%s/SubldgTrijetMass_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetMass_After" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetMass_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetMass_After" % (analysisType),
        ]

    hListFilter = []
    if histoLevel == "Vital":
        for h in hList:
            if any(substring in h for substring in ["Pt", "BDisc", "Eta", "Dijet", "DiJet", "Fit", "Trijet1", "Trijet2", "Tetrajet1", "Tetrajet2", "ChiSqr"]):
                continue
            else:
                hListFilter.append(h)
    elif histoLevel == "Informative":
        for h in hList:
            if any(substring in h for substring in ["Pt", "BDisc", "Eta", "Dijet", "DiJet", "Fit", "Tetrajet1", "Tetrajet2"]):
                continue
            else:
                hListFilter.append(h)
    elif histoLevel == "Debug":
        hListFilter = hList
    return hListFilter


def getTopMassRecoHistos(histoLevel="Vital", analysis="Baseline", folder="ForFakeBMeasurement"):
    analyses = ["Baseline", "Inverted"]
    if analysis not in analyses:
        raise Exception("The analysis type \"%s\" is not valid. Please select one from %s" % (analysis, ", ".join(analyses) ) )

    folderList = ["ForFakeBMeasurement", "EWKFakeB", "EWKGenuineB"]
    if folder not in folderList:
        raise Exception("The folder \"%s\" is not valid. Please select one from %s" % (folder, ", ".join(folderList) ) )

    Verbose("Creating histogram list for %s" % analysis, True)

    # Entire list
    hList = [        
        "%s/%s_TopMassReco_ChiSqr_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_LdgTetrajetPt_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_LdgTetrajetMass_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_SubldgTetrajetPt_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_SubldgTetrajetMass_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_TetrajetBJetPt_AfterAllSelections" % (folder, analysis), 
        "%s/%s_TopMassReco_TetrajetBJetEta_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_LdgTrijetPt_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_LdgTrijetM_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_SubLdgTrijetPt_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_SubLdgTrijetM_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_LdgDijetPt_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_LdgDijetM_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_SubLdgDijetPt_AfterAllSelections" % (folder, analysis),
        "%s/%s_TopMassReco_SubLdgDijetM_AfterAllSelections" % (folder, analysis)
        ]

    return hList


def getHistos(datasetsMgr, datasetName, name1, name2):
    Verbose("getHistos()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(name1)
    h1.setName("Baseline" + "-" + datasetName)

    h2 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(name2)
    h2.setName("Inverted" + "-" + datasetName)
    return [h1, h2]


def getHisto(datasetsMgr, datasetName, histoName, analysisType):
    Verbose("getHisto()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-" + datasetName)
    return h1


def PlotTemplates(datasetsMgr, histoName):
    Verbose("Plotting EWK Vs QCD unity-normalised histograms")

    # FIXME - First pseudo-multicrab had the Fake/Genuine boolean REVERSED
    # FIXME - First pseudo-multicrab had the Fake/Genuine boolean REVERSED
    # FIXME - First pseudo-multicrab had the Fake/Genuine boolean REVERSED
    # FIXME - First pseudo-multicrab had the Fake/Genuine boolean REVERSED
    defaultFolder  = "ForFakeBMeasurement"
    genuineBFolder = "ForFakeBMeasurementEWKFakeB"
    fakeBFolder    = "ForFakeBMeasurementEWKGenuineB"

    # Create comparison plot
    p1 = plots.ComparisonPlot(
        getHisto(datasetsMgr, "Data", "%s" % histoName, "Baseline"),
        getHisto(datasetsMgr, "EWK" , "%s" % histoName.replace(defaultFolder, genuineBFolder), "Baseline")
        )
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    p2 = plots.ComparisonPlot(
        getHisto(datasetsMgr, "Data", "%s" % histoName, "Inverted"),
        getHisto(datasetsMgr, "EWK" , "%s" % histoName.replace(defaultFolder, genuineBFolder), "Inverted")
        )
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    p3 = plots.ComparisonPlot(
        getHisto(datasetsMgr, "Data", "%s" % histoName, "Baseline"),
        getHisto(datasetsMgr, "EWK" , "%s" % histoName.replace(defaultFolder, fakeBFolder), "Baseline")
        )
    p3.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    p4 = plots.ComparisonPlot(
        getHisto(datasetsMgr, "Data", "%s" % histoName, "Inverted"),
        getHisto(datasetsMgr, "EWK" , "%s" % histoName.replace(defaultFolder, fakeBFolder), "Inverted")
        )
    p4.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get EWK histos
    EWKGenuineB_baseline = p1.histoMgr.getHisto("Baseline-EWK").getRootHisto().Clone("Baseline-EWKGenuineB")
    EWKGenuineB_inverted = p2.histoMgr.getHisto("Inverted-EWK").getRootHisto().Clone("Inverted-EWKGenuineB")
    EWKFakeB_baseline    = p3.histoMgr.getHisto("Baseline-EWK").getRootHisto().Clone("Baseline-EWKFakeB")
    EWKFakeB_inverted    = p4.histoMgr.getHisto("Inverted-EWK").getRootHisto().Clone("Inverted-EWKFakeB")

    # Data histos
    Data_baseline = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone("Baseline-Data")
    Data_inverted = p2.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone("Inverted-Data")

    # Create FakeB (Data-EWK_GenuineB) histos
    FakeB_baseline = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone("Baseline-FakeB")
    FakeB_inverted = p2.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone("Inverted-FakeB")
    FakeB_baseline.Add(EWKGenuineB_baseline, -1)
    FakeB_inverted.Add(EWKGenuineB_inverted, -1)

    # Normalize histograms to unit area
    if 1:
        Data_baseline.Scale(1.0/Data_baseline.Integral())
        Data_inverted.Scale(1.0/Data_inverted.Integral())
        EWKGenuineB_baseline.Scale(1.0/EWKGenuineB_baseline.Integral())
        EWKGenuineB_inverted.Scale(1.0/EWKGenuineB_inverted.Integral())
        EWKFakeB_baseline.Scale(1.0/EWKFakeB_baseline.Integral())    
        EWKFakeB_inverted.Scale(1.0/EWKFakeB_inverted.Integral())
        FakeB_baseline.Scale(1.0/FakeB_baseline.Integral())
        FakeB_inverted.Scale(1.0/FakeB_inverted.Integral())

    # Create the final plot object
    compareHistos = [EWKGenuineB_baseline]
    # compareHistos = [EWKGenuineB_baseline, EWKGenuineB_inverted, EWKFakeB_inverted, Data_inverted]
    # compareHistos = [EWKGenuineB_inverted, EWKFakeB_inverted, Data_inverted]
    # compareHistos = [EWKGenuineB_baseline, EWKFakeB_baseline, EWKGenuineB_inverted, EWKFakeB_inverted]
    # compareHistos = [FakeB_baseline, EWKGenuineB_baseline, EWKFakeB_baseline, EWKGenuineB_inverted, EWKFakeB_inverted]
    p = plots.ComparisonManyPlot(FakeB_inverted, compareHistos, saveFormats=[])
    p.setLuminosity(GetLumi(datasetsMgr))
        
    # Apply styles
    p.histoMgr.forHisto("Inverted-FakeB"      , styles.getInvertedLineStyle() )
    p.histoMgr.forHisto("Baseline-EWKGenuineB", styles.getBaselineLineStyle() )
    if 0:
        p.histoMgr.forHisto("Baseline-FakeB"      , styles.getInvertedLineStyle() )
        p.histoMgr.forHisto("Baseline-EWKFakeB"   , styles.getFakeBStyle() )
        p.histoMgr.forHisto("Inverted-EWKGenuineB", styles.getGenuineBStyle() )
        p.histoMgr.forHisto("Inverted-EWKFakeB"   , styles.getFakeBLineStyle() )
        p.histoMgr.forHisto("Inverted-Data"       , styles.getDataStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("Inverted-FakeB"      , "HIST")
    p.histoMgr.setHistoDrawStyle("Baseline-EWKGenuineB", "HIST")
    if 0:
        p.histoMgr.setHistoDrawStyle("Baseline-FakeB"      , "AP")
        p.histoMgr.setHistoDrawStyle("Baseline-EWKFakeB"   , "HIST")
        p.histoMgr.setHistoDrawStyle("Inverted-EWKGenuineB", "AP")
        p.histoMgr.setHistoDrawStyle("Inverted-EWKFakeB"   , "HIST")
        p.histoMgr.setHistoDrawStyle("Inverted-Data"       , "AP")
        
    # Set legend style
    p.histoMgr.setHistoLegendStyle("Inverted-FakeB"      , "L")
    p.histoMgr.setHistoLegendStyle("Baseline-EWKGenuineB", "L")
    if 0:
        p.histoMgr.setHistoLegendStyle("Baseline-FakeB"      , "P")
        p.histoMgr.setHistoLegendStyle("Baseline-EWKFakeB"   , "FL")
        p.histoMgr.setHistoLegendStyle("Inverted-EWKGenuineB", "P")
        p.histoMgr.setHistoLegendStyle("Inverted-EWKFakeB"   , "L")
        p.histoMgr.setHistoLegendStyle("Inverted-Data"       , "LP")
        
    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            "Inverted-FakeB"      : "FakeB (Inverted)",# (I)",
            #"Inverted-Data"       : "Data (I)",
            "Baseline-EWKGenuineB": "EWK (Baseline)",#-GenuineB (B)",
            #"Baseline-FakeB"      : "FakeB",
            #"Baseline-EWKFakeB"   : "EWK-FakeB (B)",
            #"Inverted-EWKGenuineB": "EWK-GenuineB (I)",
            #"Inverted-EWKFakeB"   : "EWK-FakeB (I)",
            })

    # Append analysisType to histogram name
    saveName = histoName

    # Draw the histograms #alex
    plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 

    # Add text
    text = opts.optMode.replace("OptChiSqrCutValue", "#chi^{2} #leq ")
    histograms.addText(0.21, 0.85, text)

    # Save plot in all formats
    saveDir = os.path.join(opts.saveDir, "Test", opts.optMode)
    SavePlot(p, saveName, saveDir, saveFormats = [".png"])
    return


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
    OPTMODE      = None
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MCONLY       = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'

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

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

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
        raw_input("=== plotHistograms.py: Press any key to quit ROOT ...")
