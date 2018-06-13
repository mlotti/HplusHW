#!/usr/bin/env python
'''
  DESCRIPTION:
  
  This script calculates the genuine tt efficiency. 
  Steps before running this script:
  
  1. Produce the normalization factors for QCD and TT with getNormalization.py 
  2. Get QCD+EWK+ST misidentification rate and produce the SF_{CR2} json with script getMisIdRateCR2.py
  3. Run the analyzer on QCD+EWK+ST events with the SF_{CR2} form step 2.
  4. Get the Fake TT misidentification rate and produce the SF_{CR1} json. with scipt getMisIdRateCR1.py
  5. Run the analyzer on TT events with the SF_{CR1} from step 1.
  6. Ready to calculate the Genuine TT efficiencies of the Top BDT tagger.
  
  PHASE SPACE:
  
         Mini-Isolation
              ^
              |
              |--------------|--------------|--------------|
        >=0.1 |      CR2     |      -       |      VR      |
              |--------------|              |--------------|
         <0.1 |      CR1     |      -       |      SR      |
              |--------------|--------------|--------------|----> MET
              |              20             50             |

  Genuine TT in Data:
  
  Numerator:    [ Data_{SR} - F1*QCD_{SR}*SF_{CR2} - EWK*SF_{CR2} - ST*SF_{CR2} - F2*FakeTT_{SR}*SF_{CR1} ] passing BDT
  Denominator:  [ Data_{SR} - F1*QCD_{SR} - EWK*SF_{CR2} - ST*SF_{CR2} - F2*FakeT_{SR}]
  
  Genuine TT in MC:
  
  Numerator:    [ TT-SR-Genuine ] passing BDT
  Denominator:  [ TT-SR-Genuine ]
  
  SF = Efficiency in Data / Efficiency in MC
  
  
  USAGE:
  ./getEfficiencies.py -num <pseudo_nummcrab_directory> -den <pseudo_dencrab_directory> [opts]
  
  LAST USED:

  (1) ./getGenuineEfficiency.py --noSF SystTopBDT_180528_151309_MET30_MuIso0p1_InvMET30_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180602_113334_MET30_MuIso0p2_InvMET30_InvMuIso0p2_withCR1SF \
  --withCR2SF SystTopBDT_180529_083852_MET30_MuIso0p2_InvMET30_InvMuIso0p2_withCR2SF --url -e "TTW"

  (2) ./getGenuineEfficiency.py --noSF SystTopBDT_180528_151533_MET30_MuIso0p1_InvMET30_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180602_114148_MET30_MuIso0p1_InvMET30_InvMuIso0p2_withCR1SF \
  --withCR2SF SystTopBDT_180529_084257_MET30_MuIso0p1_InvMET30_InvMuIso0p2_withCR2SF --url -e "TTW"

  (3) ./getGenuineEfficiency.py --noSF SystTopBDT_180528_152141_MET50_MuIso0p1_InvMET20_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180602_114435_MET50_MuIso0p1_InvMET20_InvMuIso0p2_withCR1SF \
  --withCR2SF SystTopBDT_180529_084610_MET50_MuIso0p1_InvMET20_InvMuIso0p2_withCR2SF --url -e "TTW"

  (4) ./getGenuineEfficiency.py --noSF SystTopBDT_180528_152310_MET40_MuIso0p1_InvMET30_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180602_114641_MET40_MuIso0p1_InvMET30_InvMuIso0p2_withCR1SF \
  --withCR2SF SystTopBDT_180529_084900_MET40_MuIso0p1_InvMET30_InvMuIso0p2_withCR2SF --url -e "TTW"

  (5) ./getGenuineEfficiency.py --noSF SystTopBDT_180528_152540_MET30_MuIso0p1_InvMET15_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180602_114840_MET30_MuIso0p1_InvMET15_InvMuIso0p2_withCR1SF \
  --withCR2SF SystTopBDT_180529_085334_MET30_MuIso0p1_InvMET15_InvMuIso0p2_withCR2SF --url -e "TTW"
  
  (6) ./getGenuineEfficiency.py --noSF SystTopBDT_180528_152944_MET30_MuIso0p2_InvMET20_InvMuIso0p4_noSF --withCR1SF SystTopBDT_180602_115034_MET30_MuIso0p2_InvMET20_InvMuIso0p4_withCR1SF \
  --withCR2SF SystTopBDT_180529_085656_MET30_MuIso0p2_InvMET20_InvMuIso0p4_withCR2SF --url -e "TTW"

  (7) ./getGenuineEfficiency.py --noSF SystTopBDT_180529_093052_MET50_MuIso0p1_InvMET20_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180602_115353_MET50_MuIso0p1_InvMET20_InvMuIso0p1_withCR1SF \
  --withCR2SF SystTopBDT_180530_075514_MET50_MuIso0p1_InvMET20_InvMuIso0p1_withCR2SF --url -e "TTW"

  (8) ./getGenuineEfficiency.py --noSF SystTopBDT_180529_165537_MET30_MuIso0p1_InvMET30_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180602_115622_MET30_MuIso0p1_InvMET30_InvMuIso0p1_withCR1SF \
  --withCR2SF SystTopBDT_180530_075724_MET30_MuIso0p1_InvMET30_InvMuIso0p1_withCR2SF --url -e "TTW"
  # Marina
  (9) ./getGenuineEfficiency.py --noSF SystTopBDT_180529_170402_MET30_MuIso0p1_InvMET20_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180602_115822_MET30_MuIso0p1_InvMET20_InvMuIso0p1_withCR1SF \
  --withCR2SF SystTopBDT_180530_080019_MET30_MuIso0p1_InvMET20_InvMuIso0p1_withCR2SF --url -e "TTW"
  
  (10) ./getGenuineEfficiency.py --noSF SystTopBDT_180529_094433_MET30_MuIso0p1_InvMET15_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180602_120116_MET30_MuIso0p1_InvMET15_InvMuIso0p1_withCR1SF \
  --withCR2SF SystTopBDT_180530_080239_MET30_MuIso0p1_InvMET15_InvMuIso0p1_withCR2SF --url -e "TTW"
  
  (11) ./getGenuineEfficiency.py --noSF SystTopBDT_180529_094647_MET50_MuIso0p2_InvMET30_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180602_122528_MET50_MuIso0p2_InvMET30_InvMuIso0p2_withCR1SF \
  --withCR2SF SystTopBDT_180530_075159_MET50_MuIso0p2_InvMET30_InvMuIso0p2_withCR2SF --url -e "TTW"

  (12) ./getGenuineEfficiency.py --noSF SystTopBDT_180529_094856_MET30_MuIso0p1_InvMET20_InvMuIso0p3_noSF --withCR1SF SystTopBDT_180602_123016_MET30_MuIso0p1_InvMET20_InvMuIso0p3_withCR1SF \
  --withCR2SF SystTopBDT_180530_074700_MET30_MuIso0p1_InvMET20_InvMuIso0p3_withCR2SF --url -e "TTW"




  
  OTHER SELECTIONS:
  (A) ./getGenuineEfficiency.py --noSF SystTopBDT_180513_100633_MET50_MuIso0p2_InvMET20_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180513_181711_MET50_MuIso0p2_InvMET20_InvMuIso0p2_withCR1SF \
  --withCR2SF SystTopBDT_180513_154620_MET50_MuIso0p2_InvMET20_InvMuIso0p2_withCR2SF --url -e "TTW"

  (B) ./getGenuineEfficiency.py --noSF SystTopBDT_180513_101101_MET50_MuIso0p1_InvMET20_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180513_184604_MET50_MuIso0p1_InvMET20_InvMuIso0p1_withCR1SF \
  --withCR2SF SystTopBDT_180513_155700_MET50_MuIso0p1_InvMET20_InvMuIso0p1_withCR2SF --url -e "TTW"
  
  (C) ./getGenuineEfficiency.py --noSF SystTopBDT_180513_101634_MET50_MuIso0p2_InvMET30_InvMuIso0p2_noSF --withCR1SF SystTopBDT_180513_185326_MET50_MuIso0p2_InvMET30_InvMuIso0p2_withCR1F \
  --withCR2SF SystTopBDT_180513_160712_MET50_MuIso0p2_InvMET30_InvMuIso0p2_withCR2SF --url -e "TTW"
  
  (D) ./getGenuineEfficiency.py --noSF SystTopBDT_180513_102112_MET50_MuIso0p1_InvMET30_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180513_185942_MET50_MuIso0p1_InvMET30_InvMuIso0p1_withCR1SF \
  --withCR2SF SystTopBDT_180513_161853_MET50_MuIso0p1_InvMET30_InvMuIso0p1_withCR2SF --url -e "TTW"

  (E) ./getGenuineEfficiency.py --noSF SystTopBDT_180514_110341_MET40_MuIso0p1_InvMET20_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180515_034913_MET40_MuIso0p1_InvMET20_InvMuIso0p1_withCR1SF \
  --withCR2SF SystTopBDT_180514_170239_MET40_MuIso0p1_InvMET20_InvMuIso0p1_withCR2SF --url -e "TTW"
  
  (F) ./getGenuineEfficiency.py --noSF SystTopBDT_180514_115524_MET40_MuIso0p1_InvMET30_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180515_035307_MET40_MuIso0p1_InvMET30_InvMuIso0p1_withCR1SF \
--withCR2SF SystTopBDT_180514_174250_MET40_MuIso0p1_InvMET30_InvMuIso0p1_withCR2SF --url -e "TTW"

  (G) ./getGenuineEfficiency.py --noSF SystTopBDT_180514_115629_MET30_MuIso0p1_InvMET20_InvMuIso0p1_noSF --withCR1SF SystTopBDT_180515_035717_MET30_MuIso0p1_InvMET20_InvMuIso0p1_withCR1SF \
--withCR2SF SystTopBDT_180514_174443_MET30_MuIso0p1_InvMET20_InvMuIso0p1_withCR2SF --url -e "TTW"

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
ROOT.gErrorIgnoreLevel = ROOT.kFatal #kPrint = 0,  kInfo = 1000, kWarning = 2000, kError = 3000, kBreak = 4000, kSysError = 5000, kFatal = 6000
from ROOT import *

import getpass

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.SystTopBDT.SystTopBDTNormalization as SystTopBDTNormalization

import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector
import HiggsAnalysis.FakeBMeasurement.FakeBResult as fakeBResult

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

def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h     = tefficiency.GetCopyTotalHisto()
    n     = h.GetNbinsX()
    
    # For-loop: All bins
    for i in range(1, n+1):
        # print "i=", i, " x=", h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i), "  Efficiency=", tefficiency.GetEfficiency(i)
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))

        # ugly hack to prevent error going above 1
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)

    graph = ROOT.TGraphAsymmErrors(n, array.array("d",x), array.array("d",y),
                                   array.array("d",xerrl), array.array("d",xerrh),
                                   array.array("d",yerrl), array.array("d",yerrh))
    return graph


def GetHistoKwargs(histoName):
    # Definitions
    _opts   = {}
    _cutBox = {}
    _rebinX = 1
    _logY   = True
    _opts   = {"ymin": 1e0, "ymaxfactor": 1.2}
    _ylabel = "Events / %.0f"
    if _logY:
        _opts = {"ymin": 1e0, "ymaxfactor": 5.0}

    if "pt" in histoName.lower():
        _units        = "GeV/c"
        _xlabel       = "p_{T} (%s)" % (_units)
        _ylabel      += " " + _units
        _cutBox       = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _rebinX       = 2
        if "tetrajetbjet" in histoName.lower():
            _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            _rebinX = 1

    if "mass" in histoName.lower():
        _units        = "GeV/c^{2}"
        _xlabel       = "m_{T} (%s)" % (_units)
        _ylabel      += " " + _units
        _opts["xmin"] = 0.0 
        _opts["xmax"] = 300
        _cutBox       = {"cutValue": 80.4, "fillColor": 16, "box": False, "line": True, "greaterThan": True}


    if "met" in histoName.lower():
        _units        = "GeV"
        _xlabel       = "E_{T}^{miss} (%s)" % (_units)
        _cutBox       = {"cutValue": 50.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _rebinX = 2
                
    # Define plotting options
    kwargs = {
        "xlabel"           : _xlabel,
        "rebinX"           : _rebinX,
        "ylabel"           : _ylabel,
        "log"              : _logY,
        "opts"             : _opts,
        "opts2"            : {"ymin": 0.6, "ymax": 2.0-0.6},
        "stackMCHistograms": True,
        "ratio"            : opts.ratio, 
        "ratioYlabel"      : "Data/MC",
        "ratioInvert"      : False, 
        "cutBox"           : _cutBox,
        "addLuminosityText": True, # cannot do that
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "createLegend"     : {"x1": 0.66, "y1": 0.70, "x2": 0.95, "y2": 0.92},
        }
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

def GetDatasetsFromDir(opts, pseudomulticrab):
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([pseudomulticrab], #opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([pseudomulticrab],#opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([pseudomulticrab],#opts.mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    
def PrintPSet(selection, datasetsMgr, depth=0):
    selection = "\"%s\":"  % (selection)
    thePSets = datasetsMgr.getAllDatasets()[0].getParameterSet()

    # First drop everything before the selection
    thePSet_1 = thePSets.split(selection)[-1]

    # Then drop everything after the selection
    thePSet_2 = thePSet_1.split("},")[depth]
    # Final touch
    thePSet = selection + thePSet_2

    Print(thePSet, True)
    return

def getHisto(datasetsMgr, datasetName, histoName, analysisType):
    Verbose("getHisto()", True)

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-" + datasetName)
    return h1

def getModuleInfoString(opts):
    moduleInfoString = "_%s_%s" % (opts.dataEra, opts.searchMode)
    if len(opts.optMode) > 0:
        moduleInfoString += "_%s" % (opts.optMode)
    return moduleInfoString

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Print(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return

#================================================================================================ 
# Main
#================================================================================================ 
def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(False)
    style.setGridY(False)

    optModes = [""]
    # For-loop: All opt Mode
    for opt in optModes:
        opts.optMode = opt

        # Numerator & Denominator dataset manager
        noSF_datasetsMgr      = GetDatasetsFromDir(opts, opts.noSFcrab)
        withCR1SF_datasetsMgr = GetDatasetsFromDir(opts, opts.withCR1SFcrab) 
        withCR2SF_datasetsMgr = GetDatasetsFromDir(opts, opts.withCR2SFcrab) 
        
        # Update all events to PU weighting
        noSF_datasetsMgr.updateNAllEventsToPUWeighted()
        withCR1SF_datasetsMgr.updateNAllEventsToPUWeighted()
        withCR2SF_datasetsMgr.updateNAllEventsToPUWeighted()
        
        # Load Luminosities
        noSF_datasetsMgr.loadLuminosities()
        withCR1SF_datasetsMgr.loadLuminosities()
        withCR2SF_datasetsMgr.loadLuminosities()
        
        if 0:
            noSF_datasetsMgr.PrintCrossSections()
            noSF_datasetsMgr.PrintLuminosities()
 
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(noSF_datasetsMgr) 
        plots.mergeRenameReorderForDataMC(withCR1SF_datasetsMgr) 
        plots.mergeRenameReorderForDataMC(withCR2SF_datasetsMgr) 
        
        # Get luminosity if a value is not specified
        if opts.intLumi < 0:
            opts.intLumi = noSF_datasetsMgr.getDataset("Data").getLuminosity()
            
        # Remove datasets
        removeList = []
        #removeList = ["TTWJetsToLNu_", "TTWJetsToQQ"]
        for i, d in enumerate(removeList, 0):
            msg = "Removing dataset %s" % d
            Print(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
            noSF_datasetsMgr.remove(filter(lambda name: d in name, noSF_datasetsMgr.getAllDatasetNames()))
            withCR1SF_datasetsMgr.remove(filter(lambda name: d in name, withCR1SF_datasetsMgr.getAllDatasetNames()))
        
        # Print summary of datasets to be used
        if 0:
            noSF_datasetsMgr.PrintInfo()
            withCR1SF_datasetsMgr.PrintInfo()
            withCR2SF_datasetsMgr.PrintInfo()
            
        # Merge EWK samples
        EwkDatasets = ["Diboson", "DYJetsToLL", "WJetsHT"]
        noSF_datasetsMgr.merge("EWK", EwkDatasets)
        withCR1SF_datasetsMgr.merge("EWK", EwkDatasets)
        withCR2SF_datasetsMgr.merge("EWK", EwkDatasets)
        
        # Get histosgram names
        folderListIncl = withCR1SF_datasetsMgr.getDataset(withCR1SF_datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        folderList = [h for h in folderListIncl if "AfterAllSelections_LeadingTrijet_Pt" in h ]

        # For-loop: All histo paths
        for h in folderList:
            if "lowMET" in h:
                folderList.remove(h)
        
        folderPath    = os.path.join(opts.folder, "")
        folderPathGen = os.path.join(opts.folder + "Genuine")
        folderPathFake =os.path.join(opts.folder + "Fake"   )
        
        histoList = folderList
        num_pathList = [os.path.join(folderPath, h) for h in histoList]
        num_pathList.extend([os.path.join(folderPathGen, h) for h in histoList])
        num_pathList.extend([os.path.join(folderPathFake, h) for h in histoList])
        
        # Denominator Histogram (To be used in the estimation of QCD Data-Driven)
        histoList = [h for h in folderListIncl if "AfterStandardSelections_LeadingTrijet_Pt" in h]
        den_pathList = [os.path.join(folderPath, h) for h in histoList]
        den_pathList.extend([os.path.join(folderPathGen, h) for h in histoList])
        den_pathList.extend([os.path.join(folderPathFake, h) for h in histoList])

        # For-loop: All histo paths
        for h in den_pathList:
            if "lowMET" in h:
                den_pathList.remove(h)
        
        # Do the histograms
        PlotHistos(noSF_datasetsMgr, withCR1SF_datasetsMgr, withCR2SF_datasetsMgr, num_pathList, den_pathList,  opts)
        
    return


def GetHistoPathDict(histoList, printList=False):
    
    histoDict = {}
    
    # For-loop: All histograms (full paths)
    for h in histoList:
        
        if "_SR" in h:
            region = "SR"
        elif "_VR" in h:
            region = "VR"
        elif "_CR1" in h:
            region = "CR1"
        elif "_CR2" in h:
            region = "CR2"
        else:
            raise Exception("Could not determine Control Region for histogram %s" % (h) )
        
        lIncl = "%s-%s" % (region, "Inclusive")
        lGen  = "%s-%s" % (region, "Genuine")
        lFake = "%s-%s" % (region, "Fake")
        
        if "Genuine" in h:
            histoDict[lGen] = h
        elif "Fake" in h:
            histoDict[lFake] = h
        else:
            histoDict[lIncl] = h
        
    # Create table of key->histogram mapping
    rows   = []
    align  = "{:<40} {:<80}"
    header = align.format("Key", "Full Path")
    hLine  = "="*120
    rows.append(hLine)
    rows.append(header)
    rows.append(hLine)
    for k in histoDict:
        rows.append(align.format(k, histoDict[k]))
    rows.append(hLine)
    rows.append("")

    if 0:#printList:
        for i, row in enumerate(rows, 1):
            Print(row, i==1)
    return histoDict

def GetRootHistos(datasetsMgr, histoList, regions):
    
    # Definition
    hPathDict = GetHistoPathDict(histoList, printList=True)
    rhDict    = {}
    
    # For-loop: All Control Regions (CR)
    for region in regions:
        
        # Define labels
        lIncl = "%s-%s" % (region, "Inclusive")
        lGen  = "%s-%s" % (region, "Genuine")
        lFake = "%s-%s" % (region, "Fake")
        
        # Get the desired histograms                                                                                                                                                                            
        pIncl = plots.DataMCPlot(datasetsMgr, hPathDict[lIncl])
        pGen  = plots.DataMCPlot(datasetsMgr, hPathDict[lGen])
        pFake = plots.DataMCPlot(datasetsMgr, hPathDict[lFake])
        
        
        # Get the desired histograms
        p = plots.DataMCPlot(datasetsMgr, hPathDict[lIncl])
        
        # Clone and Save the root histograms
        rhDict["TT-"  + lIncl] = pIncl.histoMgr.getHisto("TT").getRootHisto().Clone("TT-" + lIncl)
        rhDict["TT-"  + lGen ] = pGen.histoMgr.getHisto("TT").getRootHisto().Clone("TT-" + lGen)
        rhDict["TT-"  + lFake] = pFake.histoMgr.getHisto("TT").getRootHisto().Clone("TT-" + lFake)
        
        rhDict["Data-"+ lIncl] = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("Data-" + lIncl)
        rhDict["EWK-" + lIncl] = pIncl.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK-" + lIncl)
        rhDict["QCD-" + lIncl] = pIncl.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD-" + lIncl)
        
        rhDict["SingleTop-" + lIncl] = pIncl.histoMgr.getHisto("SingleTop").getRootHisto().Clone("SingleTop-" + lIncl)
        rhDict["SingleTop-" + lGen ] =  pGen.histoMgr.getHisto("SingleTop").getRootHisto().Clone("SingleTop-" + lGen)
        rhDict["SingleTop-" + lFake] = pFake.histoMgr.getHisto("SingleTop").getRootHisto().Clone("SingleTop-" + lFake)
        
    return rhDict

def GetHistosForEfficiency(hNumerator, hDenominator):
    
    hNum = hNumerator.Clone("Numerator")
    hDen = hDenominator.Clone("Denominator")
    hNum.Reset()
    hDen.Reset()

    # Debug
    for i in range(0, hDenominator.GetNbinsX()+1):
        num    = hNumerator.GetBinContent(i)
        numErr = hNumerator.GetBinError(i)
        den    = hDenominator.GetBinContent(i)
        denErr = hDenominator.GetBinError(i)
        
        if num < 0:
            num    = 0.00001
            numErr = 0.000001

        if den == 0:
            den    = 0.00001
            denErr = 0.000001

        if num > den:
            num = den

        # Fill histos
        if 0:
            print "num: %s +/- %s" % (num, numErr)
            print "den: %s +/- %s" % (den, denErr)
            print
        
        hNum.SetBinContent(i, num)
        hNum.SetBinError(i, numErr)
        hDen.SetBinContent(i, den)
        hDen.SetBinError(i, denErr)
    return hNum, hDen

def PlotHistos(noSF_datasetsMgr, withCR1SF_datasetsMgr, withCR2SF_datasetsMgr, num_histoList, den_histoList,  opts):    
    
    # Get the histogram customisations (keyword arguments)
    _kwargs = GetHistoKwargs(num_histoList[0])
    
    # Get the root histos for all datasets and Control Regions (CRs)
    regions = ["SR", "VR", "CR1", "CR2"]
    labels  = ["Genuine", "Fake", "Inclusive"]
    
    #==========================================================================================
    # Get Dictionaries
    #==========================================================================================
    rhDict_den_noSF      = GetRootHistos(noSF_datasetsMgr,      den_histoList, regions)
    rhDict_num_noSF      = GetRootHistos(noSF_datasetsMgr,      num_histoList, regions)
    rhDict_num_withCR1SF = GetRootHistos(withCR1SF_datasetsMgr, num_histoList, regions) # Scale Factors from CR1 are only applied in the Numerator on Fake TT
    rhDict_num_withCR2SF = GetRootHistos(withCR2SF_datasetsMgr, num_histoList, regions) # Scale Factors from CR2 are only applied in the Numerator on EWK+QCD+ST
    
    # =========================================================================================
    # Normalization Factors (see: getNormalization.py)
    # =========================================================================================
    # Marina
    #f1=0.610901; f2=0.889906; # (1)
    #f1=0.610901; f2=0.906343; # (2)
    #f1=0.610963; f2=0.903020; # (3)
    #f1=0.610901; f2=0.901711; # (4)
    #f1=0.603648; f2=0.907290; # (5)
    #f1=0.611682; f2=0.889619; # (6)
    #f1=0.613102; f2=0.902808; # (7)
    #f1=0.609202; f2=0.906565; # (8)
    #f1=0.613102; f2=0.906056; # (9)
    #f1=0.608068; f2=0.906713; # (10)
    #f1=0.610901; f2=0.889106; # (11)
    f1=0.616422; f2=0.905622; # (12)
    
    # =========================================================================================
    # (A) Apply Normalization Factors (see: getNormalizations.py)
    # =========================================================================================
    
    # Normalize all histograms (QCD and TT) to normalization factors
    for re in regions:
        
        rhDict_den_noSF["NormQCD-"+re+"-Inclusive"] = rhDict_den_noSF["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_den_noSF["NormQCD-"+re+"-Inclusive"].Scale(f1)

        rhDict_num_noSF["NormQCD-"+re+"-Inclusive"] =rhDict_num_noSF["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_num_noSF["NormQCD-"+re+"-Inclusive"].Scale(f1)

        rhDict_num_withCR2SF["NormQCD-"+re+"-Inclusive"] = rhDict_num_withCR2SF["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_num_withCR2SF["NormQCD-"+re+"-Inclusive"].Scale(f1)
        
        for la in labels:
            
            rhDict_den_noSF["NormTT-"+re+"-"+la] = rhDict_den_noSF["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_den_noSF["NormTT-"+re+"-"+la].Scale(f2)
            
            rhDict_num_noSF["NormTT-"+re+"-"+la] = rhDict_num_noSF["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_num_noSF["NormTT-"+re+"-"+la].Scale(f2)
            
            rhDict_num_withCR1SF["NormTT-"+re+"-"+la] = rhDict_num_withCR1SF["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_num_withCR1SF["NormTT-"+re+"-"+la].Scale(f2)
            
    # ==========================================================================================
    # (B) Estimate Genuine TT in SR
    # ==========================================================================================
            
    # (B1) Genuine TT in Data - Denominator = Data - F1*QCD - F2*FakeTT - EWK - ST
    rhDict_den_noSF["TTinData-SR-Genuine"] = rhDict_den_noSF["Data-SR-Inclusive"].Clone("genuine t#bar{t} (Data)") 
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["NormQCD-SR-Inclusive"],   -1)
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["NormTT-SR-Fake"],         -1)
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["EWK-SR-Inclusive"],       -1)
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["SingleTop-SR-Inclusive"], -1)

    # (B2) Genuine TT in Data - Numerator = Data - F1*QCD*SF_{CR2} - F2*FakeTT*SF_{CR1} - ST*SF_{CR2} - EWK*SF_{CR2}
    rhDict_num_noSF["TTinData-SR-Genuine"] = rhDict_num_noSF["Data-SR-Inclusive"].Clone("genuine t#bar{t} (Data)")
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withCR2SF["NormQCD-SR-Inclusive"],   -1)
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withCR1SF["NormTT-SR-Fake"],         -1)
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withCR2SF["SingleTop-SR-Inclusive"], -1)
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withCR2SF["EWK-SR-Inclusive"],       -1)
    
    # (B3) Genuine TT in MC - Denominator:  rhDict_den_noSF["TT-SR-Genuine"]
    # (B4) Genuine TT in MC - Numerator:    rhDict_num_noSF["TT-SR-Genuine"]
    
    # ========================================================================================
    # (C) Plot Numerator and Denominator (Data Vs MC)
    # ========================================================================================
    _kwargs["opts"] = {"xmax" : 800, "ymaxfactor" : 2.0}
    _kwargs["ratioYlabel"]  = "Data/MC"
    _kwargs["ratio"]        = True
    _kwargs["stackMCHistograms"] = False
    _kwargs["createLegend"]      = {"x1": 0.60, "y1": 0.75, "x2": 0.95, "y2": 0.92}
    _kwargs["ratioInvert"]  = True

    num_data = rhDict_num_noSF["TTinData-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (Data)")
    den_data = rhDict_den_noSF["TTinData-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (Data)")
    
    num_mc = rhDict_num_noSF["TT-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (MC)")
    den_mc = rhDict_den_noSF["TT-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (MC)")
    
    num_data.Rebin(2)
    num_mc.Rebin(2)
    den_data.Rebin(2)
    den_mc.Rebin(2)               

    styles.getABCDStyle("CR4").apply(num_mc)
    styles.getABCDStyle("CR4").apply(den_mc)
    
    # Denominator
    hName = "GenuineTT_SR_Denominator"
    hData_Den = histograms.Histo( den_data, "genuine t#bar{t}_{SR} (Data)", "Data", drawStyle="AP"); hData_Den.setIsDataMC(isData=True, isMC=False)
    hMC_Den   = histograms.Histo( den_mc,   "genuine t#bar{t}_{SR} (MC)", "MC", drawStyle="HIST");   hMC_Den.setIsDataMC(isData=False, isMC=True)

    pDen = plots.ComparisonManyPlot(hData_Den, [hMC_Den], saveFormats=[])
    pDen.setLuminosity(opts.intLumi)
    pDen.setDefaultStyles()
    plots.drawPlot(pDen, hName, **_kwargs)
    SavePlot(pDen, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # Numerator
    hName = "GenuineTT_SR_Numerator"
    hData_Num = histograms.Histo( num_data, "genuine t#bar{t}_{SR} (Data)", "Data", drawStyle="AP"); hData_Num.setIsDataMC(isData=True, isMC=False)
    hMC_Num   = histograms.Histo( num_mc,   "genuine t#bar{t}_{SR} (MC)", "MC", drawStyle="HIST");   hMC_Num.setIsDataMC(isData=False, isMC=True)

    pNum = plots.ComparisonManyPlot(hData_Num, [hMC_Num], saveFormats=[])
    pNum.setLuminosity(opts.intLumi)
    pNum.setDefaultStyles()
    plots.drawPlot(pNum, hName, **_kwargs)
    SavePlot(pNum, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # ========================================================================================
    # (D) Plot Genuine TT Efficiency
    # ========================================================================================
    _kwargs = {
        "xlabel"           : "p_{T} (GeV/c)",
        "ylabel"           : "Efficiency",
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True,
        "ratioInvert"      : False,
        "ratioType"        : "errorScale",
        "ratioCreateLegend": True,
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.08},
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False},
        "errorBarsX"       : True,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.2, "xmax" : 600},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : False,
        "createLegend"     : {"x1": 0.54, "y1": 0.80, "x2": 0.95, "y2": 0.92},
        }

    bins  = [0, 100, 200, 300, 400, 500, 600]
    xBins = array.array('d', bins)
    nx    = len(xBins)-1

    # Data 
    h0_data_den = rhDict_den_noSF["TTinData-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (Data)")
    h0_data_num = rhDict_num_noSF["TTinData-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (Data)")
    
    # MC
    h0_mc_den = rhDict_den_noSF["TT-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (MC)")
    h0_mc_num = rhDict_num_noSF["TT-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (MC)")
    
    h0_data_den = h0_data_den.Rebin(nx, "", xBins)
    h0_data_num = h0_data_num.Rebin(nx, "", xBins)
    
    h0_mc_den = h0_mc_den.Rebin(nx, "", xBins)
    h0_mc_num = h0_mc_num.Rebin(nx, "", xBins)
    
    hNumerator_Data, hDenominator_Data = GetHistosForEfficiency(h0_data_num, h0_data_den)
    hNumerator_MC,   hDenominator_MC   = GetHistosForEfficiency(h0_mc_num, h0_mc_den)
    
    eff_data = ROOT.TEfficiency(hNumerator_Data, hDenominator_Data)
    eff_mc   = ROOT.TEfficiency(hNumerator_MC,   hDenominator_MC)

    eff_data.SetStatisticOption(ROOT.TEfficiency.kFCP)
    eff_mc.SetStatisticOption(ROOT.TEfficiency.kFCP)

    geff_data = convert2TGraph(eff_data)
    geff_mc   = convert2TGraph(eff_mc)

    styles.dataStyle.apply(geff_data)
    styles.ttStyle.apply(geff_mc)

    Graph_Data = histograms.HistoGraph(geff_data, "genuine t#bar{t}_{SR} (Data) ", "p", "P")
    Graph_MC   = histograms.HistoGraph(geff_mc, "genuine t#bar{t}_{SR} (MC)", "p", "P")
    
    p = plots.ComparisonManyPlot(Graph_MC, [Graph_Data], saveFormats=[])
    saveName = "Efficiency_GenuineTT_SR"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])


    return



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

    # Save to dirs
    
    # Default Settings
    ANALYSISNAME = "SystTopBDT"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    ALTPLOT      = False
    INTLUMI      = -1.0
    MCONLY       = False
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    USEMC        = False
    RATIO        = True
    FOLDER       = "SystTopBDT_"
    INCLUSIVE    = False

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")
    
    parser.add_option("--noSF", dest="noSFcrab", action="store",
                      help="Path to the pseudo-multicrab directory without SF")
    
    parser.add_option("--withCR1SF", dest="withCR1SFcrab", action="store",
                      help="Path to the pseudo-multicrab directory with SF from CR1")
    
    parser.add_option("--withCR2SF", dest="withCR2SFcrab", action="store",
                      help="Path to the pseudo-multicrab directory with SF from CR2")

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

    parser.add_option("--altPlot", dest="altPlot", action="store_true", default=ALTPLOT, 
                      help="Draw alternative plot with Data and Bkg-Sum [default: %s]" % ALTPLOT)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store", 
                      help="List of datasets in numcrab and dencrab to include")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in numcrab and dencrab to exclude")

    parser.add_option("--useMC", dest="useMC", action="store_true", default=USEMC,
                      help="Use QCD MC instead of QCD=Data-EWK? [default: %s]" % (USEMC) )
    
    parser.add_option("--inclusiveOnly", dest="inclusiveOnly", action="store_true", default=INCLUSIVE,
                      help="Only calculate the inclusive Transfer Factor (TF). Do not calculated binned TF? [default: %s]" % (INCLUSIVE) )
    
    parser.add_option("--ratio", dest="ratio", action="store_true", default=RATIO,
                      help="Draw ratio canvas for Data/MC curves? [default: %s]" % (RATIO) )
    
    parser.add_option("--folder", dest="folder", default=FOLDER,
                      help="Folder in ROOT files under which all necessary histograms are located [default: %s]" % (FOLDER) )

    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
        
    # Sanity check
    if opts.noSFcrab == None or opts.withCR1SFcrab == None or opts.withCR2SFcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
        
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.noSFcrab, prefix=opts.analysisName+"/", postfix="")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== getEfficiencies.py: Press any key to quit ROOT ...")
