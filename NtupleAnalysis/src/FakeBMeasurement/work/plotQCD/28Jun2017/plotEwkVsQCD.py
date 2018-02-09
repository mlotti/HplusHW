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
./plotEwkVsQCD.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotEwkVsQCD.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/FakeBMeasurement_170602_235941_BJetsEE2_TopChiSqrVar_H2Var --mergeEWK --histoLevel Vital
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
    if "trijetmass" in histoName.lower(): #alex
        _opts["xmax"] = 800.0

    # Define plotting options    
    kwargs = {"ylabel": "Arbitrary Units / %s" % (_format),
              "log"   : _logY,
              "opts"  : _opts,
              "opts2" : {"ymin": 0.0, "ymax": 2.0},
              "rebinX": _rebin,
              "ratio" : True, 
              "cutBox": _cutBox,
              "cmsExtraText": "Preliminary",
              "ratioYlabel" : "Ratio",
              "ratioInvert" : False, 
              "addCmsText"  : True,
              "createLegend": {"x1": 0.62, "y1": 0.78, "x2": 0.92, "y2": 0.92},
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

    optModes = ["", "OptChiSqrCutValue40", "OptChiSqrCutValue60", "OptChiSqrCutValue80", "OptChiSqrCutValue100", "OptChiSqrCutValue120", "OptChiSqrCutValue140"] 

    if opts.optMode != None:
        optModes = [opts.Mode]

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
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
   
        if 0:
            datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))

        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"] #, "TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
        newOrder.extend(GetListOfEwkDatasets())
        # newOrder.extend("M_500")
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
            Print("Cannot draw the EWKvQCD histograms without the option --mergeEWK. Exit", True)
            sys.exit()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)

        # Do the template comparisons
        analysisTypes = ["Baseline", "Inverted"]
        for analysis in analysisTypes:
            for hName in getTopSelectionHistos(opts.histoLevel, analysis):
                if "ldgtrijetmass_after" not in hName.lower():
                    continue
                EWKvQCD(datasetsMgr, hName.split("/")[-1], analysis)
    return


