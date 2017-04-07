#!/usr/bin/env python
'''
Description:
Generic scipt that plots most TH1 histograms produced by the
FakeBMeasurement.cc class. 

For the definition of the counter class see:
HiggsAnalysis/NtupleAnalysis/scripts

For more counter tricks and optios see also:
HiggsAnalysis/NtupleAnalysis/scripts/hplusPrintCounters.py

Usage:
./plotFakeBAnalysis.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotFakeBAnalysis.py -m old/FakeBMeasurement_170406_LE2Bjets --mergeEWK
./plotFakeBAnalysis.py -m FakeBMeasurement_170315_FullStats/ -v
./plotFakeBAnalysis.py -m FakeBMeasurement_170315_FullStats/ -i "JetHT|TT"
./plotFakeBAnalysis.py -m FakeBMeasurement_170316_FullStats/ --mcOnly --intLumi 100000

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
    #return ["TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
    #return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]
    print "fixme"
    return ["TT"]

def GetHistoKwargs(histoName):
    '''
    '''
    Verbose("Creating a map of histoName <-> kwargs")

    if "pt" in histoName.lower():
        _format = "%0.0f"
        _rebin  = 1
        _logY   = True
        _cutBox = None
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
        _format = "%0.0f"
        _rebin  = 1
        _logY   = True
        _cutBox = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}        
    elif "mass" in histoName.lower():
        _format = "%0.0f"
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
        _format = "%0.2f"
        _rebin  = 1
        _logY   = True
        _cutBox = _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    else:
        raise Exception("The kwargs have not been prepared for the histogram with name \"%s\"." % (histoName) )

    # Customise options (main pad) for with/whitout logY scale 
    if _logY:
        _opts   = {"xmax": 500, "ymin": 2e-4, "ymaxfactor": 5}
    else:
        _opts   = {"xmax": 500.0, "ymin": 0.0, "ymaxfactor": 1.2} 
    print "fixme"

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
                                                        analysisName=opts.analysisName)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def main(opts):
    Verbose("main function")

    comparisonList = ["AfterStdSelections"]

    # Setup & configure the dataset manager 
    datasetsMgr = GetDatasetsFromDir(opts)
    datasetsMgr.updateNAllEventsToPUWeighted()
    datasetsMgr.loadLuminosities() # from lumi.json
    if opts.verbose:
        datasetsMgr.PrintCrossSections()
        datasetsMgr.PrintLuminosities()

    # Check multicrab consistency
    # consistencyCheck.checkConsistencyStandalone(dirs[0],datasets,name="CorrelationAnalysis")

    # Custom Filtering of datasets 
    # datasetsMgr.remove(filter(lambda name: "HplusTB" in name and not "M_500" in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: "ST" in name, datasetsMgr.getAllDatasetNames()))
               
    # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
    plots.mergeRenameReorderForDataMC(datasetsMgr)
   
    # Get Integrated Luminosity
    if opts.mcOnly:
        # Determine integrated lumi
        if opts.intLumi < 0.0:
            opts.intLumi = GetLumi(datasetsMgr)
        else:
            pass
        # Remove data datasets
        datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))

    # Print dataset information
    datasetsMgr.PrintInfo()

    # Re-order datasets (different for inverted than default=baseline)
    newOrder = ["Data"] #, "TT", "DYJetsToQQHT", "TTWJetsToQQ", "WJetsToQQ_HT_600ToInf", "SingleTop", "Diboson", "TTZToQQ", "TTTT"]
    newOrder.extend(GetListOfEwkDatasets())

    if opts.mcOnly:
        newOrder.remove("Data")
    datasetsMgr.selectAndReorder(newOrder)

    # Set/Overwrite cross-sections                                                                                                                                                                                             
    for d in datasetsMgr.getAllDatasets():
        if "ChargedHiggs" in d.getName():
            datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)

    # Merge EWK samples
    if opts.mergeEWK:
        datasetsMgr.merge("EWK", GetListOfEwkDatasets())
        plots._plotStyles["EWK"] = styles.getAltEWKStyle()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)


    # Do the Purity Triples
    if 0:
        Print("Plotting Purity Triplet Histograms", True)
        PurityTripletPlots(datasetsMgr, analysisType="")
        PurityTripletPlots(datasetsMgr, analysisType="EWKFakeB")
        PurityTripletPlots(datasetsMgr, analysisType="EWKGenuineB")
        
    # Do the standard top-selections
    if 0:
        Print("Plotting Top Selection Histograms", True)
        TopSelectionHistograms(datasetsMgr, analysisType="Baseline")
        TopSelectionHistograms(datasetsMgr, analysisType="Inverted")

    # Do other histograms
    if 0:
        Print("Plotting Other Histograms", True)
        OtherHistograms(datasetsMgr, analysisType="Baseline")
        OtherHistograms(datasetsMgr, analysisType="Inverted")

    # Do the Baseline Vs Inverted histograms
    if 0:
        if opts.mergeEWK:
            for hName in getTopSelectionHistos():
                BaselineVsInvertedComparison(datasetsMgr, hName.split("/")[-1])
        else:
            Print("Cannot draw the Baseline Vs Inverted histograms without the option --mergeEWK. Exit", True)

    # Do the Data/QCD/EWK histograms
    if 0:
        if opts.mergeEWK:
            analysisTypes = ["Baseline", "Inverted"]
            for analysis in analysisTypes:
                for hName in getTopSelectionHistos(analysis):
                    DataEwkQcd(datasetsMgr, hName.split("/")[-1], analysis)
        else:
            Print("Cannot draw the Data/QCD/EWK histograms without the option --mergeEWK. Exit", True)


    if 1:
        if opts.mergeEWK:
            analysisTypes = ["Baseline", "Inverted"]
            for analysis in analysisTypes:
                for hName in getTopSelectionHistos(analysis):
                    if "Trijet" not in hName:
                        continue
                    if "Mass" not in hName:
                        print "fixme"
                        continue
                    EWKvQCD(datasetsMgr, hName.split("/")[-1], analysis)
        else:
            Print("Cannot draw the EWKvQCD histograms without the option --mergeEWK. Exit", True)
                    
    return


def PurityTripletPlots(datasetsMgr, analysisType=""):
    '''
    Create data-MC comparison plot, with the default:
    - legend labels (defined in plots._legendLabels)
    - plot styles (defined in plots._plotStyles, and in styles)
    - drawing styles ('HIST' for MC, 'EP' for data)
    - legend styles ('L' for MC, 'P' for data)
    '''
    Verbose("Plotting the Purity-Triplets for %s" % analysisType)

    analysisTypes = ["", "EWKFakeB", "EWKGenuineB"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        folder = "FakeBPurity" + analysisType

    # Definitions
    histoNames  = []    
    histoKwargs = {}
    saveFormats = [".C", ".png", ".pdf"]
    
    # General Settings
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": -0.15}
    else:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": 0.1}

    _kwargs = {"xlabel": "",
               "ylabel": "",
               "rebinX": 1,
               "rebinY": None,
               "ratioYlabel": "Data/MC",
               "ratio": False, 
               "stackMCHistograms": True,
               "ratioInvert": False, 
               "addMCUncertainty": False, 
               "addLuminosityText": True,
               "addCmsText": True,
               "cmsExtraText": "Preliminary",
               "opts": {"ymin": 2e-1, "ymaxfactor": 10},
               "opts2": {"ymin": 0.0, "ymax": 2.0},
               "log": True,
               "errorBarsX": True, 
               "moveLegend": _moveLegend,
               "cutBox": {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
               }

    # Create/Draw the plots
    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscPt_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet p_{T} (GeV/c)"
    kwargs["ylabel"] = "Events / %.0f GeV/c"
    kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscPt_AfterAllSelections" % folder] = kwargs


    if opts.histoLevel == "Debug":
        histoNames.append("%s/Inverted_FailedBJetWithBestBDiscEta_AfterAllSelections" % folder)
        kwargs = copy.deepcopy(_kwargs)
        kwargs["xlabel"] = "jet #eta"
        kwargs["ylabel"] = "Events / %.2f"
        histoKwargs["%s/Inverted_FailedBJetWithBestBDiscEta_AfterAllSelections" % folder] = kwargs
        

    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet b-tag discriminator"
    kwargs["ylabel"] = "Events / %.2f"
    kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": True, "line": True, "greaterThan": False}
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections" % folder] = kwargs
        

    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "jet pdgId"
    kwargs["ylabel"] = "Events / %.0f"
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections" % folder] = kwargs


    if opts.histoLevel == "Debug":
        histoNames.append("%s/Inverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections" % folder)
        kwargs = copy.deepcopy(_kwargs)
        kwargs["xlabel"] = "jet parton flavour"
        kwargs["ylabel"] = "Events / %.0f"
        histoKwargs["%s/Inverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections" % folder] = kwargs


    if opts.histoLevel == "Debug":
        histoNames.append("%s/Inverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections" % folder)
        kwargs = copy.deepcopy(_kwargs)
        kwargs["xlabel"] = "jet hadron flavour"
        kwargs["ylabel"] = "Events / %.0f"
        histoKwargs["%s/Inverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections" % folder] = kwargs


    histoNames.append("%s/Inverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections" % folder)
    kwargs = copy.deepcopy(_kwargs)
    kwargs["xlabel"] = "ancestor bit"
    kwargs["ylabel"] = "Events / %.0f"
    histoKwargs["%s/Inverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections" % folder] = kwargs


    # For-loop: All histograms in list
    for histoName in histoNames:
        kwargs_  = histoKwargs[histoName]
        saveName = os.path.join(opts.saveDir, histoName.replace("/", "_"))

        if opts.mcOnly:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
            kwargs_.pop("ratio", None)
            kwargs_.pop("ratioYlabel", None)
            kwargs_.pop("ratioInvert", None)
            kwargs_.pop("opts2", None)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        else:
            p = plots.DataMCPlot(datasetsMgr, histoName)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary

        ## For-loop: All save formats
        for i, ext in enumerate(saveFormats):
            Print("%s" % saveName + ext, i==0)
            p.saveAs(saveName, formats=saveFormats)

    return


def OtherHistograms(datasetsMgr, analysisType=""):
    '''
    Create data-MC comparison plot, with the default:
    - legend labels (defined in plots._legendLabels)
    - plot styles (defined in plots._plotStyles, and in styles)
    - drawing styles ('HIST' for MC, 'EP' for data)
    - legend styles ('L' for MC, 'P' for data)
    '''
    Verbose("Plotting all other histograms for %s" % analysisType)

    # Sanity check
    IsBaselineOrInverted(analysisType)

    # Definitions
    histoNames  = []
    histoKwargs = {}
    saveFormats = [".C", ".png", ".pdf"]

    # General Settings
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": -0.15}
    else:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": 0.1}

    _kwargs = {"rebinX": 1,
               "rebinY": None,
               "ratioYlabel": "Data/MC",
               "ratio": False, 
               "stackMCHistograms": True,
               "ratioInvert": False, 
               "addMCUncertainty": False, 
               "addLuminosityText": True,
               "addCmsText": True,
               "cmsExtraText": "Preliminary",
               "opts": {"ymin": 2e-1, "ymaxfactor": 10}, #1.2
               "opts2": {"ymin": 0.0, "ymax": 2.0},
               "log": True,
               "errorBarsX": True, 
               "moveLegend": _moveLegend,
               "cutBox": {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
               }

    # Create/Draw the plots
    histoName = "%s_TopMassReco_LdgTrijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_LdgTrijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    kwargs["log"]    = False
    kwargs["opts"]   = {"xmax": 700, "ymin": 2e-1, "ymaxfactor": 1.2}
    kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgTrijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgTrijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    kwargs["log"]    = False
    kwargs["opts"]   = {"xmax": 700, "ymin": 2e-1, "ymaxfactor": 1.2}
    kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_LdgDijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_LdgDijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    kwargs["cutBox"] = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgDijetPt_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs

    histoName = "%s_TopMassReco_SubLdgDijetM_AfterAllSelections" % analysisType
    kwargs = copy.deepcopy(_kwargs)
    kwargs["ylabel"] = "Events / %.0f"
    kwargs["cutBox"] = {"cutValue": 80.399, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    histoNames.append(histoName)
    histoKwargs[histoName] = kwargs


    # For-loop: All histograms in list
    for histoName in histoNames:
        kwargs_  = histoKwargs[histoName]
        saveName = os.path.join(opts.saveDir, histoName.replace("/", "_"))

        if opts.mcOnly:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
            kwargs_.pop("ratio", None)
            kwargs_.pop("ratioYlabel", None)
            kwargs_.pop("ratioInvert", None)
            kwargs_.pop("opts2", None)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        else:
            p = plots.DataMCPlot(datasetsMgr, histoName)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary

        # For-loop: All save formats
        for i, ext in enumerate(saveFormats):
            Print("%s" % saveName + ext, i==0)
            p.saveAs(saveName, formats=saveFormats)
    return


def getTopSelectionHistos(analysisType="Baseline"):
    '''
    Returns the list of histograms created by
    the TopSelection class
    '''
    Verbose("Creating histogram list for %s" % analysisType, True)

    # Sanity check
    IsBaselineOrInverted(analysisType)

    histoList = [        
        "topSelection_%s/ChiSqr_Before" % (analysisType),
        "topSelection_%s/ChiSqr_After" % (analysisType),
        "topSelection_%s/NJetsUsedAsBJetsInFit_Before" % (analysisType),
        "topSelection_%s/NJetsUsedAsBJetsInFit_After" % (analysisType),
        "topSelection_%s/NumberOfFits_Before" % (analysisType),
        "topSelection_%s/NumberOfFits_After" % (analysisType),
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
    return histoList


def TopSelectionHistograms(datasetsMgr, analysisType=""):
    '''
    Create data-MC comparison plot, with the default:
    - legend labels (defined in plots._legendLabels)
    - plot styles (defined in plots._plotStyles, and in styles)
    - drawing styles ('HIST' for MC, 'EP' for data)
    - legend styles ('L' for MC, 'P' for data)
    '''
    Verbose("Plotting all topSelection histograms for %s" % analysisType)

    # Sanity check
    IsBaselineOrInverted(analysisType)

    # Definitions
    histoNames  = getTopSelectionHistos(analysisType)
    histoKwargs = {}
    saveFormats = [".C", ".png", ".pdf"]

    # General Settings
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": -0.15}
    else:
        _moveLegend = {"dx": -0.05, "dy": 0.0, "dh": 0.1}

    _kwargs = {"rebinX": 1,
               "rebinY": None,
               "ratioYlabel": "Data/MC",
               "ratio": False, 
               "stackMCHistograms": True,
               "ratioInvert": False, 
               "addMCUncertainty": False, 
               "addLuminosityText": True,
               "addCmsText": True,
               "cmsExtraText": "Preliminary",
               "opts": {"ymin": 2e-1, "ymaxfactor": 10}, #1.2
               "opts2": {"ymin": 0.0, "ymax": 2.0},
               "log": True,
               "errorBarsX": True, 
               "moveLegend": _moveLegend,
               "cutBox": {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True},
               "ylabel": "Events / %.0f",
               }

    # Create/Draw the plots
    for histoName in histoNames:
        histoKwargs[histoName] = _kwargs

    # For-loop: All histograms in list
    for histoName in histoNames:
        kwargs_  = histoKwargs[histoName]
        saveName = os.path.join(opts.saveDir, histoName.replace("/", "_"))

        if opts.mcOnly:
            p = plots.MCPlot(datasetsMgr, histoName, normalizeToLumi=opts.intLumi)
            kwargs_.pop("ratio", None)
            kwargs_.pop("ratioYlabel", None)
            kwargs_.pop("ratioInvert", None)
            kwargs_.pop("opts2", None)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        else:
            p = plots.DataMCPlot(datasetsMgr, histoName)
            plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary

        # For-loop: All save formats
        for i, ext in enumerate(saveFormats):
            Print("%s" % saveName + ext, i==0)
            p.saveAs(saveName, formats=saveFormats)
    return
    
                         
def getHistos(datasetsMgr, datasetName, name1, name2):

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(name1)
    h1.setName("Baseline" + "-" + datasetName)

    h2 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(name2)
    h2.setName("Inverted" + "-" + datasetName)
    return [h1, h2]


def BaselineVsInvertedComparison(datasetsMgr, histoName):
    
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, "Data", "topSelection_Baseline/%s" % histoName, "topSelection_Inverted/%s" % histoName))
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, "EWK", "topSelection_Baseline/%s" % histoName, "topSelection_Inverted/%s" % histoName) )
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get Data histos    
    baseline_Data = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone("Baseline-Data")
    inverted_Data = p1.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone("Inverted-Data")
    # Get EWK histos
    baseline_EWK = p2.histoMgr.getHisto("Baseline-EWK").getRootHisto().Clone("Baseline-EWK")
    inverted_EWK = p2.histoMgr.getHisto("Inverted-EWK").getRootHisto().Clone("Inverted-EWK")
    # Create QCD histos: QCD = Data-EWK
    baseline_QCD = p1.histoMgr.getHisto("Baseline-Data").getRootHisto().Clone("Baseline-QCD")
    baseline_QCD.Add(baseline_EWK, -1)
    inverted_QCD = p1.histoMgr.getHisto("Inverted-Data").getRootHisto().Clone("Inverted-QCD")
    inverted_QCD.Add(inverted_EWK, -1)

    # Normalize histograms to unit area
    baseline_QCD.Scale(1.0/baseline_QCD.Integral())
    inverted_QCD.Scale(1.0/inverted_QCD.Integral())

    # Create the final plot object
    p = plots.ComparisonManyPlot(baseline_QCD, [inverted_QCD], saveFormats=[]) #[".C", ".png", ".pdf"])
    p.setLuminosity(GetLumi(datasetsMgr))
        
    # Apply styles
    p.histoMgr.forHisto("Baseline-QCD" , styles.getBaselineStyle() )
    p.histoMgr.forHisto("Inverted-QCD" , styles.getInvertedStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle("Baseline-QCD", "LP")
    p.histoMgr.setHistoLegendStyle("Baseline-QCD", "LP")
    # p.histoMgr.setHistoLegendStyleAll("LP")

    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            "Baseline-QCD" : "Baseline (QCD)",
            "Inverted-QCD" : "Inverted (QCD)",
            })

    # Draw the histograms. FixMe
    _rebinX = 1
    if "Mass" or "ChiSqr" in histoName:
        _rebinX = 2
        Print("Rebin is set to %s for %s" % (_rebinX, histoName), True)

    plots.drawPlot(p, histoName,  
                   ylabel = "Events / %.0f",
                   log = True, 
                   rebinX = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.62, "y1": 0.78, "x2": 0.92, "y2": 0.92},
                   opts  = {"ymin": 1e-4, "ymaxfactor": 1.2},
                   opts2 = {"ymin": 0.6, "ymax": 1.4},
                   ratio = True,
                   ratioInvert = False, 
                   ratioYlabel = "Ratio",
                   cutBox = None,
                   )
    
    # For-loop: All save formats
    SavePlot(p, histoName, os.path.join(opts.saveDir, "BaselineVsInverted") ) 
    return


def EWKvQCD(datasetsMgr, histoName, analysisType=""):
    '''
    '''
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

    # Draw the histograms
    plots.drawPlot(p, saveName, **GetHistoKwargs(histoName) ) #the "**" unpacks the kwargs_ 
    # _kwargs = {"lessThan": True}
    # p.addCutBoxAndLine(cutValue=200, fillColor=ROOT.kRed, box=False, line=True, ***_kwargs)

    # For-loop: All save formats
    SavePlot(p, saveName, os.path.join(opts.saveDir, "EWKvQCD") ) 
    return


def IsBaselineOrInverted(analysisType):
    analysisTypes = ["Baseline", "Inverted"]
    if analysisType not in analysisTypes:
        raise Exception("Invalid analysis type \"%s\". Please select one of the following: %s" % (analysisType, "\"" + "\", \"".join(analysisTypes) + "\"") )
    else:
        pass
    return


def DataEwkQcd(datasetsMgr, histoName, analysisType):
    '''
    Create plots with "Data", "QCD=Data-EWK", and "EWK" on the same canvas
    Mostly for sanity checks and visualisation purposes
    '''
    Verbose("Plotting histogram %s for Data, EWK, QCD for %s" % (histoName, analysisType), True)

    # Sanity check
    IsBaselineOrInverted(analysisType)

    # Define histogram names (full path)
    h1 = "topSelection_Baseline/%s" % (histoName)
    h2 = "topSelection_Inverted/%s" % (histoName)

    # Create plot object for Data
    p1 = plots.ComparisonPlot(*getHistos(datasetsMgr, "Data", h1, h2) )
    p1.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())
    # Create plot object for EWK
    p2 = plots.ComparisonPlot(*getHistos(datasetsMgr, "EWK", h1, h2) )
    p2.histoMgr.normalizeMCToLuminosity(datasetsMgr.getDataset("Data").getLuminosity())

    # Get Data and EWK histos
    Data = p1.histoMgr.getHisto(analysisType + "-Data").getRootHisto().Clone(analysisType + "-Data")
    EWK  = p2.histoMgr.getHisto(analysisType + "-EWK").getRootHisto(). Clone(analysisType + "-EWK")

    # Create QCD histo: QCD = Data-EWK
    QCD  = p1.histoMgr.getHisto(analysisType + "-Data").getRootHisto().Clone(analysisType + "-QCD")
    QCD.Add(EWK, -1)
    
    # Create the final plot object. The Data is treated as the reference histo. 
    # All other histograms are compared with respect to that. 
    p = plots.ComparisonManyPlot(Data, [QCD, EWK], saveFormats=[])
    p.setLuminosity(GetLumi(datasetsMgr))

    # Apply histo styles
    p.histoMgr.forHisto(analysisType + "-Data", styles.getDataStyle() )
    p.histoMgr.forHisto(analysisType + "-QCD" , styles.getQCDLineStyle() )
    p.histoMgr.forHisto(analysisType + "-EWK" , styles.getAltEWKStyle() )

    # Set draw style
    p.histoMgr.setHistoDrawStyle(analysisType + "-Data", "P")
    p.histoMgr.setHistoLegendStyle(analysisType + "-Data", "P")
    p.histoMgr.setHistoDrawStyle(analysisType + "-QCD", "LP")
    p.histoMgr.setHistoLegendStyle(analysisType + "-QCD", "LP")
    p.histoMgr.setHistoDrawStyle(analysisType + "-EWK", "HIST")
    p.histoMgr.setHistoLegendStyle(analysisType + "-EWK", "LFP")
    # p.histoMgr.setHistoLegendStyleAll("LP")

    # Set legend labels
    p.histoMgr.setHistoLegendLabelMany({
            analysisType + "-Data": "%s (Data)" % (analysisType),
            analysisType + "-QCD" : "%s (QCD)"  % (analysisType),
            analysisType + "-EWK" : "%s (EWK)"  % (analysisType),
            })
    
    # Draw the histograms
    #_cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    _rebinX = 1
    if "Mass" in histoName:
        _rebinX = 2
        Print("Rebin is set to %s for %s" % (_rebinX, histoName), True)

    histoName += "_" + analysisType
    plots.drawPlot(p, histoName,  
                   ylabel = "Events / %.0f",
                   log = True, 
                   rebinX = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.62, "y1": 0.78, "x2": 0.92, "y2": 0.92},
                   opts  = {"ymin": 1e0, "ymaxfactor": 10},
                   opts2 = {"ymin": 1e-5, "ymax": 1e0},
                   ratio = True,
                   ratioInvert = False, 
                   ratioYlabel = "Ratio",
                   cutBox = None
                   )

    # Save the plot in default formats
    SavePlot(p, histoName, os.path.join(opts.saveDir, "DataEwkQcd") ) 
    return


def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if not opts.noURL:
            Print(saveName + ext, i==0)
        else:
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
    ANALYSISNAME = "FakeBMeasurement"
    BATCHMODE    = True
    DATAERA      = "Run2016"
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MCONLY       = False
    MERGEEWK     = False
    NOURL        = True
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    SEARCHMODE   = "80to1000"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Never', 'Systematics', 'Vital', 'Informative', 'Debug'

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

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

    parser.add_option("--noURL", dest="noURL", action="store_false", default=NOURL, 
                      help="Do print the actual save path the histogram is saved (and not the URL) [default: %s]" % NOURL)
    
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
