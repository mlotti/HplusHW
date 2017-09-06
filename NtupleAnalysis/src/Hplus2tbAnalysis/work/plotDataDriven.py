#!/usr/bin/env python
'''
Description:

Usage:
./plotDataDriven.py -m <pseudo_mcrab_directory> [opts]

Examples:
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_HLTBJetTrgMatch_TopCut10_H2Cut0p5_170720_104648 --url -o ""
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170817_025841/ --url --signalMass 500
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170810_022933/ --url --signalMass 800
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_HLTBJetTrgMatch_TopCut10_H2Cut0p5_170720_104648 --url --signalMass 800

Last Used:
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170827_075947/ --url
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_InvMassFix_170822_074229/ --url --signalMass 800
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170817_025841/ --url --signalMass 500
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
    #return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]
    return  ["TT", "WJetsToQQ_HT_600ToInf", "SingleTop", "DYJetsToQQHT", "TTZToQQ",  "TTWJetsToQQ", "Diboson", "TTTT"]

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

    #optModes = ["", "OptChiSqrCutValue50", "OptChiSqrCutValue100"]
    optModes = [""]

    if opts.optMode != None:
        optModes = [opts.optMode]
        
    # For-loop: All opt Mode
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0) # ATLAS 13 TeV H->tb exclusion limits
                
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
   
        # Custom Filtering of datasets 
        datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
        # datasetsMgr.remove(filter(lambda name: "Charged" in name, datasetsMgr.getAllDatasetNames()))

        # Replace QCD MC with QCD-DataDriven
        qcdDatasetName    = "FakeBMeasurementTrijetMass"
        qcdDatasetNameNew = "QCD-Data"
        if opts.mcQCD:
            pass
        else:
            replaceQCDFromData(datasetsMgr, qcdDatasetName, qcdDatasetNameNew)

        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"]
        if opts.signalMass != 0:
            signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass
            newOrder.extend([signal])
        if opts.mcQCD:
            newOrder.extend(["QCD"])
        else:
            newOrder.extend(["QCD-Data"])
        newOrder.extend(GetListOfEwkDatasets())
        datasetsMgr.selectAndReorder(newOrder)
        
        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)

        # Do Data-MC histograms with DataDriven QCD
        DataMCHistograms(datasetsMgr, qcdDatasetNameNew)
    return

def GetHistoKwargs(histoList, opts):
    '''
    Dictionary with 
    key   = histogramName
    value = kwargs
    '''
    
    histoKwargs = {}
    _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": 0.1}
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.12}    
    logY = True

    _kwargs = {
        "ylabel"           : "Events / %.0f",
        "rebinX"           : 1,
        "rebinY"           : None,
        "ratioYlabel"      : "Data/Bkg",
        "ratio"            : True, 
        "stackMCHistograms": True,
        "ratioInvert"      : False, 
        "addMCUncertainty" : False, 
        "addLuminosityText": True,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 2e-1, "ymaxfactor": 10}, #1.2
        "opts2"            : {"ymin": 0.0, "ymax": 2.0},
        "log"              : logY,
        "moveLegend"       : _moveLegend,
        }

    for h in histoList:
        kwargs = copy.deepcopy(_kwargs)
        if "met" in h.lower():
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "E_{T}^{miss} (%s)" % units
        if "NVertices" in h:
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "Vertices"
        if "Njets" in h:                
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "Jets Multiplicity"
            kwargs["cutBox"] = {"cutValue": 7.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "JetPt" in h:                
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "JetEta" in h:                
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "#eta"
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": 10}
        if "NBjets" in h:                
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "b-Jets Multiplicity"
            kwargs["cutBox"] = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 10.0, "ymin": 1e+0, "ymaxfactor": 10}
        if "BjetPt" in h:                
            units = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "BjetEta" in h:                
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "#eta"
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": 10}
        if "BtagDiscriminator" in h:                
            kwargs["ylabel"]     = "Events / %.2f"
            kwargs["xlabel"]     = "b-Tag Discriminator"
            kwargs["cutBox"]     = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["moveLegend"] = {"dx": -0.5, "dy": -0.01, "dh": 0.0}
            kwargs["opts"]       = {"xmin": 0.0, "xmax": 1.05, "ymin": 1e+0, "ymaxfactor": 10}
        if "HT" in h:
            units            = "GeV"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "H_{T} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["rebinX"] = 5
            kwargs["opts"]   = {"xmin": 500.0, "xmax": 4100, "ymin": 1e+0, "ymaxfactor": 10}
        if "MHT" in h:
            units            = "GeV"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "MHT (%s)"  % units
            kwargs["rebinX"] = 2
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 400, "ymin": 1e+0, "ymaxfactor": 10}
        if "Sphericity" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "Sphericity"
        if "Aplanarity" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "Aplanarity"
        if "Circularity" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "Circularity"
        if "Circularity" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "Circularity"
        if "ThirdJetResolution" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "y_{23}"
        if "FoxWolframMoment" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "H_{2}"
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 1.01}
            kwargs["cutBox"] = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "Centrality" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "Centrality"
            kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": 0.0}
        if "TopFitChiSqr" in h:
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "#chi^{2}"
            kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["rebinX"] = 2
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 180.0, "ymin": 1e+0, "ymaxfactor": 10}
        if "LdgTrijetPt" in h:
            units = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "LdgTrijetDijetPt" in h:
            units = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 700.0, "ymin": 1e+0, "ymaxfactor": 10}
        if "LdgTrijetMass" in h:
            startBlind       = 115 #135 v. sensitive to bin-width!
            endBlind         = 225 #205 v. sensitive to bin-width!
            kwargs["rebinX"] = 4
            units            = "GeV/c^{2}"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "m_{jjb} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 1200.0, "ymin": 1e+0, "ymaxfactor": 10}
            if "AllSelections" in h:
                kwargs["blindingRangeString"] = "%s-%s" % (startBlind, endBlind)
                kwargs["moveBlindedText"]     = {"dx": -0.22, "dy": +0.08, "dh": -0.12}
        if "LdgTrijetBjetPt" in h:
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "LdgTrijetBjetEta" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "#eta"
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": 10}
        if "SubldgTrijetPt" in h:
            units = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "SubldgTrijetMass" in h:
            startBlind       = 115 #135 v. sensitive to bin-width!
            endBlind         = 225 #205 v. sensitive to bin-width!
            kwargs["rebinX"] = 1
            units            = "GeV/c^{2}"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "m_{jjb} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 1200.0, "ymin": 1e+0, "ymaxfactor": 10}
            if "AllSelections" in h:
                kwargs["blindingRangeString"] = "%s-%s" % (startBlind, endBlind)
                kwargs["moveBlindedText"]     = {"dx": -0.22, "dy": +0.08, "dh": -0.12}
        if "SubldgTrijetBjetPt" in h:
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "SubldgTrijetBjetEta" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "#eta"
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": 10}
        if "LdgTetrajetPt" in h:
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "LdgTetrajetMass" in h:
            ROOT.gStyle.SetNdivisions(5, "X")
            startBlind       = 150  # 135 v. sensitive to bin-width!
            endBlind         = 2500 #v. sensitive to bin-width!
            kwargs["rebinX"] = 4
            units            = "GeV/c^{2}"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "m_{jjbb} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": endBlind, "ymin": 1e+0, "ymaxfactor": 10}
            #kwargs["opts"]   = {"xmin": 0.0, "xmax": 2000, "ymin": 1e+0, "ymaxfactor": 10}
            if "AllSelections" in h:
                kwargs["blindingRangeString"] = "%s-%s" % (startBlind, endBlind)
                kwargs["moveBlindedText"]     = {"dx": -0.22, "dy": +0.08, "dh": -0.12}
        if "SubldgTetrajetPt" in h:
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "SubldgTetrajetMass" in h:
            startBlind       = 135  # 175 v. sensitive to bin-width!
            endBlind         = 3000
            kwargs["rebinX"] = 2
            units            = "GeV/c^{2}"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "m_{jjbb} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": endBlind, "ymin": 1e+0, "ymaxfactor": 10}
            kwargs["cutBox"] = {"cutValue": 7.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            if "AllSelections" in h:
                kwargs["blindingRangeString"] = "%s-%s" % (startBlind, endBlind)
                kwargs["moveBlindedText"] = {"dx": -0.22, "dy": +0.08, "dh": -0.12}
        if "TetrajetBjetPt" in h:
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "TetrajetBjetEta" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "#eta"
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": 10}
        if "TopMassWMassRatio" in h:
            kwargs["ylabel"] = "Events / %.1f"
            kwargs["xlabel"] = "R_{3/2}"
            #kwargs["cutBox"] = {"cutValue": (173.21/80.385), "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["cutBox"] = {"cutValue": (172.5/80.385), "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            #kwargs["cutBox"] = {"cutValue": 2.1, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            #kwargs["opts"]   = {"xmin": 0, "xmax": +10.0, "ymin": 1e+0, "ymaxfactor": 1.2}
            kwargs["opts"]   = {"xmin": 0, "xmax": +10.0, "ymin": 1e+0, "ymaxfactor": 10}
            kwargs["log"]    = True#False

        histoKwargs[h] = kwargs
    return histoKwargs
    
def DataMCHistograms(datasetsMgr, qcdDatasetName):
    Verbose("Plotting Data-MC Histograms")

    # Definitions
    histoNames  = []
    saveFormats = [".png"] #[".C", ".png", ".pdf"]

    # Get list of histograms
    dataPath    = "ForDataDrivenCtrlPlots"
    allHistos   = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(dataPath)
    histoList   = [h for h in allHistos if "StandardSelections" in h]
    histoList.extend([h for h in allHistos if "AllSelections" in h])
    histoList   = [h for h in histoList if "_MCEWK" not in h]
    histoList   = [h for h in histoList if "_Purity" not in h]
    histoPaths  = [dataPath + "/" + h for h in histoList]

    # Get histogram<->kwargs dictionary 
    histoKwargs = GetHistoKwargs(histoPaths, opts)

    # For-loop: All histograms in list
    for histoName in histoPaths:

        if "LdgTetrajetMass" not in histoName:
            continue

        if "JetEtaPhi" in histoName:
            continue

        if opts.signalMass == 0:
            if "LdgTrijetMass" in histoName:
                continue
            
            if "LdgTetrajetMass" in histoName:
                continue

        if "Vs" in histoName:
            continue

        # Not used in this analysis (yet)
        if "MHT" in histoName:
            continue

        # By definition of the Inverted sample the following histoscannot agree!
        if "NBjets_" in histoName:
            continue
        if "BJetPt_" in histoName:
            continue
        if "_BJetEta_" in histoName:
            continue
        if "_BtagDiscriminator_" in histoName:
            continue

        kwargs_  = histoKwargs[histoName]
        saveName = histoName.replace("/", "_")

        # Create the plotting object
        p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])

        # Apply QCD data-driven style
        if opts.signalMass != 0:
            signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass
            mHPlus = "%s" % int(opts.signalMass)
            p.histoMgr.forHisto(signal, styles.getSignalStyleHToTB_M(mHPlus))

        #p.histoMgr.forHisto(opts.signalMass, styles.getSignalStyleHToTB())
        if opts.mcQCD:
            pass
        else:
            p.histoMgr.forHisto(qcdDatasetName, styles.getAltQCDStyle())
            p.histoMgr.setHistoDrawStyle(qcdDatasetName, "HIST")
            p.histoMgr.setHistoLegendStyle(qcdDatasetName, "F")

        if not opts.mcQCD:
            p.histoMgr.setHistoLegendLabelMany({
                    qcdDatasetName: "QCD (Data)",
                    })
        else:
            p.histoMgr.setHistoLegendLabelMany({
                    "QCD": "QCD (MC)",
                    })            

        # Apply blinding of signal region
        if "blindingRangeString" in kwargs_:
            startBlind = float(kwargs_["blindingRangeString"].split("-")[1])
            endBlind   = float(kwargs_["blindingRangeString"].split("-")[0])
            plots.partiallyBlind(p, maxShownValue=startBlind, minShownValue=endBlind, invert=True, moveBlindedText=kwargs_["moveBlindedText"])

        # Draw and save the plot
        plots.drawPlot(p, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode) )
    return

def getHisto(datasetsMgr, datasetName, histoName):
    Verbose("getHisto()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(datasetName)
    return h1

def replaceQCDFromData(dMgr, dataDrivenDatasetName, newName="QCD-Data"):
    
    # Define variables
    mcQCDName      = "QCD"
    dataDrivenQCD  = dMgr.getDataset(dataDrivenDatasetName)
    dataDrivenQCD.setName(newName)

    # Get list of dataset names
    names = dMgr.getAllDatasetNames()

    # Return the index in the list of the first dataset whose name is mcQCDName.
    index = names.index(mcQCDName)

    # Remove the dataset at the given position in the list, and return it. 
    names.pop(index)
    
    # Insert the dataset to the given position  (index) of the list
    names.insert(index, dataDrivenQCD.getName())

    # Remove from the dataset manager the mcQCDName
    dMgr.remove(mcQCDName)
    names.pop(names.index(dataDrivenQCD.getName()))
    
    # Select and reorder Datasets. 
    # This method can be used to either select a set of dataset.Dataset objects. reorder them, or both.
    dMgr.selectAndReorder(names)
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):
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
    ANALYSISNAME = "Hplus2tbAnalysis"
    MCQCD        = False
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MCONLY       = False
    SIGNALMASS   = 0
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/Results/"
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

    parser.add_option("--mcQCD", dest="mcQCD", action="store_true", default=MCQCD,
                      help="Do not replace QCD MC with Data-Driven QCD Background Estiomation [default: %s]" % MCQCD)

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

    parser.add_option("--signalMass", dest="signalMass", type=float, default=SIGNALMASS, 
                     help="Mass value of signal to use [default: %s]" % SIGNALMASS)

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

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotDataDriven.py: Press any key to quit ROOT ...")