def getTopSelectionHistos(histoLevel="Vital", analysisType="Baseline"):
    '''
    Returns the list of histograms created by
    the TopSelection class
    '''
    
    Verbose("Creating histogram list for %s" % analysisType, True)

    # Entire list
    hList = [        
        "topSelection_%s/ChiSqr_Before" % (analysisType),
        "topSelection_%s/ChiSqr_After" % (analysisType),
        "topSelection_%s/NJetsUsedAsBJetsInFit_Before" % (analysisType),
        "topSelection_%s/NJetsUsedAsBJetsInFit_After" % (analysisType),
        "topSelection_%s/NumberOfFits_Before" % (analysisType),
        "topSelection_%s/NumberOfFits_After" % (analysisType),
        "topSelection_%s/TetrajetBJetPt_Before" % (analysisType),
        "topSelection_%s/TetrajetBJetPt_After" % (analysisType),
        "topSelection_%s/TetrajetBJetEta_Before" % (analysisType),
        "topSelection_%s/TetrajetBJetEta_After" % (analysisType),
        "topSelection_%s/TetrajetBJetBDisc_Before" % (analysisType),
        "topSelection_%s/TetrajetBJetBDisc_After" % (analysisType),
        "topSelection_%s/Tetrajet1Pt_Before" % (analysisType),
        "topSelection_%s/Tetrajet1Mass_Before" % (analysisType),
        "topSelection_%s/Tetrajet1Eta_Before" % (analysisType),
        "topSelection_%s/Tetrajet1Pt_After" % (analysisType),
        "topSelection_%s/Tetrajet1Mass_After" % (analysisType),
        "topSelection_%s/Tetrajet1Eta_After" % (analysisType),
        "topSelection_%s/Tetrajet2Pt_Before" % (analysisType),
        "topSelection_%s/Tetrajet2Mass_Before" % (analysisType),
        "topSelection_%s/Tetrajet2Eta_Before" % (analysisType),
        "topSelection_%s/Tetrajet2Pt_After" % (analysisType),
        "topSelection_%s/Tetrajet2Mass_After" % (analysisType),
        "topSelection_%s/Tetrajet2Eta_After" % (analysisType),
        "topSelection_%s/LdgTetrajetPt_Before" % (analysisType),
        "topSelection_%s/LdgTetrajetMass_Before" % (analysisType),
        "topSelection_%s/LdgTetrajetEta_Before" % (analysisType),
        "topSelection_%s/LdgTetrajetPt_After" % (analysisType),
        "topSelection_%s/LdgTetrajetMass_After" % (analysisType),
        "topSelection_%s/LdgTetrajetEta_After" % (analysisType),
        "topSelection_%s/SubldgTetrajetPt_Before" % (analysisType),
        "topSelection_%s/SubldgTetrajetMass_Before" % (analysisType),
        "topSelection_%s/SubldgTetrajetEta_Before" % (analysisType),
        "topSelection_%s/SubldgTetrajetPt_After" % (analysisType),
        "topSelection_%s/SubldgTetrajetMass_After" % (analysisType),
        "topSelection_%s/SubldgTetrajetEta_After" % (analysisType),
        "topSelection_%s/Trijet1Mass_Before" % (analysisType),
        "topSelection_%s/Trijet2Mass_Before" % (analysisType),
        "topSelection_%s/Trijet1Mass_After" % (analysisType),
        "topSelection_%s/Trijet2Mass_After" % (analysisType),
        "topSelection_%s/Trijet1Pt_Before" % (analysisType),
        "topSelection_%s/Trijet2Pt_Before" % (analysisType),
        "topSelection_%s/Trijet1Pt_After" % (analysisType),
        "topSelection_%s/Trijet2Pt_After" % (analysisType),
        "topSelection_%s/Trijet1DijetMass_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetMass_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetMass_After" % (analysisType),
        "topSelection_%s/Trijet2DijetMass_After" % (analysisType),
        "topSelection_%s/Trijet1DijetPt_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetPt_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetPt_After" % (analysisType),
        "topSelection_%s/Trijet2DijetPt_After" % (analysisType),
        "topSelection_%s/Trijet1DijetDEta_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetDEta_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetDEta_After" % (analysisType),
        "topSelection_%s/Trijet2DijetDEta_After" % (analysisType),
        "topSelection_%s/Trijet1DijetDPhi_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetDPhi_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetDPhi_After" % (analysisType),
        "topSelection_%s/Trijet2DijetDPhi_After" % (analysisType),
        "topSelection_%s/Trijet1DijetDR_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetDR_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetDR_After" % (analysisType),
        "topSelection_%s/Trijet2DijetDR_After" % (analysisType),
        "topSelection_%s/Trijet1DijetBJetDR_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetBJetDR_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetBJetDR_After" % (analysisType),
        "topSelection_%s/Trijet2DijetBJetDR_After" % (analysisType),
        "topSelection_%s/Trijet1DijetBJetDPhi_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetBJetDPhi_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetBJetDPhi_After" % (analysisType),
        "topSelection_%s/Trijet2DijetBJetDPhi_After" % (analysisType),
        "topSelection_%s/Trijet1DijetBJetDEta_Before" % (analysisType),
        "topSelection_%s/Trijet2DijetBJetDEta_Before" % (analysisType),
        "topSelection_%s/Trijet1DijetBJetDEta_After" % (analysisType),
        "topSelection_%s/Trijet2DijetBJetDEta_After" % (analysisType),
        "topSelection_%s/LdgTrijetPt_Before" % (analysisType),
        "topSelection_%s/LdgTrijetPt_After" % (analysisType),
        "topSelection_%s/LdgTrijetMass_Before" % (analysisType),
        "topSelection_%s/LdgTrijetMass_After" % (analysisType),
        "topSelection_%s/LdgTrijetJet1Pt_Before" % (analysisType),
        "topSelection_%s/LdgTrijetJet1Pt_After" % (analysisType),
        "topSelection_%s/LdgTrijetJet1Eta_Before" % (analysisType),
        "topSelection_%s/LdgTrijetJet1Eta_After" % (analysisType),
        "topSelection_%s/LdgTrijetJet1BDisc_Before" % (analysisType),
        "topSelection_%s/LdgTrijetJet1BDisc_After" % (analysisType),
        "topSelection_%s/LdgTrijetJet2Pt_Before" % (analysisType),
        "topSelection_%s/LdgTrijetJet2Pt_After" % (analysisType),
        "topSelection_%s/LdgTrijetJet2Eta_Before" % (analysisType),
        "topSelection_%s/LdgTrijetJet2Eta_After" % (analysisType),
        "topSelection_%s/LdgTrijetJet2BDisc_Before" % (analysisType),
        "topSelection_%s/LdgTrijetJet2BDisc_After" % (analysisType),
        "topSelection_%s/LdgTrijetBJetPt_Before" % (analysisType),
        "topSelection_%s/LdgTrijetBJetPt_After" % (analysisType),
        "topSelection_%s/LdgTrijetBJetEta_Before" % (analysisType),
        "topSelection_%s/LdgTrijetBJetEta_After" % (analysisType),
        "topSelection_%s/LdgTrijetBJetBDisc_Before" % (analysisType),
        "topSelection_%s/LdgTrijetBJetBDisc_After" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetPt_Before" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetPt_After" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetEta_Before" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetEta_After" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetMass_Before" % (analysisType),
        "topSelection_%s/LdgTrijetDiJetMass_After" % (analysisType),
        "topSelection_%s/SubldgTrijetPt_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetPt_After" % (analysisType),
        "topSelection_%s/SubldgTrijetMass_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetMass_After" % (analysisType),
        "topSelection_%s/SubldgTrijetJet1Pt_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetJet1Pt_After" % (analysisType),
        "topSelection_%s/SubldgTrijetJet1Eta_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetJet1Eta_After" % (analysisType),
        "topSelection_%s/SubldgTrijetJet1BDisc_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetJet1BDisc_After" % (analysisType),
        "topSelection_%s/SubldgTrijetJet2Pt_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetJet2Pt_After" % (analysisType),
        "topSelection_%s/SubldgTrijetJet2Eta_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetJet2Eta_After" % (analysisType),
        "topSelection_%s/SubldgTrijetJet2BDisc_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetJet2BDisc_After" % (analysisType),
        "topSelection_%s/SubldgTrijetBJetPt_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetBJetPt_After" % (analysisType),
        "topSelection_%s/SubldgTrijetBJetEta_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetBJetEta_After" % (analysisType),
        "topSelection_%s/SubldgTrijetBJetBDisc_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetBJetBDisc_After" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetPt_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetPt_After" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetEta_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetEta_After" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetMass_Before" % (analysisType),
        "topSelection_%s/SubldgTrijetDiJetMass_After" % (analysisType),
        # "topSelection_%s/Trijet1MassVsChiSqr_Before" % (analysisType),
        # "topSelection_%s/Trijet2MassVsChiSqr_Before" % (analysisType),
        # "topSelection_%s/Trijet1MassVsChiSqr_After" % (analysisType),
        # "topSelection_%s/Trijet2MassVsChiSqr_After" % (analysisType),
        # "topSelection_%s/Trijet1DijetPtVsDijetDR_Before" % (analysisType),
        # "topSelection_%s/Trijet2DijetPtVsDijetDR_Before" % (analysisType),
        # "topSelection_%s/Trijet1DijetPtVsDijetDR_After" % (analysisType),
        # "topSelection_%s/Trijet2DijetPtVsDijetDR_After" % (analysisType),
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


def getHistos(datasetsMgr, datasetName, name1, name2):
    Verbose("getHistos()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(name1)
    h1.setName("Baseline" + "-" + datasetName)

    h2 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(name2)
    h2.setName("Inverted" + "-" + datasetName)
    return [h1, h2]


def EWKvQCD(datasetsMgr, histoName, analysisType=""):
    Verbose("Plotting EWK Vs QCD unity-normalised histograms for %s" % analysisType)

    # Sanity check
    IsBaselineOrInverted(analysisType)

    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, "Data", "topSelection_Baseline/%s" % histoName, "topSelection_Inverted/%s" % histoName))
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, "EWK", "topSelection_Baseline/%s" % histoName, "topSelection_Inverted/%s" % histoName) )
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get histos    
    data = p1.histoMgr.getHisto(analysisType + "-Data").getRootHisto().Clone(analysisType+ " -Data")
    EWK  = p2.histoMgr.getHisto(analysisType + "-EWK").getRootHisto().Clone(analysisType + "-EWK")
    # Create QCD histos: QCD = Data-EWK
    QCD = p1.histoMgr.getHisto(analysisType + "-Data").getRootHisto().Clone(analysisType + "-QCD")
    QCD.Add(EWK, -1)

    # Normalize histograms to unit area
    QCD.Scale(1.0/QCD.Integral())
    EWK.Scale(1.0/EWK.Integral())

    # Create the final plot object
    p = plots.ComparisonManyPlot(QCD, [EWK], saveFormats=[]) #[".C", ".png", ".pdf"])
    p.setLuminosity(GetLumi(datasetsMgr))
        
    # Apply styles
    p.histoMgr.forHisto(analysisType + "-QCD" , styles.getQCDLineStyle() )
    p.histoMgr.forHisto(analysisType + "-EWK" , styles.getAltEWKStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle(analysisType + "-QCD", "LP")
    p.histoMgr.setHistoLegendStyle(analysisType + "-QCD", "LP")

    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            analysisType + "-QCD" : analysisType + " (QCD)",
            analysisType + "-EWK" : analysisType + " (EWK)",
            })

    # Append analysisType to histogram name
    saveName = histoName + "_" + analysisType

    # Draw the histograms #alex
    plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 

    # _kwargs = {"lessThan": True}
    # p.addCutBoxAndLine(cutValue=200, fillColor=ROOT.kRed, box=False, line=True, ***_kwargs)

    # Save plot in all formats
    saveDir = os.path.join(opts.saveDir, "EWKvQCD", opts.optMode)
    SavePlot(p, saveName, saveDir) 
    return


def IsBaselineOrInverted(analysisType):
    analysisTypes = ["Baseline", "Inverted"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        pass
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
    OPTMODE      = None#"OptChiSqrCutValue25"
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
