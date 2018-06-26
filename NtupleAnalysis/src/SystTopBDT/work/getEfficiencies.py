#!/usr/bin/env python
'''
  DESCRIPTION:
  
  This script calculates the genuine & inclusive tt efficiency. 

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
  
  Numerator:    [ Data - (F1*QCD - EWK - ST - F2*FakeTT)*SF ] passing BDT
  Denominator:  [ Data - (F1*QCD - EWK - ST - F2*FakeTT)    ]
  
  Inclusive TT in Data:
  
  Numerator:    [ Data - (F1*QCD - EWK - ST)*SF ] passing BDT
  Denominator:  [ Data - (F1*QCD - EWK - ST)    ]

  SF = Efficiency in Data / Efficiency in MC
  
  USAGE:
  ./getEfficiencies.py --noSF <pseudo multicrab with no SF applied> --withSF <pseudo multicrab with SF applied> [opts]
  
  
  LAST USED:
  
  BDT 0.00: ./getEfficiencies.py --noSF SystTopBDT_180621_085413_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p00_noSF \
  --withSF SystTopBDT_180621_162205_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p00_withSF \
  --url -e "TTW"
  
  BDT 0.10: ./getEfficiencies.py --noSF SystTopBDT_180621_112722_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p10_noSF \
  --withSF SystTopBDT_180621_162205_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p00_withSF \
  --url -e "TTW"
  
  BDT 0.20: ./getEfficiencies.py --noSF SystTopBDT_180621_090053_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p20_noSF \
  --withSF SystTopBDT_180621_163417_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p20_withSF \
  --url -e "TTW"
  
  BDT 0.30: ./getEfficiencies.py --noSF SystTopBDT_180621_090339_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p30_noSF \
  --withSF SystTopBDT_180621_163417_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p20_withSF \
  --url -e "TTW"

  BDT 0.40: ./getEfficiencies.py --noSF SystTopBDT_180620_045023_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p40_noSF \
  --withSF SystTopBDT_180621_093037_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p40_withSF \
  --url -e "TTW"
  
  BDT 0.50: ./getEfficiencies.py --noSF SystTopBDT_180620_045528_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p50_noSF \
  --withSF SystTopBDT_180621_094207_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p50_withSF \
  --url -e "TTW"
  
  BDT 0.60: ./getEfficiencies.py --noSF SystTopBDT_180620_050745_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p60_noSF \
  --withSF SystTopBDT_180621_094642_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p60_withSF \
  --url -r "TTW"
  
  BDT 0.70: ./getEfficiencies.py --noSF SystTopBDT_180620_052556_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p70_noSF \
  --withSF SystTopBDT_180621_095138_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p70_withSF \
  --url -e "TTW"
  
  BDT 0.80: ./getEfficiencies.py --noSF SystTopBDT_180620_054613_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p80_noSF \
  --withSF SystTopBDT_180621_095603_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p80_withSF \
  --url -e "TTW"
  
  BDT 0.90: ./getEfficiencies.py --noSF SystTopBDT_180620_055650_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p90_noSF \
  --withSF SystTopBDT_180621_095852_MET50_MuIso0p1_InvMET20_InvMuIso0p1_massCut300_BDTCut0p90_withSF \
  --url -e "TTW"
  
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
        datasetMgr_noSF   = GetDatasetsFromDir(opts, opts.noSFcrab)
        datasetMgr_withSF = GetDatasetsFromDir(opts, opts.withSFcrab)
        
        # Update all events to PU weighting
        datasetMgr_noSF.updateNAllEventsToPUWeighted()
        datasetMgr_withSF.updateNAllEventsToPUWeighted()
        
        # Load Luminosities
        datasetMgr_noSF.loadLuminosities()
        
        if 0:
            datasetMgr_noSF.PrintCrossSections()
             
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetMgr_noSF)
        plots.mergeRenameReorderForDataMC(datasetMgr_withSF)
        
        # Get luminosity if a value is not specified
        if opts.intLumi < 0:
            opts.intLumi = datasetMgr_noSF.getDataset("Data").getLuminosity()
            
        # Merge EWK samples
        EwkDatasets = ["Diboson", "DYJetsToLL", "WJetsHT"]
        datasetMgr_noSF.merge("EWK", EwkDatasets)
        datasetMgr_withSF.merge("EWK", EwkDatasets)
                
        # Get histosgram names
        folderListIncl = datasetMgr_withSF.getDataset(datasetMgr_withSF.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
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
        PlotHistos(datasetMgr_noSF, datasetMgr_withSF, num_pathList, den_pathList,  opts)
        
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

def PlotHistos(d_noSF, d_withSF, num_histoList, den_histoList,  opts):    
    
    # Get the histogram customisations (keyword arguments)
    _kwargs = GetHistoKwargs(num_histoList[0])
    
    # Get the root histos for all datasets and Control Regions (CRs)
    regions = ["SR", "VR", "CR1", "CR2"]
    labels  = ["Genuine", "Fake", "Inclusive"]
    
    #==========================================================================================
    # Get Dictionaries
    #==========================================================================================
    rhDict_den_noSF   = GetRootHistos(d_noSF, den_histoList, regions)
    rhDict_num_noSF   = GetRootHistos(d_noSF, num_histoList, regions)
    rhDict_num_withSF = GetRootHistos(d_withSF, num_histoList, regions) 
        
    # =========================================================================================
    # Normalization Factors (see: getNormalization.py)
    # =========================================================================================
    f1=0.619886; f2=0.904877;
    
    # =========================================================================================
    # (A) Apply Normalization Factors (see: getNormalizations.py)
    # =========================================================================================
    
    # Normalize all histograms (QCD and TT) to normalization factors
    for re in regions:
        
        rhDict_den_noSF["NormQCD-"+re+"-Inclusive"] = rhDict_den_noSF["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_den_noSF["NormQCD-"+re+"-Inclusive"].Scale(f1)

        rhDict_num_noSF["NormQCD-"+re+"-Inclusive"] =rhDict_num_noSF["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_num_noSF["NormQCD-"+re+"-Inclusive"].Scale(f1)

        rhDict_num_withSF["NormQCD-"+re+"-Inclusive"] = rhDict_num_withSF["QCD-"+re+"-Inclusive"].Clone("NormQCD-"+re+"-Inclusive")
        rhDict_num_withSF["NormQCD-"+re+"-Inclusive"].Scale(f1)
        
        for la in labels:
            
            rhDict_den_noSF["NormTT-"+re+"-"+la] = rhDict_den_noSF["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_den_noSF["NormTT-"+re+"-"+la].Scale(f2)
            
            rhDict_num_noSF["NormTT-"+re+"-"+la] = rhDict_num_noSF["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_num_noSF["NormTT-"+re+"-"+la].Scale(f2)
            
            rhDict_num_withSF["NormTT-"+re+"-"+la] = rhDict_num_withSF["TT-"+re+"-"+la].Clone("NormTT-"+re+"-"+la)
            rhDict_num_withSF["NormTT-"+re+"-"+la].Scale(f2)
            

    # =========================================================================================
    # (B) Estimate Inclusive TT in SR
    # =========================================================================================
    
    # (B1) Inclusive TT in Data (Denominator)  =  Data - F1*QCD - EWK - ST
    rhDict_den_noSF["TTinData-SR-Inclusive"] = rhDict_den_noSF["Data-SR-Inclusive"].Clone("Inclusive t#bar{t} (Data)")
    rhDict_den_noSF["TTinData-SR-Inclusive"].Add(rhDict_den_noSF["NormQCD-SR-Inclusive"],   -1)
    rhDict_den_noSF["TTinData-SR-Inclusive"].Add(rhDict_den_noSF["EWK-SR-Inclusive"],       -1)
    rhDict_den_noSF["TTinData-SR-Inclusive"].Add(rhDict_den_noSF["SingleTop-SR-Inclusive"], -1)
    
    # (B2) Inclusive TT in Data (Numerator)    =  Data - (F1*QCD -EWK - ST)*SF
    rhDict_num_noSF["TTinData-SR-Inclusive"] = rhDict_num_noSF["Data-SR-Inclusive"].Clone("Inclusive t#bar{t} (Data)")
    rhDict_num_noSF["TTinData-SR-Inclusive"].Add(rhDict_num_withSF["NormQCD-SR-Inclusive"],   -1)
    rhDict_num_noSF["TTinData-SR-Inclusive"].Add(rhDict_num_withSF["EWK-SR-Inclusive"],       -1)
    rhDict_num_noSF["TTinData-SR-Inclusive"].Add(rhDict_num_withSF["SingleTop-SR-Inclusive"], -1)
    
    # ==========================================================================================
    # (C) Plot Inclusive Efficiency (Data Vs MC)
    # ==========================================================================================
    _kwargs["opts"] = {"xmax" : 800, "ymaxfactor" : 2.0}
    _kwargs["ratioYlabel"]  = "Data/MC"
    _kwargs["ratio"]        = True
    _kwargs["stackMCHistograms"] = False
    _kwargs["createLegend"]      = {"x1": 0.60, "y1": 0.75, "x2": 0.95, "y2": 0.92}
    _kwargs["ratioInvert"]  = True
    
    num_data = rhDict_num_noSF["TTinData-SR-Inclusive"].Clone("t#bar{t}_{SR} (Data)")
    den_data = rhDict_den_noSF["TTinData-SR-Inclusive"].Clone("t#bar{t}_{SR} (Data)")
    
    num_mc = rhDict_num_noSF["TT-SR-Inclusive"].Clone("t#bar{t}_{SR} (MC)")
    den_mc = rhDict_den_noSF["TT-SR-Inclusive"].Clone("t#bar{t}_{SR} (MC)")
    
    num_data.Rebin(2)
    num_mc.Rebin(2)
    den_data.Rebin(2)
    den_mc.Rebin(2)

    styles.getABCDStyle("CR4").apply(num_mc)
    styles.getABCDStyle("CR4").apply(den_mc)
    
    # Denominator
    hName = "InclusiveTT_SR_Denominator"
    hData_Den = histograms.Histo( den_data, "t#bar{t}_{SR} (Data)", "Data", drawStyle="AP"); hData_Den.setIsDataMC(isData=True, isMC=False)
    hMC_Den   = histograms.Histo( den_mc,   "t#bar{t}_{SR} (MC)", "MC", drawStyle="HIST");   hMC_Den.setIsDataMC(isData=False, isMC=True)

    pDen = plots.ComparisonManyPlot(hData_Den, [hMC_Den], saveFormats=[])
    pDen.setLuminosity(opts.intLumi)
    pDen.setDefaultStyles()
    plots.drawPlot(pDen, hName, **_kwargs)
    SavePlot(pDen, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    # Numerator
    hName = "InclusiveTT_SR_Numerator"
    hData_Num = histograms.Histo( num_data, "t#bar{t}_{SR} (Data)", "Data", drawStyle="AP"); hData_Num.setIsDataMC(isData=True, isMC=False)
    hMC_Num   = histograms.Histo( num_mc,   "t#bar{t}_{SR} (MC)", "MC", drawStyle="HIST");   hMC_Num.setIsDataMC(isData=False, isMC=True)
    
    pNum = plots.ComparisonManyPlot(hData_Num, [hMC_Num], saveFormats=[])
    pNum.setLuminosity(opts.intLumi)
    pNum.setDefaultStyles()
    plots.drawPlot(pNum, hName, **_kwargs)
    SavePlot(pNum, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # =========================
    # Inclusive Efficiency
    # =========================
    _kwargs = {
        "xlabel"           : "p_{T} (GeV/c)",
        "ylabel"           : "Efficiency",
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True,
        "ratioInvert"      : False,
        "ratioType"        : None,
        "ratioCreateLegend": True,
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.08},
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False},
        "errorBarsX"       : True,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.5, "xmax" : 600},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : False,
        "createLegend"     : {"x1": 0.64, "y1": 0.80, "x2": 0.95, "y2": 0.92},
        }

    bins  = [0, 100, 200, 300, 400, 500, 600]
    xBins = array.array('d', bins)
    nx    = len(xBins)-1

    # Data 
    h0_data_den = rhDict_den_noSF["TTinData-SR-Inclusive"].Clone("t#bar{t}_{SR} (Data)")
    h0_data_num = rhDict_num_noSF["TTinData-SR-Inclusive"].Clone("t#bar{t}_{SR} (Data)")
    
    # MC
    h0_mc_den = rhDict_den_noSF["TT-SR-Inclusive"].Clone("t#bar{t}_{SR} (MC)")
    h0_mc_num = rhDict_num_noSF["TT-SR-Inclusive"].Clone("t#bar{t}_{SR} (MC)")
    
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

    Graph_Data = histograms.HistoGraph(geff_data, "t#bar{t}_{SR} (Data) ", "p", "P")
    Graph_MC   = histograms.HistoGraph(geff_mc, "t#bar{t}_{SR} (MC)", "p", "P")
    
    p = plots.ComparisonManyPlot(Graph_MC, [Graph_Data], saveFormats=[])
    saveName = "Efficiency_InclusiveTT_SR"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])
    
    
    
    # ==========================================================================================
    # (D) Estimate Genuine TT in SR
    # ==========================================================================================
    
    # (D1) Genuine TT in Data - Denominator = Data - F1*QCD - F2*FakeTT - EWK - ST
    rhDict_den_noSF["TTinData-SR-Genuine"] = rhDict_den_noSF["Data-SR-Inclusive"].Clone("genuine t#bar{t} (Data)") 
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["NormQCD-SR-Inclusive"],   -1)
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["NormTT-SR-Fake"],         -1)
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["EWK-SR-Inclusive"],       -1)
    rhDict_den_noSF["TTinData-SR-Genuine"].Add(rhDict_den_noSF["SingleTop-SR-Inclusive"], -1)

    # (D2) Genuine TT in Data - Numerator = Data - [F1*QCD - F2*FakeTT - ST - EWK] * SF
    rhDict_num_noSF["TTinData-SR-Genuine"] = rhDict_num_noSF["Data-SR-Inclusive"].Clone("genuine t#bar{t} (Data)")
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withSF["NormQCD-SR-Inclusive"],   -1)
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withSF["NormTT-SR-Fake"],         -1)
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withSF["SingleTop-SR-Inclusive"], -1)
    rhDict_num_noSF["TTinData-SR-Genuine"].Add(rhDict_num_withSF["EWK-SR-Inclusive"],       -1)
    
    # ========================================================================================
    # (E) Plot Numerator and Denominator (Data Vs MC)
    # ========================================================================================
    _kwargs = GetHistoKwargs(num_histoList[0])
    _kwargs["opts"] = {"xmax" : 800, "ymaxfactor" : 2.0}
    _kwargs["ratioYlabel"]  = "Data/MC"
    _kwargs["ratio"]        = True
    _kwargs["stackMCHistograms"] = False
    _kwargs["createLegend"]      = {"x1": 0.60, "y1": 0.75, "x2": 0.95, "y2": 0.92}
    _kwargs["ratioInvert"]  = True
    
    num_data.Reset()
    den_data.Reset()
    num_mc.Reset()
    den_mc.Reset()
    
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

    pDenumerator = plots.ComparisonManyPlot(hData_Den, [hMC_Den], saveFormats=[])
    pDenumerator.setLuminosity(opts.intLumi)
    pDenumerator.setDefaultStyles()
    plots.drawPlot(pDenumerator, hName, **_kwargs)
    SavePlot(pDenumerator, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # Numerator
    hName = "GenuineTT_SR_Numerator"
    hData_Num = histograms.Histo( num_data, "genuine t#bar{t}_{SR} (Data)", "Data", drawStyle="AP"); hData_Num.setIsDataMC(isData=True, isMC=False)
    hMC_Num   = histograms.Histo( num_mc,   "genuine t#bar{t}_{SR} (MC)", "MC", drawStyle="HIST");   hMC_Num.setIsDataMC(isData=False, isMC=True)

    pNumerator = plots.ComparisonManyPlot(hData_Num, [hMC_Num], saveFormats=[])
    pNumerator.setLuminosity(opts.intLumi)
    pNumerator.setDefaultStyles()
    plots.drawPlot(pNumerator, hName, **_kwargs)
    SavePlot(pNumerator, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # ========================================================================================
    # (F) Plot Genuine TT Efficiency
    # ========================================================================================
    _kwargs = {
        "xlabel"           : "p_{T} (GeV/c)",
        "ylabel"           : "Efficiency",
        "ratioYlabel"      : "Data/MC",
        "ratio"            : True,
        "ratioInvert"      : False,
        "ratioType"        : None, #"errorScale",
        "ratioCreateLegend": True,
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.08},
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False},
        "errorBarsX"       : True,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.25, "xmax" : 600},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : False,
        "createLegend"     : {"x1": 0.54, "y1": 0.80, "x2": 0.95, "y2": 0.92},
        }

    bins  = [0, 100, 200, 300, 400, 500, 600]
    xBins = array.array('d', bins)
    nx    = len(xBins)-1
    
    # Data 
    h1_data_den = rhDict_den_noSF["TTinData-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (Data)")
    h1_data_num = rhDict_num_noSF["TTinData-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (Data)")
    
    # MC
    h1_mc_den = rhDict_den_noSF["TT-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (MC)")
    h1_mc_num = rhDict_num_noSF["TT-SR-Genuine"].Clone("genuine t#bar{t}_{SR} (MC)")
    
    h1_data_den = h1_data_den.Rebin(nx, "", xBins)
    h1_data_num = h1_data_num.Rebin(nx, "", xBins)
    
    h1_mc_den = h1_mc_den.Rebin(nx, "", xBins)
    h1_mc_num = h1_mc_num.Rebin(nx, "", xBins)
    
    h_Numerator_Data, h_Denominator_Data = GetHistosForEfficiency(h1_data_num, h1_data_den)
    h_Numerator_MC,   h_Denominator_MC   = GetHistosForEfficiency(h1_mc_num, h1_mc_den)
    
    effi_data = ROOT.TEfficiency(h_Numerator_Data, h_Denominator_Data)
    effi_mc   = ROOT.TEfficiency(h_Numerator_MC,   h_Denominator_MC)

    effi_data.SetStatisticOption(ROOT.TEfficiency.kFCP)
    effi_mc.SetStatisticOption(ROOT.TEfficiency.kFCP)

    geffi_data = convert2TGraph(effi_data)
    geffi_mc   = convert2TGraph(effi_mc)

    styles.dataStyle.apply(geffi_data)
    styles.ttStyle.apply(geffi_mc)
    
    Graph_Data = histograms.HistoGraph(geffi_data, "genuine t#bar{t}_{SR} (Data) ", "p", "P")
    Graph_MC   = histograms.HistoGraph(geffi_mc, "genuine t#bar{t}_{SR} (MC)", "p", "P")
    
    pp = plots.ComparisonManyPlot(Graph_MC, [Graph_Data], saveFormats=[])
    saveName = "Efficiency_GenuineTT_SR"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    plots.drawPlot(pp, savePath, **_kwargs)
    SavePlot(pp, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])


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
    
    parser.add_option("--noSF", dest="noSFcrab", action="store", help="Path to the pseudo-multicrab directory without SF")
    
    parser.add_option("--withSF", dest="withSFcrab", action="store", help="Path to the pseudo-multicrab directory with SF applied")
    
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
    if opts.noSFcrab == None or opts.withSFcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
        
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.noSFcrab, prefix=opts.analysisName+"/", postfix="")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== getEfficiencies.py: Press any key to quit ROOT ...")
