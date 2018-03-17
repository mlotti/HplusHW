#!/usr/bin/env python
'''
DESCRIPTIONM:
Script that plots Data/MC for all histograms under a given folder (passsed as option to the script)
Good for sanity checks for key points in the cut-flow


USAGE:
./plotDataMC_ControlPlots.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plotDataMC_ControlPlots.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/SignalAnalysis/Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_TopCut10_171012_011451 --folder topologySelection_
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_TopCut10_171012_011451 --folder jetSelection_ --url
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_TopMVA0p90_171106_064503 --folder topbdtSelection_ -e "QCD_HT50to100|QCD_HT100to200|QCD_HT200to300|QCD_HT300to500"
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_TopMVA0p90_171106_064503/ --url --signalMass 500
./plotDataMC_ControlPlots.py -m /uscms_data/d3/aattikis/workspace/pseudo-multicrab/SignalAnalysis/Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_TopCut10_171012_011451 --folder ForDataDrivenCtrlPlots --signalMass 500 -e "FakeB"
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_MVA0p80_MVA0p80_TopMassCutOff600GeV_180104_043952 --folder counters/weighted --url


LAST USED:
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder PUDependency
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder counters/weighted
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder eSelection_Veto
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder muSelection_Veto
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder tauSelection_Veto
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder jetSelection_
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder bjetSelection_
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder topbdtSelection_
./plotDataMC_ControlPlots.py -m Hplus2tbAnalysis_NewLeptonVeto_3bjets40_MVA0p85_MVA0p85_TopMassCutOff600GeV_180122_022900/ --folder ForDataDrivenCtrlPlots

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

        # Define datasets to remove by default
        QCD_list = ["QCD_HT700to1000", "QCD_HT50to100", "QCD_HT500to700", "QCD_HT300to500", 
                    "QCD_HT200to300", "QCD_HT2000toInf", "QCD_HT1500to2000", "QCD_HT100to200", "QCD_HT1000to1500"]
        QCDExt_list = [x+"_ext1" for x in QCD_list]
        datasetsToRemove = ["QCD-b"]
        # datasetsToRemove.extend(QCD_list)
        # datasetsToRemove.extend(QCDExt_list)

        # ZJets and DYJets overlap
        if "ZJetsToQQ_HT600toInf" in datasetsMgr.getAllDatasetNames() and "DYJetsToQQ_HT180" in datasetsMgr.getAllDatasetNames():
            Print("Cannot use both ZJetsToQQ and DYJetsToQQ due to duplicate events? Investigate. Removing ZJetsToQQ datasets for now ..", True)
            datasetsMgr.remove(filter(lambda name: "ZJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "DYJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
        
        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0) # ATLAS 13 TeV H->tb exclusion limits
                if d.getName() != opts.signal:
                    datasetsToRemove.append(d.getName())

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Custom Filtering of datasets 
        for i, d in enumerate(datasetsToRemove, 0):
            msg = "Removing dataset %s" % d
            Verbose(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
            datasetsMgr.remove(filter(lambda name: d == name, datasetsMgr.getAllDatasetNames()))

        if opts.verbose:
            datasetsMgr.PrintInfo()
  
        # Re-order datasets (different for inverted than default=baseline)
        newOrder = ["Data"]
        for i, d in enumerate(datasetsMgr.getAllDatasets(), 0):
            if d.isData():
                continue
            else:
                newOrder.append(d.getName())

        # Re-arrange dataset order?
        if 0:
            s = newOrder.pop( newOrder.index("noTop") )
            newOrder.insert(len(newOrder), s) #after "Data"

        # Move signal to top
        if opts.signal in newOrder:
            s = newOrder.pop( newOrder.index(opts.signal) )
            newOrder.insert(1, s)
        datasetsMgr.selectAndReorder(newOrder)
        
        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(opts.gridX)
        style.setGridY(opts.gridY)

        # Do Data-MC histograms with DataDriven QCD
        folder     = opts.folder
        histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)        
        histoPaths = [os.path.join(folder, h) for h in histoList]
        ignoreList = ["Aplanarity", "Planarity", "Sphericity", "FoxWolframMoment", "Circularity", "ThirdJetResolution", "Centrality", "_Vs_"]
        myHistos   = []
        for h in histoPaths:
            skip = False

            # Skip unwanted histos
            for i in ignoreList:
                if i in h:
                    skip = True

            if skip:
                continue
            else:
                myHistos.append(h)

        for i, h in enumerate(myHistos, 1):
            # Plot the histograms!
            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i, "/", "%s:" % (len(myHistos)), h)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)

            DataMCHistograms(datasetsMgr, h)
        
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)    
    return

def GetHistoKwargs(h, opts):

    # Common bin settings
    myBins  = []
    vtxBins = []
    ptBins  = []
    bWidth  = 2    
    for i in range(0, 40, bWidth):
        vtxBins.append(i)
    bWidth  = 10 #25
    for i in range(40, 100+bWidth, bWidth):
        vtxBins.append(i)

    _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": +0.1}
    if opts.mergeEWK:
        _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.12}    
    logY    = True
    _yLabel = "Events / %.0f "
    yMin    = 1e-1
    yMaxF   = 1.2
    if logY:
        yMaxF = 20#10

    _kwargs = {
        "ylabel"           : _yLabel,
        "rebinX"           : 1,
        "rebinY"           : None,
        "ratioType"        : "errorScale",
        "ratioErrorOptions": {"numeratorStatSyst": False},
        "ratioYlabel"      : "Data/MC",
        "ratio"            : opts.ratio, 
        "stackMCHistograms": True,
        "ratioInvert"      : False, 
        "addMCUncertainty" : True, 
        "addLuminosityText": True,
        "addCmText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": yMin, "ymaxfactor": yMaxF},
        #"opts2"            : {"ymin": 0.0, "ymax": 2.0},
        "opts2"            : {"ymin": 0.59, "ymax": 1.41},
        "log"              : logY,
        "moveLegend"       : _moveLegend,
        }

    kwargs = copy.deepcopy(_kwargs)
    
    if "pt" in h.lower():
        units            = "GeV/c"
        kwargs["ylabel"] = _yLabel + units

    if "eta" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": yMin, "ymaxfactor": yMaxF}

    if "DeltaEta" in h:
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["opts"]   = {"xmax": +6.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "BDT" in h:
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.4, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": +0.4, "ymin": yMin, "ymaxfactor": yMaxF}

    if "DeltaR" in h or "DeltaY" in h or "DR" in h:
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["opts"]   = {"xmax": +8.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if h == "TrijetBDT_Mass": # before BDT cut
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "m_{jjb}^{cand} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +500.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if h == "TopCandMass": #after all cuts
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "m_{jjb}^{BDT} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +500.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if h == "BDTmultiplicity":
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "top multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +40.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 2.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if h == "BDTGresponse":
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "BDT discriminant"
        kwargs["ylabel"] = "Events / %.1f "
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +1.0, "ymin": yMin, "ymax": 3e5} #yMaxF}
        kwargs["cutBox"] = {"cutValue": 0.9, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.5, "dh": 0.0}

    if h == "EventTrijetPt": #before cuts (fixme: why filled for data? used TopMatched)
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "p_{T,jjb}^{cand} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        #kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymax": 3e5} #yMaxF}

    if h == "EventTrijetPt2T": #before cuts (fixme: why filled for data? used TopMatched)
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "p_{T,jjb}^{cand} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        
    if h == "EventTrijetPt_BDT": # both pass, matched (fixme: filled for data?)
        units            = "GeV/c"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "p_{T,jjb}^{BDT} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        
    if h == "EventTrijetPt2T_BDT": #both pass, both matched (fixme: filled for data?)
        units            = "GeV/c"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "p_{T,jjb}^{BDT} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if h == "JetMultiplicity":
        kwargs["xlabel"] = "jets multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +15.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 7.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.0, "dh": 0.1}

    if h == "LdgBjetPt":
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        #kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
   
    if "dgTrijetBJetBDisc" in h: #after cuts
        kwargs["rebinX"] = 2
        #kwargs["xlabel"] = "CSVv2 discriminant"
        kwargs["xlabel"] = "b-jet discriminant"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.5, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.0, "dh": 0.1}
 
    if "dgTrijetBJetPt" in h:
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +600.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "dgTrijetBJetEta" in h:
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "#eta"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": yMin, "ymaxfactor": yMaxF}

    if "dgTrijetDiJetEta" in h:
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "#eta"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": yMin, "ymaxfactor": yMaxF}
        
    if "dgTrijetDiJetMass" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "m_{jj}^{BDT} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +300.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 80.385, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "dgTrijetDiJetPt" in h:
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T,jj}^{BDT} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +800.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "dgTrijetJet1BDisc" in h or "dgTrijetJet2BDisc" in h:
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "b-jet discriminant"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.5, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.00, "dh": 0.1}

    if  "dgTrijetJet1Eta" in h or "ldgTrijetJet2Eta" in h:
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "#eta"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": yMin, "ymaxfactor": yMaxF}

    if  "ldgTrijetJet1Pt" in h or "ldgTrijetJet2Pt" in h:
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +600.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "dgTrijetMass" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "m_{jjb}^{ldg} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +400.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "AfterStandardSelections" in h:
            #kwargs["opts"]   = {"xmin": 0.0, "xmax": +1500.0, "ymin": yMin, "ymaxfactor": yMaxF}
            kwargs["opts"]   = {"xmin": 50, "xmax": +600, "ymin": yMin, "ymaxfactor": yMaxF}
        if "AfterAllSelections" in h:
            kwargs["opts"]   = {"xmin": 175-80, "xmax": +175+100, "ymin": yMin, "ymaxfactor": yMaxF}

    if "dgTrijetDijetMass" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "m_{jj} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +400.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 80.385, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "AfterStandardSelections" in h:
            kwargs["opts"]   = {"xmin": 0, "xmax": +600, "ymin": yMin, "ymaxfactor": yMaxF}
        if "AfterAllSelections" in h:
            kwargs["opts"]   = {"xmin": 0, "xmax": +500, "ymin": yMin, "ymaxfactor": yMaxF}

    if "ldgTrijetPt" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T,jjb}^{ldg} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        #kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymax": 3e5} #yMaxF}

    if "dgTrijetTopMassWMassRatio" in h:
        units            = ""
        kwargs["rebinX"] = 1
        kwargs["ylabel"] = "Events / %.2f"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +5.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": (173.21/80.385), "fillColor": 16, "box": False, "line": True, "greaterThan": True} 
        if "AfterStandardSelections" in h:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +10.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if h == "TetrajetBJetBDisc":
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "b-jet discriminant"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.5, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.00, "dh": 0.1}

    if  h == "TetrajetBJetEta":
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "#eta_{b_{free}}"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": yMin, "ymaxfactor": yMaxF}

    if h == "TetrajetBJetPt" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T, b_{free}} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if h == "TetrajetMass" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 5
        kwargs["xlabel"] = "m_{jjbb} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": opts.signalMass, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "counters" in opts.folder:
        ROOT.gStyle.SetLabelSize(16.0, "X")
        kwargs["moveLegend"] = {"dx": -0.08, "dy": 0.0, "dh": 0.1}
        kwargs["opts2"]      = {"ymin": 0.6, "ymax": 2.0-0.6}
        # kwargs["moveLegend"] = {"dx": -0.52, "dy": -0.55, "dh": 0.0}

    if h == "counter":
        xMin = 15.0
        xMax = 21.0
        kwargs["opts"]   = {"xmin": xMin, "ymin": 1e0, "ymax": 1e8}
        # kwargs["cutBox"] = {"cutValue": xMin+2, "fillColor": 16, "box": False, "line": False, "greaterThan": True} #indicate btag SF

    if "IsolPt" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +400.0, "ymin": yMin, "ymaxfactor": yMaxF}
        
    if "RelIsoAfter" in h or "RelIsoPassed" in h:
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +0.25, "ymin": yMin, "ymaxfactor": yMaxF}

    if "IsolMiniIso" in h or "MiniIso" in h:
        kwargs["ylabel"] = "Events / %.0f "
        kwargs["xlabel"] = "mini relative isolation"
        #kwargs["opts"]   = {"xmin": 0.0, "xmax": +10.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 0.4, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "after" in h.lower() or "passed" in h.lower():
            kwargs["ylabel"] = "Events / %.2f "
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "vtx" in h.lower():
        kwargs["xlabel"] = "PV multiplicity"
        kwargs["cutBox"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "electronPt" in h:
        units            = "GeV/c"
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units

    if h == "tauNpassed":
        units            = "GeV/c"
        kwargs["xlabel"] = "#tau-jet multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 7.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": False}

    if "HT" in h or "JT" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        if opts.folder == "topologySelection_":
            kwargs["rebinX"] = 1
        else:
            kwargs["rebinX"] = 5
        units = "GeV"
        if "HT" in h:
            kwargs["xlabel"] = "H_{T} (%s)" % units
        else:
            kwargs["xlabel"] = "J_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "ForDataDrivenCtrlPlots" in opts.folder:
            kwargs["cutBox"] = {"cutValue": 900.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3500.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "MHT" in h:
        kwargs["rebinX"] = 2
        units            = "GeV"
        kwargs["xlabel"] = "MHT (%s)" % units
        kwargs["ylabel"] = _yLabel + units

    regex = re.compile('selectedJets.*JetPt')
    if(regex.search(h)):
        ROOT.gStyle.SetNdivisions(8, "X")
        kwargs["rebinX"] = 1
        units            = "GeV"
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    regex = re.compile('selectedBJets.*JetPt')
    if(regex.search(h)):
        #ROOT.gStyle.SetNdivisions(8, "X")
        kwargs["rebinX"] = 1
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    regex = re.compile('selectedBJets.*BDisc')
    if(regex.search(h)):
        ROOT.gStyle.SetNdivisions(8, "X")
        kwargs["xlabel"] = "b-jet discriminant"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.5, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.00, "dh": 0.1}

    if "btagdiscriminator" in h.lower():
        kwargs["rebinX"] = 1
        #kwargs["xlabel"] = "CSVv2 discriminant"
        kwargs["xlabel"] = "b-jet discriminant"
        kwargs["ylabel"] = "Events / %.2f "
        if "_" in h.lower():
            ROOT.gStyle.SetNdivisions(8, "X")
            kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.5, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        else:
            #ROOT.gStyle.SetNdivisions(8, "X")
            kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.00, "dh": 0.1}

    if h == "btagSF":
        kwargs["xlabel"] = "b-jet SF"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 3.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "met" in h.lower():
        units            = "GeV"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "E_{T}^{miss} (%s)" % (units)
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 800.0, "ymin": yMin, "ymaxfactor": yMaxF}
        if "METFilter" in h:
            kwargs["rebinX"] = 1
            kwargs["xlabel"] = ""
            kwargs["ylabel"] = "Events / %.0f "
            kwargs["opts"]   = {"xmin": 0.0, "ymin": yMin, "ymaxfactor": yMaxF}
        if "Selections" in h:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 400.0, "ymin": yMin, "ymaxfactor": yMaxF}
            
        if "metphi" in h.lower():
            units            = "rads"
            kwargs["xlabel"] = "E_{T}^{miss} #phi (%s)" % (units)
            kwargs["ylabel"] = _yLabel + units
            kwargs["opts"]   = {"xmin": -3.2, "xmax": 3.2, "ymin": yMin, "ymaxfactor": yMaxF}

    if "AlphaT" in h:
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 1.2, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "planarity" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "

    if "cparameter" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["moveLegend"] = {"dx": -0.52, "dy": -0.0, "dh": 0.0}

    if "centrality" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "

    if "centrality" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "

    if "circularity" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "

    if "parameter" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "

    if "foxwolfram" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "sphericity" in h.lower():
        kwargs["ylabel"] = "Events / %.2f "

    if "y23" in h:
        kwargs["ylabel"] = "Events / %.2f "

    if "LdgTetrajetMass_After" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 10
        kwargs["xlabel"] = "m_{jjbb} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        if "AllSelections" in h:
            ROOT.gStyle.SetNdivisions(10, "X")
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3100.0, "ymin": yMin, "ymaxfactor": yMaxF}
        else:
            ROOT.gStyle.SetNdivisions(7, "X")
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +4000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": opts.signalMass, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "LdgTrijetBjetPt" in h:
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "AllSelections" in h:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +600.0, "ymin": yMin, "ymaxfactor": yMaxF}
        else:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "MHT" in h:
        units            = "GeV"
        kwargs["xlabel"] = "MHT (%s)" % (units)
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 400.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "NBjets" in h:
        kwargs["xlabel"] = "b-jet multiplicity"
        kwargs["opts"]   = {"xmin": 2.0, "xmax": 10.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 3, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "Njets" in h:
        kwargs["xlabel"] = "jet multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 18.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 7, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "Selections" in h:
            kwargs["opts"]   = {"xmin": 6.0, "xmax": 18.0, "ymin": yMin, "ymaxfactor": yMaxF}
            #kwargs["moveLegend"] = {"dx": -0.52, "dy": -0.0, "dh": 0.0}

    if "NVertices" in h:
        kwargs["rebinX"] = vtxBins
        binWmin, binWmax = GetBinWidthMinMax(vtxBins)
        kwargs["ylabel"] = "Events / %.0f-%.0f" % (binWmin, binWmax)
        kwargs["xlabel"] = "PV multiplicity"
        kwargs["cutBox"] = {"cutValue": 20.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "SubldgTrijetBjetPt" in h:
        if "AllSelections" in h:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 500.0, "ymin": yMin, "ymaxfactor": yMaxF}

    return kwargs
    

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

def getHistos(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]

def DataMCHistograms(datasetsMgr, histoName):
    Verbose("Plotting Data-MC Histograms")

    # Skip 2-D plots
    skipStrings = []
    if opts.folder == "topbdtSelection_":
        skipStrings = ["_Vs_", "Vs", "Matched", "MCtruth", "TopQuark", 
                       "RealSelected", "DeltaMVAgt1", "SelectedTop", 
                       "LdgTrijetFake", "LdgTrijetFakeJJB", "TrijetFake",
                       "FakeInTopDir", "LdgTrijetFakeJJB_BDT", "LdgTrijetFake_BDT"]

    if opts.folder == "counters":
        skipStrings = ["weighted"]
    if opts.folder == "eSelection_Veto":
        skipStrings = ["Resolution"]
    if opts.folder == "muSelection_Veto":
        skipStrings = ["Resolution"]
    if opts.folder == "tauSelection_Veto":
        skipStrings = ["riggerMatch", "NprongsMatrix", "Resolution"]
    if opts.folder == "PUDependency":
        skipStrings = ["WithProbabilisticBtag", "AngularCuts", "AntiIsolatedTau", "NvtxTau"]
    if opts.folder == "jetSelection_":
        skipStrings = ["JetMatching"]
    if opts.folder == "bjetSelection_":
        skipStrings = ["MatchDeltaR", "btagSFRelUncert", "_dEta", "_dPhi", "_dPt", "_dR"]
    if opts.folder == "metSelection_":
        skipStrings = [""]
    if opts.folder == "topologySelection_":
        skipStrings = ["_Vs_"]
    if "ForDataDrivenCtrlPlots" in opts.folder:
        skipStrings = ["_Vs_", "JetEtaPhi", "MinDeltaPhiJet", "MaxDeltaPhiJet", "MinDeltaRJet"]

    # Skip histograms if they contain a given string
    for keyword in skipStrings:
        if keyword in histoName:
            return

    # Get Histogram name and its kwargs
    saveName = histoName.rsplit("/")[-1] # histoName.replace("/", "_")
    kwargs_  = GetHistoKwargs(saveName, opts)

    # Create the plotting object
    p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])

    # Apply style
    if opts.signalMass != 0:
        p.histoMgr.forHisto(opts.signal, styles.getSignalStyleHToTB_M(opts.signalMass))

    if "QCD" in datasetsMgr.getAllDatasetNames():
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

    # Replace bin labels
    if "counter" in opts.folder and "counter" in histoName.split("/")[-1]:
        # p.getFrame().GetXaxis().LabelsOption("v") #vertical orientation of bin labels
        replaceBinLabels(p, saveName)
        #pass

    # Save the plots in custom list of saveFormats
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode, opts.folder), [".png", ".pdf"] )
    return

def replaceBinLabels(p, histoName):
    '''
    https://root.cern.ch/doc/master/classTAttText.html#T5
    '''
    myBinList = []
    if histoName == "counter" or histoName == "weighted/counter":
        # myBinList = ["#geq 7 jets", "#geq 3 b-jets", "b-jets SF", "QGLR", "#geq 2 tops", "fat-jet veto", "All"]
        myBinList = ["#geq 7 jets", "#geq 3 b-jets", "b-jets SF", "#geq 2 tops", "fat-jet veto", "All"]
    elif "bjet" in histoName:
        myBinList = ["All", "#eta", "p_{T}", "CSVv2 (M)", "Trg Match", "#geq 3"]
    elif "jet" in histoName:
        myBinList = ["All", "jet ID", "PU ID", "#tau match", "#eta", "p_{T}", "#geq 7", "H_{T}", "J_{T}", "MHT"]
    else:
        pass
    for i in range(0, len(myBinList)):
        p.getFrame().GetXaxis().SetBinLabel(i+1, myBinList[i])
        #p.getFrame().GetXaxis().GetBinLabel(i+1).SetTextAngle(90) #not correct
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))
    saveName = saveName.replace(" ", "_")
    saveName = saveName.replace(")", "")
    saveName = saveName.replace("(", "")

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
    GRIDX        = False
    GRIDY        = False
    OPTMODE      = None
    BATCHMODE    = True
    INTLUMI      = -1.0
    SIGNALMASS   = 500
    MERGEEWK     = False
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    RATIO        = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug' 
    FOLDER       = "topbdtSelection_" #jetSelection_

    
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

    parser.add_option("--ratio", dest="ratio", action="store_true", default=RATIO,
                      help="Enable ratio pad for Data/Bkg comparison [default: %s]" % RATIO)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--mergeEWK", dest="mergeEWK", action="store_true", default=MERGEEWK, 
                      help="Merge all EWK samples into a single sample called \"EWK\" [default: %s]" % MERGEEWK)

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX, 
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY, 
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--signalMass", dest="signalMass", type=int, default=SIGNALMASS, 
                     help="Mass value of signal to use [default: %s]" % SIGNALMASS)

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
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="DataMC")

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 650, 800, 1000, 2000, 3000]
    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()
    else:
        #opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%i_ext1" % opts.signalMass
        opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass

    # Sanity check
#     allowedFolders = ["counters", "counters/weighted", "PUDependency", "Weighting", 
#                       "eSelection_Veto", "muSelection_Veto", "tauSelection_Veto",
#                       "ForDataDrivenCtrlPlotsEWKFakeB", "ForDataDrivenCtrlPlotsEWKGenuineB",
#                       "QuarkGluonLikelihoodRatio_", "QGLRSelection_", 
#                       "jetSelection_", "bjetSelection_", "metSelection_", "fatjetSelection_Veto",
#                       "topologySelection_", "topbdtSelection_", "ForDataDrivenCtrlPlots"]
# 
#     if opts.folder not in allowedFolders:
#         Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
#         for m in allowedFolders:
#             Print(m, False)
#         sys.exit()


    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotDataMC_ControlPlots.py: Press any key to quit ROOT ...")
