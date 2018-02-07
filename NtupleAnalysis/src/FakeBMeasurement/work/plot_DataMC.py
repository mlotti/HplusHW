#!/usr/bin/env python
'''
DESCRIPTION:
Script that plots Data/MC for all histograms under a given folder (passsed as option to the script)
Good for sanity checks for key points in the cut-flow


USAGE:
./plot_DataMC.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plot_DataMC.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_TopCut10_171012_011451 --folder jetSelection_ --url
./plot_DataMC.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDTm0p80_AllSelections_BDT0p90_RandomSort_171120_100657 --url --folder ForFakeBMeasurement --ratio
./plot_DataMC.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDTm0p80_AllSelections_BDT0p90_RandomSort_171120_100657 --url --folder ForFakeBMeasurementEWKGenuineB --onlyMC
./plot_DataMC.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDTm0p80_AllSelections_BDT0p90_RandomSort_171120_100657 --url --folder ForFakeBMeasurementEWKFakeB --onlyMC --nostack
./plot_DataMC.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDTm0p80_AllSelections_BDT0p90_RandomSort_171120_100657 --url --mergeEWK --nostack --onlyMC

LAST USED:
./plot_DataMC.py -m FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p50to085_180129_133455/ --folder counters/weighted --url --ratio

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
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

def rchop(myString, endString):
  if myString.endswith(endString):
    return myString[:-len(endString)]
  return myString

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

def GetListOfEwkDatasets(datasetsMgr):
    Verbose("Getting list of EWK datasets")
    if "noTop" in datasetsMgr.getAllDatasetNames():
        return  ["TT", "noTop", "SingleTop", "ttX"]
    else: # TopSelectionBDT
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
        datasetsToRemove = ["QCD-b"]#, "QCD_HT50to100", "QCD_HT100to200"]#, "QCD_HT200to300"]#, "QCD_HT300to500"]
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0) # ATLAS 13 TeV H->tb exclusion limits
                if d.getName() != opts.signal:
                    datasetsToRemove.append(d.getName())

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Custom Filtering of datasets 
        for i, d in enumerate(datasetsToRemove, 0):
            msg = "Removing dataset %s" % d
            Print(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
            datasetsMgr.remove(filter(lambda name: d in name, datasetsMgr.getAllDatasetNames()))
        if opts.verbose:
            datasetsMgr.PrintInfo()

        # ZJets and DYJets overlap
        if "ZJetsToQQ_HT600toInf" in datasetsMgr.getAllDatasetNames() and "DYJetsToQQ_HT180" in datasetsMgr.getAllDatasetNames():
            Print("Cannot use both ZJetsToQQ and DYJetsToQQ due to duplicate events? Investigate. Removing ZJetsToQQ datasets for now ..", True)
            datasetsMgr.remove(filter(lambda name: "ZJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        
        # Get Luminosity
        intLumi = datasetsMgr.getDataset("Data").getLuminosity()

        # Re-order datasets (different for inverted than default=baseline)
        newOrder = []
        # For-loop: All MC datasets
        for d in datasetsMgr.getMCDatasets():
            newOrder.append(d.getName())

        # Move signal to top
        if opts.signal in newOrder:
            s = newOrder.pop( newOrder.index(opts.signal) )
            newOrder.insert(0, s)

        # Add Data to list of samples!
        if not opts.onlyMC:
            newOrder.insert(0, "Data")
            
        # Apply new dataset order!
        datasetsMgr.selectAndReorder(newOrder)
        
        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets(datasetsMgr))
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
        histoPaths1 = [os.path.join(folder, h) for h in histoList]
        histoPaths2 = [h for h in histoPaths1 if "jet" not in h.lower()]
        nHistos     = len(histoPaths2)

        # For-loop: All histograms
        for i, h in enumerate(histoPaths2, 1):
            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i, "/", "%s:" % (nHistos), h)
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)
            PlotHistograms(datasetsMgr, h, intLumi)

    savePath = opts.saveDir
    if opts.url:
        savePath = opts.saveDir.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + savePath + ShellStyles.NormalStyle()), True)
    return

def GetHistoKwargs(h, opts):
    _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": 0.1}    
    logY    = True
    _yLabel = "Events / %.0f "
    yMin    = 1e0
    if logY:
        yMaxF = 10
    else:
        yMaxF = 1.2
        
    _kwargs = {
        "ylabel"           : _yLabel,
        "rebinX"           : 1,
        "rebinY"           : None,
        "ratioYlabel"      : "Data/Bkg. ",
        "ratio"            : opts.ratio,
        "ratioCreateLegend": True,
        "ratioType"        : "errorScale",
        "ratioErrorOptions": {"numeratorStatSyst": False},
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.05},
        "stackMCHistograms": not opts.nostack,
        "ratioInvert"      : False, 
        "addMCUncertainty" : True, 
        "addLuminosityText": True,
        "addCmsText"       : True,
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

    if "mvamax" in h.lower():
        units            = ""
        kwargs["ylabel"] = "Events / %.2f " + units
        kwargs["xlabel"] = "MVA discriminant"
        kwargs["cutBox"] = {"cutValue": 0.9, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -1.0, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.49}

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
        kwargs["cutBox"] = {"cutValue": 7.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["moveLegend"] = {"dx": -0.49, "dy": -0.0, "dh": 0.0}

    if h == "LdgBjetPt":
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        #kwargs["opts"]   = {"xmin": 0.0, "xmax": +1000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
   
    if "dgTrijetBJetBDisc" in h: #after cuts
        kwargs["rebinX"] = 2
        #kwargs["xlabel"] = "CSVv2 discriminant"
        kwargs["xlabel"] = "b-jet discriminant"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.8, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.1, "dy": -0.55, "dh": 0.0}
 
    if "dgTrijetBJetPt" in h:
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
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
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.8, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.1, "dy": -0.55, "dh": 0.0}

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
        kwargs["cutBox"] = {"cutValue": 40.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +600.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "dgTrijetMass" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "m_{jjb}^{ldg} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +400.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "AfterStandardSelections" in h:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1500.0, "ymin": yMin, "ymaxfactor": yMaxF}

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
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.8, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.1, "dy": -0.55, "dh": 0.0}

    if  h == "TetrajetBJetEta":
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "#eta"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": yMin, "ymaxfactor": yMaxF}

    if h == "TetrajetBJetPt" in h:
        ROOT.gStyle.SetNdivisions(8, "X")
        units            = "GeV/c"
        kwargs["rebinX"] = 1
        kwargs["xlabel"] = "p_{T,jjbb} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["cutBox"] = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if h == "TetrajetMass" in h:
        units            = "GeV/c^{2}"
        kwargs["rebinX"] = 2
        kwargs["xlabel"] = "m_{jjbb} (%s)" % units
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": +3000.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": opts.signalMass, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "counters" in opts.folder:
        ROOT.gStyle.SetLabelSize(16.0, "X")        
        kwargs["moveLegend"] = {"dx": -500.0, "dy": -500.0, "dh": -500.0}
        #if opts.ratio:
        #    kwargs["moveLegend"] = {"dx": -0.52, "dy": -0.55, "dh": 0.0}
        #else:
        #    kwargs["moveLegend"] = {"dx": -0.52, "dy": -0.45, "dh": 0.0}
            
    if h == "counter":
        ROOT.gStyle.SetLabelSize(16.0, "X")
        xMin = 17  # 15 = jets selection, 16 = bjets selection, 17 = baseline: bjets selection, 18 = bjets SF
        xMax = 29
        kwargs["opts"] = {"xmin": xMin, "ymin": 1e0, "ymax": 5e6}#"ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -500.0, "dy": -500.0, "dh": -500.0}

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

    if "vtx" in h.lower():
        kwargs["xlabel"] = "PV multiplicity"
        kwargs["cutBox"] = {"cutValue": 1.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}

    if "electronPt" in h:
        units            = "GeV/c"
        kwargs["xlabel"] = "p_{T} (%s)" % units
        kwargs["ylabel"] = _yLabel + units

    if h == "tauNpassed":
        units            = "GeV/c"
        kwargs["xlabel"] = "#tau-jet multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 8.0, "ymin": yMin, "ymaxfactor": yMaxF}

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
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +3500.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "MHT" in h:
        kwargs["rebinX"] = 1
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
        kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        kwargs["opts"]   = {"xmin": 0.8, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.1, "dy": -0.55, "dh": 0.0}

    if "btagdiscriminator" in h.lower():
        kwargs["rebinX"] = 1
        #kwargs["xlabel"] = "CSVv2 discriminant"
        kwargs["xlabel"] = "b-jet discriminant"
        kwargs["ylabel"] = "Events / %.2f "
        if "_" in h.lower():
            ROOT.gStyle.SetNdivisions(8, "X")
            kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.8, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        else:
            #ROOT.gStyle.SetNdivisions(8, "X")
            kwargs["cutBox"] = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["moveLegend"] = {"dx": -0.1, "dy": -0.55, "dh": 0.0}

    if h == "btagSF":
        kwargs["xlabel"] = "b-jet SF"
        kwargs["ylabel"] = "Events / %.2f "
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 3.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "met" in h.lower():
        units            = "GeV"
        kwargs["xlabel"] = "E_{T}^{miss} (%s)" % (units)
        kwargs["ylabel"] = _yLabel + units
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 800.0, "ymin": yMin, "ymaxfactor": yMaxF}
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
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 12.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 3, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

    if "Njets" in h:
        kwargs["xlabel"] = "jet multiplicity"
        kwargs["opts"]   = {"xmin": 0.0, "xmax": 18.0, "ymin": yMin, "ymaxfactor": yMaxF}
        kwargs["cutBox"] = {"cutValue": 7, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "Selections" in h:
            kwargs["moveLegend"] = {"dx": -0.52, "dy": -0.0, "dh": 0.0}

    if "NVertices" in h:
        kwargs["xlabel"] = "PV multiplicity"
        kwargs["cutBox"] = {"cutValue": 1.0, "fillColor": 16, "box": True, "line": True, "greaterThan": True}
        if "AllSelections" in h:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 80.0, "ymin": yMin, "ymaxfactor": yMaxF}

    if "SubldgTrijetBjetPt" in h:
        if "AllSelections" in h:
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 500.0, "ymin": yMin, "ymaxfactor": yMaxF}

    # alex

    return kwargs
    

def getHistos(datasetsMgr, histoName):

    h1 = datasetsMgr.getDataset("Data").getDatasetRootHisto(histoName)
    h1.setName("Data")

    h2 = datasetsMgr.getDataset("EWK").getDatasetRootHisto(histoName)
    h2.setName("EWK")
    return [h1, h2]


def getHisto(datasetsMgr, histoName, dataset):
    h = datasetsMgr.getDataset(dataset).getDatasetRootHisto(histoName)
    return h


def PlotHistograms(datasetsMgr, histoName, intLumi):
    Verbose("Plotting Data-MC Histograms")

    # Skip 2-D plots
    skipStrings = []
    if "topbdtSelection_" in opts.folder:
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
        skipStrings = ["_Vs_", "JetEtaPhi", "MinDeltaPhiJet", "MaxDeltaPhiJet", "MinDeltaRJet", "SubldgTetrajet"]

    # Skip histograms if they contain a given string
    for keyword in skipStrings:
        if keyword in histoName:
            return

    # Get Histogram name and its kwargs
    saveName = histoName.rsplit("/")[-1]
    kwargs_  = GetHistoKwargs(saveName, opts)

    # Create the plotting object
    if opts.onlyMC:        
        if 1:
            p = plots.MCPlot(datasetsMgr, histoName, saveFormats=[], normalizeToLumi=intLumi)
        else:
            p = plots.MCPlot(datasetsMgr, histoName, saveFormats=[], normalizeToOne=True)
    else:
        p = plots.DataMCPlot(datasetsMgr, histoName, saveFormats=[])

    # Apply style
    if opts.signalMass != 0:
        p.histoMgr.forHisto(opts.signal, styles.getSignalStyleHToTB_M(opts.signalMass))

    # p.histoMgr.forHisto(opts.signalMass, styles.getSignalStyleHToTB())
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
    if "counter" in opts.folder:
        replaceBinLabels(p, histoName)

    # Save the plots in custom list of saveFormats
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.folder, opts.optMode), [".png", ".pdf"] )
    return

def replaceBinLabels(p, histoName):
    '''
    https://root.cern.ch/doc/master/classTAttText.html#T5
    '''
    #if "counter" not in histoName:
    if histoName != "counters/weighted/counter":
        return

    myBinDict = {
        "passed jet selection ()"         : "#geq 7j",
        "passed b-jet selection ()"       : "#geq 3b",
        "Baseline: passed b-jet selection": "SR: #geq 3b",
        "Baseline: b tag SF"              : "SR: b-SF",
        "passed MET selection (Baseline)" : "SR: MET",
        "passed top selection (Baseline)" : "SR: Top",
        "Baseline: selected events"       : "SR: All",
        "Baseline: selected CR events"    : "CR1: All",
        "Inverted: passed b-jet selection": "VR: =2b",
        "Inverted: b tag SF"              : "VR: b-SF",
        "passed MET selection (Inverted)" : "VR: MET",
        "passed top selection (Inverted)" : "VR: Top",
        "Inverted: selected events"       : "VR: All",
        "Inverted: selected CR events"    : "CR2: All",
        }

    nBinsX = p.getFrame().GetXaxis().GetNbins()
    p.getFrame().GetXaxis().LabelsOption("v")
    for i in range(0, nBinsX+1):
        oldLabel = p.getFrame().GetXaxis().GetBinLabel(i)
        if oldLabel in myBinDict.keys():
            newLabel = myBinDict[oldLabel]
            p.getFrame().GetXaxis().SetBinLabel(i, newLabel)
            Verbose("%s -> %s" % (oldLabel, newLabel), False)
        else:
            Verbose("Could not find new label for bin %i and label \"%s\"" % (i, oldLabel), True)
    return

def SavePlot(plot, plotName, saveDir, saveFormats = [".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_").replace(" ", "").replace("(", "").replace(")", "") )

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if opts.url:
            Verbose(saveNameURL, i==0)
        else:
            Verbose(saveName + ext, i==0)
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
    GRIDX        = False
    GRIDY        = False
    OPTMODE      = None
    BATCHMODE    = True
    PRECISION    = 3
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    SIGNALMASS   = 500
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = "/publicweb/a/aattikis/" #FakeBMeasurement/DataMC/"
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug' 
    FOLDER       = "ForDataDrivenCtrlPlots" #"FailedBJetGenuineB" #jetSelection_
    ONLYMC       = False
    RATIO        = False
    NOSTACK      = False

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

    parser.add_option("--histoLevel", dest="histoLevel", action="store", default = HISTOLEVEL,
                      help="Histogram ambient level (default: %s)" % (HISTOLEVEL))

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in mcrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--folder", dest="folder", type="string", default = FOLDER,
                      help="ROOT file folder under which all histograms to be plotted are located [default: %s]" % (FOLDER) )

    parser.add_option("--onlyMC", dest="onlyMC", action="store_true", default = ONLYMC,
                      help="Only draw MC datasets, no data: [default: %s]" % (ONLYMC) )

    parser.add_option("--ratio", dest="ratio", action="store_true", default = RATIO,
                      help="Draw ratio canvas for Data/MC curves? [default: %s]" % (RATIO) )

    parser.add_option("--nostack", dest="nostack", action="store_true", default = NOSTACK,
                      help="Do not stack MC histograms [default: %s]" % (NOSTACK) )

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
    else:
        mcrabDir = rchop(opts.mcrab, "/")
        if len(mcrabDir.split("/")) > 1:
            mcrabDir = mcrabDir.split("/")[-1]
        opts.saveDir += mcrabDir + "/DataMC"


    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()
    else:
        opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass

    # Sanity check
    allowedFolders = ["counters", "counters/weighted", "Weighting", "ForDataDrivenCtrlPlots", 
                      "ForDataDrivenCtrlPlotsEWKFakeB", "ForDataDrivenCtrlPlotsEWKGenuineB", "PUDependency", 
                      "Selection_Veto", "muSelection_Veto", "tauSelection_Veto", 
                      "jetSelection_", "bjetSelection_", "metSelection_Baseline",
                      "topologySelection_Baseline", "topbdtSelection_Baseline", 
                      "topbdtSelectionTH2_Baseline", "metSelection_Inverted", 
                      "topologySelection_Inverted", "topbdtSelection_Inverted",
                      "topbdtSelectionTH2_Inverted", "ForFakeBNormalization", 
                      "ForFakeBNormalizationEWKFakeB", "ForFakeBNormalizationEWKGenuineB",
                      "FailedBJet", "FailedBJetFakeB", "FailedBJetGenuineB", "ForFakeBMeasurement", 
                      "ForFakeBMeasurementEWKFakeB", "ForFakeBMeasurementEWKGenuineB"]


    if opts.folder not in allowedFolders:
        Print("Invalid folder \"%s\"! Please select one of the following:" % (opts.folder), True)
        for m in allowedFolders:
            Print(m, False)
        sys.exit()
    
    # Overwrite if certain strings found in folder name
    if 0:
        opts.onlyMC = "EWKFakeB" in opts.folder
        opts.onlyMC = "EWKGenuineB" in opts.folder

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_DataMC.py: Press any key to quit ROOT ...")
