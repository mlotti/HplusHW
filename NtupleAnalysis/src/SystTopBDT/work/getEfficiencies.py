#!/usr/bin/env python
'''
DESCRIPTION:
This script produces FakeTop normalization factors by employing an ABCD method
using regions created by muon mini-isolation and MET selections as follows:

         Mini-Isolation
              ^
              |
              |--------------|--------------|--------------|
        >=0.2 |      CR2     |      -       |      VR      |
              |--------------------------------------------|
              |       -      |      -       |      -       |
              |--------------|--------------|--------------|
         <0.1 |      CR1     |      -       |      SR      |
              |--------------|--------------|--------------|----> MET
              |              30             50             |

SR/VR = CR1/CR2

SR = (CR1/CR2)*VR

We call the ratio f=(CR1/CR2) the transfer factor that gets us from VR to the SR. This
is needed to ensure the normalisation of the sample obtained from VR is corrected.

USAGE:
./getEfficiencies.py -num <pseudo_nummcrab_directory> -den <pseudo_dencrab_directory> [opts]


EXAMPLES: 
./getEfficiencies.py --noSF SystTopBDT_180422_MET50_MuIso0p1_InvMET30_InvMuIso0p2_noSF --withQCDSF SystTopBDT_180424_104907_with_EWK_QCD_ST_SF --withEWKFakeTTSF SystTopBDT_180424_175913_withFakeTTSF_new/ -e "TTWJetsToLNu|TTWJetsToQQ" --url
./getEfficiencies.py --noSF SystTopBDT_180422_MET50_MuIso0p1_InvMET30_InvMuIso0p2_noSF --withQCDSF SystTopBDT_180424_104907_with_EWK_QCD_ST_SF --withEWKFakeTTSF SystTopBDT_180424_175913_withFakeTTSF_new/ --url -e "TTWJets"

LAST USED:
./getEfficiencies.py --noSF SystTopBDT_180425_063552_MET50_MuIso0p1_InvMET30_InvMuIso0p2_noSF_NEW --withQCDSF SystTopBDT_180426_131358_MET50_MuIso0p1_InvMET30_InvMuIso0p2_QCDEWKSTSF --withEWKFakeTTSF SystTopBDT_180426_130544_MET50_MuIso0p1_InvMET30_InvMuIso0p2_FakeTTSF

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
        #_opts["xmin"] =  50
        #_opts["xmax"] = 300
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

        if "tetrajet" in histoName.lower():
            _xlabel       = "m_{jjbb} (%s)" % (_units)
            _opts["xmin"] =    0
            _opts["xmax"] = 3000
            _cutBox       = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            _rebinX       = getBinningForTetrajetMass()
            if isinstance(_rebinX, list):
                _ylabel = "Events / bin"

    if "met" in histoName.lower():
        _units        = "GeV"
        _xlabel       = "E_{T}^{miss} (%s)" % (_units)
        _cutBox       = {"cutValue": 50.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
#        _opts         = {"xmin": 0.0, "xmax": 400.0, "ymin": 1e0, "ymax": 1e3}
        _rebinX = 2

#        myBins = []
#        for j in range(0, 100, 10):
#            myBins.append(j)
#        for k in range(100, 200, 20):
#            myBins.append(k)
#        for k in range(200, 300, 50):
#            myBins.append(k)
#        for k in range(300, 400+100, 100):
#            myBins.append(k)
#        _rebinX  = myBins #1
        # _ylabel      += " " + _units
#        binWmin, binWmax = GetBinWidthMinMax(myBins)
#        _ylabel = "Events / %.0f-%.0f %s" % (binWmin, binWmax, _units)

    if "tetrajetbjeteta" in histoName.lower():
        _units   = ""
        _xlabel  = "#eta"
        _cutBox  = {"cutValue": 0.8, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e0, "ymax": 1e3}
        _rebinX  = 1
        _ylabel  = "Events / %.2f"
                
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
        "ratioYlabel"      : "Ratio",
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
    style.setGridX(True)
    style.setGridY(True)

    optModes = [""]
    # For-loop: All opt Mode
    for opt in optModes:
        opts.optMode = opt

        # Numerator & Denominator dataset manager
        noSF_datasetsMgr            = GetDatasetsFromDir(opts, opts.noSFcrab)
        withQCDSF_datasetsMgr       = GetDatasetsFromDir(opts, opts.withQCDSFcrab)
        withEWKFakeTTSF_datasetsMgr = GetDatasetsFromDir(opts, opts.withEWKFakeTTSFcrab) 
        
        # Update all events to PU weighting
        noSF_datasetsMgr.updateNAllEventsToPUWeighted()
        withQCDSF_datasetsMgr.updateNAllEventsToPUWeighted()
        withEWKFakeTTSF_datasetsMgr.updateNAllEventsToPUWeighted()
        
        # Load Luminosities
        noSF_datasetsMgr.loadLuminosities()
        withQCDSF_datasetsMgr.loadLuminosities()
        withEWKFakeTTSF_datasetsMgr.loadLuminosities()
        
        if 0:
            noSF_datasetsMgr.PrintCrossSections()
            noSF_datasetsMgr.PrintLuminosities()
 
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(noSF_datasetsMgr) 
        plots.mergeRenameReorderForDataMC(withQCDSF_datasetsMgr) 
        plots.mergeRenameReorderForDataMC(withEWKFakeTTSF_datasetsMgr) 
        
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
            withQCDSF_datasetsMgr.remove(filter(lambda name: d in name, withQCDSF_datasetsMgr.getAllDatasetNames()))
            withEWKFakeTTSF_datasetsMgr.remove(filter(lambda name: d in name, withEWKFakeTTSF_datasetsMgr.getAllDatasetNames()))
            

        # Print summary of datasets to be used
        if 0:
            noSF_datasetsMgr.PrintInfo()
            withQCDSF_datasetsMgr.PrintInfo()
            withEWKFakeTTSF_datasetsMgr.PrintInfo()
            sys.exit()

        # Merge EWK samples
        EwkDatasets = ["Diboson", "DYJetsToLL", "WJetsHT"]#, "TTWJetsToLNu", "TTWJetsToQQ"]
        noSF_datasetsMgr.merge("EWK", EwkDatasets)
        withQCDSF_datasetsMgr.merge("EWK", EwkDatasets)
        withEWKFakeTTSF_datasetsMgr.merge("EWK", EwkDatasets)
        
        # Get histosgram names
        folderListIncl = withQCDSF_datasetsMgr.getDataset(withQCDSF_datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
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
        PlotHistos(noSF_datasetsMgr, withQCDSF_datasetsMgr, withEWKFakeTTSF_datasetsMgr, num_pathList, den_pathList,  opts)
        
    return

def getBinningForTetrajetMass(binLevel=0):
    '''
    Currenty in Combine:
    myBins = [0,50,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,
              760,780,800,820,840,860,880,900,920,940,960,980,1000,1020,1040,1060,1080,1100,1150,1200,1250,1300,1350,1400,1450,1500,1750,2000,2250,2500,
              2750,3000,3250,3500,3750,4000]
    '''
    myBins = []
    if binLevel == -1:
        myBins = [0.0, 4000.0]
    elif binLevel == 0: #default binning
        for i in range(0, 1000, 50):
            myBins.append(i)
        for i in range(1000, 2000, 100):
            myBins.append(i)
        for i in range(2000, 4000+500, 500):
            myBins.append(i)
    elif binLevel == 1: #finer binning
        for i in range(0, 1000, 25):
            myBins.append(i)
        for i in range(1000, 2000, 50):
            myBins.append(i)
        for i in range(2000, 4000+250, 250):
            myBins.append(i)
    elif binLevel == 2:
        for i in range(0, 1000, 20):
            myBins.append(i)
        for i in range(1000, 2000, 40):
            myBins.append(i)
        for i in range(2000, 4000+200, 200):
            myBins.append(i)
    elif binLevel == 3:
        for i in range(0, 1000, 10):
            myBins.append(i)
        for i in range(1000, 2000, 20):
            myBins.append(i)
        for i in range(2000, 4000+50, 50):
            myBins.append(i)
    else:
        raise Exception(ShellStyles.ErrorStyle() + "Please choose bin-level from -1 to 3" + ShellStyles.NormalStyle())

    return myBins

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
        
        # Subtract EWK + TT + SingleTop  to get QCD from Data
        rhDict["DataNoEWK-" + lIncl] = rhDict["Data-"+lIncl].Clone("DataNoEWK-" + lIncl) 
        rhDict["DataNoEWK-" + lIncl].Add(rhDict["EWK-" +lIncl], -1)
        
        rhDict["DataNoEWKNoSingleT-" + lIncl] = rhDict["DataNoEWK-" + lIncl].Clone("DataNoEWKNoSingleT-" + lIncl)
        rhDict["DataNoEWKNoSingleT-" + lIncl].Add(rhDict["SingleTop-"+lIncl], -1)
        
        rhDict["QCDinData-" + lIncl] = rhDict["DataNoEWKNoSingleT-" + lIncl].Clone("QCDinData-" + lIncl)
        rhDict["QCDinData-" + lIncl].Add(rhDict["TT-" + lIncl], -1)
        
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

def PlotHistos(noSF_datasetsMgr, withQCDSF_datasetsMgr, withEWKFakeTTSF_datasetsMgr, num_histoList, den_histoList,  opts):    
    
    # Get the histogram customisations (keyword arguments)
    _kwargs = GetHistoKwargs(num_histoList[0])
    
    # Get the root histos for all datasets and Control Regions (CRs)
    regions = ["SR", "VR", "CR1", "CR2"]
    
    #==========================================================================================
    # Get Dictionaries
    #==========================================================================================
    rhDict_num_noSF            = GetRootHistos(noSF_datasetsMgr, num_histoList, regions)
    rhDict_den_noSF            = GetRootHistos(noSF_datasetsMgr, den_histoList, regions)
    rhDict_num_withQCDSF       = GetRootHistos(withQCDSF_datasetsMgr      , num_histoList, regions)
    rhDict_num_withEWKFakeTTSF = GetRootHistos(withEWKFakeTTSF_datasetsMgr, num_histoList, regions)

    #=========================================================================================
    # Get Transfer Factor
    #=========================================================================================
    manager = SystTopBDTNormalization.SystTopBDTNormalizationManager(opts.noSFcrab, opts.optMode, verbose=False)
    manager.CalculateTransferFactor("Inclusive", rhDict_den_noSF["QCDinData-CR1-Inclusive"], rhDict_den_noSF["QCDinData-CR2-Inclusive"])
    
    # Get unique a style for each region
    for k in rhDict_den_noSF:
        dataset = k.split("-")[0]
        region  = k.split("-")[1]
        styles.getABCDStyle(region).apply(rhDict_den_noSF[k])
        if "Fake" in k:
            styles.getFakeBStyle().apply(rhDict_den_noSF[k])

    #=========================================================================================
    # Get the QCD data-driven histogram (denominator)
    #=========================================================================================
    rhDict_den_noSF["QCDdd-SR-Inclusive"] = rhDict_den_noSF["QCDinData-VR-Inclusive"].Clone("QCDdd-SR-Inclusive")
    rhDict_den_noSF["QCDdd-SR-Inclusive"].Reset()
    
    # Get the Verification Region (VR) histogram. Apply Transfer Factor (TF) to normalise according to the Signal Region (SR)
    binHisto_VR = rhDict_den_noSF["QCDinData-VR-Inclusive"]
    VRtoSR_TF   = manager.GetTransferFactor("Inclusive")
    Print("Applying TF = %s%0.6f%s to VR shape" % (ShellStyles.NoteStyle(), VRtoSR_TF, ShellStyles.NormalStyle()), True)
    binHisto_VR.Scale(VRtoSR_TF)
    rhDict_den_noSF["QCDdd-SR-Inclusive"].Add(binHisto_VR, +1)
    
    #==========================================================================================
    # Get the QCD MC histogram (denominator)
    #==========================================================================================
    # QCD Normalization factor for CR2: f =  (Data-EWK-SingleTop-TT)/(QCD MC)
    fNumerator   = rhDict_den_noSF["Data-CR2-Inclusive"].Integral() - (rhDict_den_noSF["TT-CR2-Inclusive"].Integral() + rhDict_den_noSF["EWK-CR2-Inclusive"].Integral() + rhDict_den_noSF["SingleTop-CR2-Inclusive"].Integral())
    fDenominator = rhDict_den_noSF["QCD-CR2-Inclusive"].Integral()
    f1 = (fNumerator)/(fDenominator) # Integral() != Integral(0, nBins+1) (the latter includes under/overflow bins)
    Print("The QCD normalization factor from CR2 is = %s%0.6f%s in SR" % (ShellStyles.NoteStyle(), f1, ShellStyles.NormalStyle()), True)
    rhDict_den_noSF["NormQCD-SR-Inclusive"] = rhDict_den_noSF["QCD-SR-Inclusive"].Clone("NormQCD-SR-Inclusive")
    rhDict_den_noSF["NormQCD-SR-Inclusive"].Scale(f1)

    # ============================================================
    # Get the normalization of TT in SR = Data- (EWK + f1*QCD + SingleTop)
    # ===========================================================
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"] = rhDict_den_noSF["Data-SR-Inclusive"].Clone("ForF2-TTinData-SR-Inclusive")
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"].Add(rhDict_den_noSF["EWK-SR-Inclusive"]       , -1)
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"].Add(rhDict_den_noSF["NormQCD-SR-Inclusive"]   , -1)
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"].Add(rhDict_den_noSF["SingleTop-SR-Inclusive"] , -1)
    
    # Get the histos
    h_InclusiveTT_Data = rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"]
    h_InclusiveTT_MC   = rhDict_den_noSF["TT-SR-Inclusive"]
        
    # Integrate data and MC
    nTT_SR_data = h_InclusiveTT_Data.Integral(0, h_InclusiveTT_Data.GetXaxis().GetNbins()+1)
    nTT_SR_MC   = h_InclusiveTT_MC.Integral(0, h_InclusiveTT_MC.GetXaxis().GetNbins()+1)
    # Get the normalisation factor by dividing the integrals
    f2 = float(nTT_SR_data)/float(nTT_SR_MC)

    # Apply styles
    styles.stStyle.apply(h_InclusiveTT_Data)
    styles.ttStyle.apply(h_InclusiveTT_MC)

    hTT_Data = histograms.Histo(h_InclusiveTT_Data, "tt (data)", "Data")
    hTT_Data.setIsDataMC(isData=True, isMC=False)

    # Scale the tt MC histogram
    h_InclusiveTT_MC.Scale(f2)
    hTT_MC =  histograms.Histo(h_InclusiveTT_MC, "tt (MC)", "TT")
    hTT_MC.setIsDataMC(isData=False, isMC=True)
    
    Print("The TT normalization factor from SR is = %s%0.6f%s in SR" % (ShellStyles.NoteStyle(), f2, ShellStyles.NormalStyle()), True)

    # Create sanity plot to check that normalisation of TT in data and TT in MC agree (normalisation correction)
    p = plots.ComparisonManyPlot(hTT_Data, [hTT_MC], saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    _kwargs["stackMCHistograms"] = False
    _kwargs["ratioYlabel"]       = "Data/MC "
    _kwargs["ratioInvert"]       = True

    # Draw the plot and save it
    hName = "Normalize_Inclusive_TT"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    # Reset options back to default values
    _kwargs["stackMCHistograms"] = True
    _kwargs["ratioYlabel"]       = "Ratio " 
    _kwargs["ratioInvert"]       = False
    
    # Save the the TT in denominator (normalized to Data-EWK-SingleTop-QCD) to the root-histo dictionary
    rhDict_den_noSF["NormTT-SR-Fake"] = rhDict_den_noSF["TT-SR-Fake"].Clone("NormTT-SR-Fake")
    rhDict_den_noSF["NormTT-SR-Fake"].Scale(f2)
    

    #=========================================================================================
    # Get all the denominators histograms for the efficiency calculation
    #=========================================================================================
    hDen_Data_SR        = rhDict_den_noSF["Data-SR-Inclusive"]
    hDen_SingleTop_SR   = rhDict_den_noSF["SingleTop-SR-Inclusive"]
    hDen_EWK_SR         = rhDict_den_noSF["EWK-SR-Inclusive"]
    hDen_QCDdd_SR       = rhDict_den_noSF["QCDdd-SR-Inclusive"]
    hDen_Norm_QCD_SR    = rhDict_den_noSF["NormQCD-SR-Inclusive"]
    hDen_Norm_FakeTT_SR = rhDict_den_noSF["NormTT-SR-Fake"]
    hDen_GenuineTT_SR   = rhDict_den_noSF["TT-SR-Genuine"]
    
    # ========================================================================================
    # Check normalisation of denominators (QCD data-driven and QCD MC)
    # ========================================================================================
    myStackList = []
    
    # Data
    hDen_Data = histograms.Histo(hDen_Data_SR, "Data", "Data")
    hDen_Data.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hDen_Data)
    
    # Fake TT
    styles.getFakeBStyle().apply(hDen_Norm_FakeTT_SR)
    hDen_FakeTT = histograms.Histo(hDen_Norm_FakeTT_SR, "t#bar{t} (fakes)", "Fake TT")
    hDen_FakeTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_FakeTT)
    
    # Genuine TT
    styles.genuineBStyle.apply(hDen_GenuineTT_SR)
    hDen_GenuineTT= histograms.Histo(hDen_GenuineTT_SR, "tt (genuine)")
    hDen_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_GenuineTT)
    
    # QCD (Data Driven)
    styles.altQCDStyle.apply(hDen_QCDdd_SR)
    hDen_QCDdd = histograms.Histo(hDen_QCDdd_SR, "QCD (data)")
    hDen_QCDdd.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_QCDdd)
    
    # Single Top
    hDen_SingleTop = histograms.Histo(hDen_SingleTop_SR, "SingleTop")
    hDen_SingleTop.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_SingleTop)
    
    # EWK
    styles.ewkFillStyle.apply(hDen_EWK_SR)
    plots._plotStyles["EWK"] = styles.getAltEWKStyle()
    hDen_EWK = histograms.Histo(hDen_EWK_SR, "EWK", "EWK")
    hDen_EWK.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_EWK)
    
    # Check if TT_fake + TT_genuine = TT (done. it is)
    if 0:
        myStackList = []
        hTT = histograms.Histo(h_InclusiveTT_MC, "t#bar{t}", "TT")
        hTT.setIsDataMC(isData=True, isMC=False)
        myStackList.insert(0, hTT)
        myStackList.append(hDen_FakeTT)
        myStackList.append(hDen_GenuineTT)
        _kwargs["stackMCHistograms"] = False

        styles.ewkFillStyle.apply(hDen_Norm_QCD_SR)
        hDen_QCDmc = histograms.Histo(hDen_Norm_QCD_SR, "QCD (MC)", legendStyle="P", drawStyle="AP")
        hDen_QCDmc.setIsDataMC(isData=False, isMC=True)
        print "QCD MC = ", hDen_Norm_QCD_SR.Integral()
        print "QCD Data = ", hDen_QCDdd_SR.Integral()
        p = plots.ComparisonManyPlot(hDen_QCDmc, [hDen_QCDdd], saveFormats=[])
        p.setLuminosity(opts.intLumi)
        p.setDefaultStyles()
        hName = "QCDdd_Vs_QCDmc"
        ROOT.gStyle.SetNdivisions(8, "X")
        plots.drawPlot(p, hName, **_kwargs)
        SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    # Create plot (QCD-data)
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    hName = "Denominator_LeadingTrijet_Pt_QCDdd"
    ROOT.gStyle.SetNdivisions(8, "X")
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    # Redo plot with QCD MC (normalised to data in CR2) instead of QCD Data
    hDen_QCDmc = histograms.Histo(hDen_Norm_QCD_SR, "QCD", "QCD")
    hDen_QCDmc.setIsDataMC(isData=False, isMC=True)

    myStackList = []
    myStackList.insert(0, hDen_Data)
    myStackList.append(hDen_FakeTT)
    myStackList.append(hDen_GenuineTT)
    myStackList.append(hDen_QCDmc)
    myStackList.append(hDen_SingleTop)
    myStackList.append(hDen_EWK)
    
    # Create plot (QCD MC)
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    hName = "Denominator_LeadingTrijet_Pt_QCDmc"
    _kwargs["rebinX"] = 1
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    #=========================================================================================
    # Get the numerator (QCD data-driven and QCD MC)
    #=========================================================================================
    # QCD data-driven
    rhDict_num_noSF["QCDdd-SR-Inclusive"] = rhDict_num_noSF["QCDinData-VR-Inclusive"].Clone("QCDdd-SR-Inclusive")
    rhDict_num_noSF["QCDdd-SR-Inclusive"].Reset()
    
    binHisto_VR = rhDict_num_noSF["QCDinData-VR-Inclusive"]
    VRtoSR_TF   = manager.GetTransferFactor("Inclusive")
    Print("Applying TF = %s%0.6f%s to VR shape" % (ShellStyles.NoteStyle(), VRtoSR_TF, ShellStyles.NormalStyle()), True)
    binHisto_VR.Scale(VRtoSR_TF)
    rhDict_num_noSF["QCDdd-SR-Inclusive"].Add(binHisto_VR, +1)
        
    # QCD MC
    rhDict_num_withQCDSF["NormQCD-SR-Inclusive"] = rhDict_num_withQCDSF["QCD-SR-Inclusive"].Clone()
    Print("The QCD normalization factor from CR2 is = %s%0.6f%s in SR" % (ShellStyles.NoteStyle(), f1, ShellStyles.NormalStyle()), True)
    rhDict_num_withQCDSF["NormQCD-SR-Inclusive"].Scale(f1)
    
    #==========================================================================================
    # Get the numerator (Fake-TT)
    #==========================================================================================
    rhDict_num_withEWKFakeTTSF["NormTT-SR-Fake"] = rhDict_num_withEWKFakeTTSF["TT-SR-Fake"].Clone()
    Print("The TT normalization factor from SR is = %s%0.6f%s in SR" % (ShellStyles.NoteStyle(), f2, ShellStyles.NormalStyle()), True)
    rhDict_num_withEWKFakeTTSF["NormTT-SR-Fake"].Scale(f2)
    
    # Get numerator and normalise to data
    hFakeTT_Numerator_normalized_noSF = rhDict_num_noSF["TT-SR-Fake"].Clone()
    hFakeTT_Numerator_normalized_noSF.Scale(f2)

    # Get denominator and normalise to data
    hFakeTT_Denominator_normalized = rhDict_den_noSF["TT-SR-Fake"].Clone()
    hFakeTT_Denominator_normalized.Scale(f2)
    
    #=========================================================================================
    # Numerators
    #=========================================================================================
    hNum_Data_SR        = rhDict_num_noSF["Data-SR-Inclusive"]
    hNum_SingleTop_SR   = rhDict_num_withQCDSF["SingleTop-SR-Inclusive"] # using the same SF as for QCD and EWK
    hNum_EWK_SR         = rhDict_num_withQCDSF["EWK-SR-Inclusive"]       # using the same SF as for QCD and Single Top    
    hNum_Norm_QCD_SR    = rhDict_num_withQCDSF["NormQCD-SR-Inclusive"]   # using the same SF as for EWK and Single Top
    hNum_QCDdd_SR       = rhDict_num_noSF["QCDdd-SR-Inclusive"] # data-driven
    hNum_Norm_FakeTT_SR = rhDict_num_withEWKFakeTTSF["NormTT-SR-Fake"]   # normalised by f2
    hNum_GenuineTT_SR   = rhDict_num_noSF["TT-SR-Genuine"]
    
    # Create empty list
    myStackList = []
    
    # Data
    hNum_Data = histograms.Histo(hNum_Data_SR, "Data", "Data")
    hNum_Data.setIsDataMC(isData=True, isMC=False)
    
    # Fake TT
    styles.getFakeBStyle().apply(hNum_Norm_FakeTT_SR)
    hNum_FakeTT = histograms.Histo(hNum_Norm_FakeTT_SR, "t#bar{t} (fakes)")
    hNum_FakeTT.setIsDataMC(isData=False, isMC=True)
    
    # Genuine TT
    styles.genuineBStyle.apply(hNum_GenuineTT_SR)
    hNum_GenuineTT= histograms.Histo(hNum_GenuineTT_SR, "t#bar{t} (genuine)") 
    hNum_GenuineTT.setIsDataMC(isData=False, isMC=True)
    
    # QCD (Data Driven)
    styles.altQCDStyle.apply(hNum_QCDdd_SR)
    hNum_QCDdd = histograms.Histo(hNum_QCDdd_SR, "QCD (data)")
    hNum_QCDdd.setIsDataMC(isData=False, isMC=True)
    
    # Single Top
    hNum_SingleTop = histograms.Histo(hNum_SingleTop_SR, "SingleTop")
    hNum_SingleTop.setIsDataMC(isData=False, isMC=True)
    
    # EWK
    hNum_EWK = histograms.Histo(hNum_EWK_SR, "EWK", "EWK")
    hNum_EWK.setIsDataMC(isData=False, isMC=True)
    
    # Create plot (QCD-data)
    myStackList.insert(0, hNum_Data)
    myStackList.append(hNum_FakeTT)
    myStackList.append(hNum_GenuineTT)
    myStackList.append(hNum_SingleTop)
    myStackList.append(hNum_QCDdd)
    myStackList.append(hNum_EWK)

    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    _kwargs["rebinX"] = 2
    hName = "Numerator_LeadingTrijet_Pt_QCDdd"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    # Redo plot with QCD MC (normalised to data in CR2) instead of QCD Data
    hNum_QCDmc = histograms.Histo(hNum_Norm_QCD_SR, "QCD", "QCD")
    hNum_QCDmc.setIsDataMC(isData=False, isMC=True)

    myStackList = []
    myStackList.insert(0, hNum_Data)
    myStackList.append(hNum_FakeTT)
    myStackList.append(hNum_GenuineTT)
    myStackList.append(hNum_SingleTop)
    myStackList.append(hNum_QCDmc)
    myStackList.append(hNum_EWK)
    
    # Create plot (QCD MC)
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    hName = "Numerator_LeadingTrijet_Pt_QCDmc"
    _kwargs["rebinX"] = 1
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # ================================================
    # Estimate Genuine TT in SR from data: TT_Genuine = Data - (EWK + SingleTop + TT_Fake + QCD)
    # ================================================
    # Denominator (=Before BDT cut)
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"] = hDen_Data_SR.Clone("TTinData-SR-Genuine-withQCD")

    # Subtract Single Top + EWK + TT_Fake
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Add(hDen_SingleTop_SR,    -1)
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Add(hDen_EWK_SR,          -1)
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Add(hDen_Norm_FakeTT_SR,  -1)

    # Subtract QCD (data)
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDdd"] = rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDdd")
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDdd"].Add(hDen_QCDdd_SR, -1)
    
    # Subtract QCD (MC)
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDmc"] = rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDmc")
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDmc"].Add(hDen_Norm_QCD_SR, -1)
    
    # Get the histograms
    hDen_GenuineTTinData_SR_QCDdd = rhDict_den_noSF["TTinData-SR-Genuine-noQCDdd"]
    hDen_GenuineTTinData_SR_QCDmc = rhDict_den_noSF["TTinData-SR-Genuine-noQCDmc"]

    # Data - (EWK  + SingleTop + TT_Fake + QCD data)
    #styles.getFakeBStyle().apply(hDen_GenuineTTinData_SR_QCDdd)
    styles.getABCDStyle("CR2").apply(hDen_GenuineTTinData_SR_QCDdd)
    hDen_Data_QCDdd = histograms.Histo(hDen_GenuineTTinData_SR_QCDdd, "Data - (EWK+ST+QCDdd)", legendStyle="P", drawStyle="AP")
    hDen_Data_QCDdd.setIsDataMC(isData=True, isMC=False)

    # Data - (EWK  + SingleTop + TT_Fake + QCD MC)
    #styles.altQCDStyle.apply(hDen_GenuineTTinData_SR_QCDmc)
    styles.getABCDStyle("SR").apply(hDen_GenuineTTinData_SR_QCDmc)
    hDen_Data_QCDmc = histograms.Histo(hDen_GenuineTTinData_SR_QCDmc, "Data - (EWK+ST+QCDmc)", legendStyle="P", drawStyle="AP")
    hDen_Data_QCDmc.setIsDataMC(isData=True, isMC=False)

    # TT Genuine
    #styles.genuineBStyle.apply(hDen_GenuineTT_SR)
    styles.getABCDStyle("CR4").apply(hDen_GenuineTT_SR)
    hDen_GenuineTT = histograms.Histo(hDen_GenuineTT_SR, "t#bar{t} genuine", legendStyle="F", drawStyle="HIST")
    hDen_GenuineTT.setIsDataMC(isData=False, isMC=True)

    # Options
    _kwargs["stackMCHistograms"] = False
    _kwargs["ratio"]             = False
    _kwargs["ratioYlabel"]       = "Ratio " 
    _kwargs["ratioInvert"]       = False
    _kwargs["createLegend"]      = {"x1": 0.46, "y1": 0.70, "x2": 0.95, "y2": 0.92}
    _kwargs["rebinX"]            = 2

    # Create plot (QCD data)
    hName  = "Denominator_LeadingTrijet_Pt_GenuineTT"
    p = plots.ComparisonManyPlot(hDen_Data_QCDmc, [hDen_Data_QCDdd, hDen_GenuineTT], saveFormats=[])
    #p = plots.ComparisonManyPlot(hDen_Data_QCDdd, [hDen_GenuineTT, hDen_Data_QCDmc], saveFormats=[])
    #p = plots.ComparisonManyPlot(hDen_GenuineTT, [hDen_Data_QCDdd, hDen_Data_QCDmc], saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    # Numerator (=After BDT cut)
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"] = hNum_Data_SR.Clone("TTinData-SR-Genuine-withQCD")    
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Add(hNum_SingleTop_SR, -1)
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Add(hNum_EWK_SR, -1)
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Add(hNum_Norm_FakeTT_SR, -1)
    
    # Subtract QCD (data)
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDdd"] = rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDdd")
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDdd"].Add(hNum_QCDdd_SR, -1)
    
    # Subtract QCD (MC)
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDmc"] = rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDmc")
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDmc"].Add(hNum_Norm_QCD_SR, -1)
    
    # Get the histograms    
    hNum_GenuineTTinData_SR_QCDdd = rhDict_num_noSF["TTinData-SR-Genuine-noQCDdd"]
    hNum_GenuineTTinData_SR_QCDmc = rhDict_num_noSF["TTinData-SR-Genuine-noQCDmc"]

    # Data - (EWK  + SingleTop + TT_Fake + QCD data)
    styles.getABCDStyle("CR2").apply(hNum_GenuineTTinData_SR_QCDdd)
    hNum_Data_QCDdd = histograms.Histo(hNum_GenuineTTinData_SR_QCDdd, "Data - (EWK+ST+QCDdd)", legendStyle="P", drawStyle="AP")
    hNum_Data_QCDdd.setIsDataMC(isData=True, isMC=False)

    # Data - (EWK  + SingleTop + TT_Fake + QCD MC)
    styles.getABCDStyle("SR").apply(hNum_GenuineTTinData_SR_QCDmc)
    hNum_Data_QCDmc = histograms.Histo(hNum_GenuineTTinData_SR_QCDmc, "Data - (EWK+ST+QCDmc)", legendStyle="P", drawStyle="AP")
    hNum_Data_QCDmc.setIsDataMC(isData=True, isMC=False)

    # TT Genuine
    styles.getABCDStyle("CR4").apply(hNum_GenuineTT_SR)
    hNum_GenuineTT = histograms.Histo(hNum_GenuineTT_SR, "t#bar{t} genuine", legendStyle="F", drawStyle="HIST")
    hNum_GenuineTT.setIsDataMC(isData=False, isMC=True)

    # Create plot (QCD data)
    hName  = "Numerator_LeadingTrijet_Pt_GenuineTT"
    _kwargs["rebinX"] = 2
    p = plots.ComparisonManyPlot(hNum_Data_QCDmc, [hNum_Data_QCDdd, hNum_GenuineTT], saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    
    # ================================================
    # Estimate Fake TT in SR from data: TT_Genuine = Data - (EWK + SingleTop + TT_Fake + QCD)
    # ================================================
    # Denominator (=Before BDT cut)
    styles.getFakeBStyle().apply(hFakeTT_Numerator_normalized_noSF)
    hNum_FakeTT_noSF = histograms.Histo(hFakeTT_Numerator_normalized_noSF, "t#bar{t} fakes (no SF)")
    hNum_FakeTT_noSF.setIsDataMC(isData=False, isMC=True)
    
    styles.getABCDStyle("CR2").apply(hNum_Norm_FakeTT_SR)
    hNum_FakeTT_withSF = histograms.Histo(hNum_Norm_FakeTT_SR, "t#bar{t} fakes (with SF)", legendStyle="P", drawStyle="AP")
    hNum_FakeTT_withSF.setIsDataMC(isData=False, isMC=True)
    
    myStackList = []
    myStackList.insert(0, hNum_Data)
    myStackList.append(hNum_FakeTT_noSF)
    myStackList.append(hNum_FakeTT_withSF)
    
    # Create plot (Fake TT Denominator)
    _kwargs["stackMCHistograms"] = False
    _kwargs["ratio"]             = True
    _kwargs["ratioYlabel"]       = "SF" 
    _kwargs["ratioInvert"]       = True
    _kwargs["createLegend"]      = {"x1": 0.62, "y1": 0.70, "x2": 0.95, "y2": 0.92}
    _kwargs["rebinX"]            = 10
    p = plots.ComparisonManyPlot(hNum_FakeTT_withSF, [hNum_FakeTT_noSF], saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    hName  = "Numerator_LeadingTrijet_Pt_SF"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # ================================================
    # Create Efficiency Graphs
    # ================================================
    _kwargs = {
        "xlabel"           : "p_{T} (GeV/c)",
        "ylabel"           : "Efficiency",
        "ratioYlabel"      : "Ratio ", 
        "ratio"            : False,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.2},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : False,
        "createLegend"     : {"x1": 0.64, "y1": 0.82, "x2": 0.95, "y2": 0.92},
        }

    # Definitions
    nx    = 8
    bins  = [0, 100, 200, 300, 400, 500, 600]
    xBins = array.array('d', bins)
    nx    = len(xBins)-1

    # Efficiency in Data (using the QCD Data)
    hNum_GenuineTTinData_SR_QCDdd = hNum_GenuineTTinData_SR_QCDdd.Rebin(nx, "", xBins)
    hDen_GenuineTTinData_SR_QCDdd = hDen_GenuineTTinData_SR_QCDdd.Rebin(nx, "", xBins)
    
    # Calculate the efficiency
    hNum, hDen = GetHistosForEfficiency(hNum_GenuineTTinData_SR_QCDdd, hDen_GenuineTTinData_SR_QCDdd) # Bug-fix
    eff_Data_QCDdd = ROOT.TEfficiency(hNum, hDen)
    # eff_Data_QCDdd = ROOT.TEfficiency(hNum_GenuineTTinData_SR_QCDdd, hDen_GenuineTTinData_SR_QCDdd) #does not work
    eff_Data_QCDdd.SetStatisticOption(ROOT.TEfficiency.kFCP)
    for i in range(0, nx+1):
        if 0:
            print "eff = ", eff_Data_QCDdd.GetEfficiency(i)
        else:
            pass
    gEff_Data_QCDdd = convert2TGraph(eff_Data_QCDdd)
    Graph_Data_QCDdd = histograms.HistoGraph(gEff_Data_QCDdd, "t#bar{t} genuine (Data) ", "p", "P")


    # Efficiency in Data (using the QCD MC)
    hNum_GenuineTTinData_SR_QCDmc = hNum_GenuineTTinData_SR_QCDmc.Rebin(nx, "", xBins)
    hDen_GenuineTTinData_SR_QCDmc = hDen_GenuineTTinData_SR_QCDmc.Rebin(nx, "", xBins)
    hNum, hDen = GetHistosForEfficiency(hNum_GenuineTTinData_SR_QCDmc, hDen_GenuineTTinData_SR_QCDmc) # Bug-fix
    #eff_Data_QCDmc = ROOT.TEfficiency(hNum_GenuineTTinData_SR_QCDmc, hDen_GenuineTTinData_SR_QCDmc)
    eff_Data_QCDmc = ROOT.TEfficiency(hNum, hDen)
    eff_Data_QCDmc.SetStatisticOption(ROOT.TEfficiency.kFCP)
    gEff_Data_QCDmc = convert2TGraph(eff_Data_QCDmc)
    styles.dataStyle.apply(gEff_Data_QCDmc)
    Graph_Data_QCDmc = histograms.HistoGraph(gEff_Data_QCDmc, "t#bar{t} genuine (Data) ", "p", "P")

    
    # Efficiency in Genuine TT MC
    hNum_GenuineTT_SR = hNum_GenuineTT_SR.Rebin(nx, "", xBins)
    hDen_GenuineTT_SR = hDen_GenuineTT_SR.Rebin(nx, "", xBins)
    eff_GenuineTT = ROOT.TEfficiency(hNum_GenuineTT_SR, hDen_GenuineTT_SR)
    eff_GenuineTT.SetStatisticOption(ROOT.TEfficiency.kFCP)
    gEff_GenuineTT = convert2TGraph(eff_GenuineTT)
    styles.ttStyle.apply(gEff_GenuineTT)
    Graph_GenuineTT = histograms.HistoGraph(gEff_GenuineTT, "t#bar{t} genuine (MC)", "p", "P")
    
    # Efficiency in FakeTT
    hNum_Norm_FakeTT_SR = hNum_Norm_FakeTT_SR.Rebin(nx, "", xBins)
    hDen_Norm_FakeTT_SR = hDen_Norm_FakeTT_SR.Rebin(nx, "", xBins)
    eff_FakeTT = ROOT.TEfficiency(hNum_Norm_FakeTT_SR, hDen_Norm_FakeTT_SR)
    eff_FakeTT.SetStatisticOption(ROOT.TEfficiency.kFCP)
    gEff_FakeTT = convert2TGraph(eff_FakeTT)
    styles.getABCDStyle("SR").apply(gEff_FakeTT)
    Graph_FakeTT = histograms.HistoGraph(gEff_FakeTT, "t#bar{t} (fakes)", "p", "P")

    # Efficiency in EWK
    hNum_EWK_SR = hNum_EWK_SR.Rebin(nx, "", xBins)
    hDen_EWK_SR = hDen_EWK_SR.Rebin(nx, "", xBins)
    eff_EWK = ROOT.TEfficiency(hNum_EWK_SR, hDen_EWK_SR)
    eff_EWK.SetStatisticOption(ROOT.TEfficiency.kFCP)
    gEff_EWK = convert2TGraph(eff_EWK)
    styles.genuineBStyle.apply(gEff_EWK)
    Graph_EWK =  histograms.HistoGraph(gEff_EWK, "EWK", "p", "P")

    # Efficiency in QCD (Normalized MC)
    hNum_Norm_QCD_SR = hNum_Norm_QCD_SR.Rebin(nx, "", xBins)
    hDen_Norm_QCD_SR = hDen_Norm_QCD_SR.Rebin(nx, "", xBins)
    eff_QCDmc = ROOT.TEfficiency(hNum_Norm_QCD_SR, hDen_Norm_QCD_SR)
    eff_QCDmc.SetStatisticOption(ROOT.TEfficiency.kFCP)
    gEff_QCDmc = convert2TGraph(eff_QCDmc)
    styles.qcdStyle.apply(gEff_QCDmc)
    Graph_QCDmc = histograms.HistoGraph(gEff_QCDmc, "QCD (MC)", "p", "P")

    # Efficiency in QCD (Data-Driven)
    hNum_QCDdd_SR = hNum_QCDdd_SR.Rebin(nx, "", xBins)
    hDen_QCDdd_SR = hDen_QCDdd_SR.Rebin(nx, "", xBins)
    eff_QCDdd = ROOT.TEfficiency(hNum_QCDdd_SR, hDen_QCDdd_SR)
    eff_QCDdd.SetStatisticOption(ROOT.TEfficiency.kFCP)
    gEff_QCDdd = convert2TGraph(eff_QCDdd)
    styles.fakeBStyle.apply(gEff_QCDdd)
    Graph_QCDdd = histograms.HistoGraph(gEff_QCDdd, "QCD (data)", "p", "P")

    # Efficiency in Single Top
    hNum_SingleTop_SR = hNum_SingleTop_SR.Rebin(nx, "", xBins)
    hDen_SingleTop_SR = hDen_SingleTop_SR.Rebin(nx, "", xBins)
    eff_ST =  ROOT.TEfficiency(hNum_SingleTop_SR, hDen_SingleTop_SR)
    eff_ST.SetStatisticOption(ROOT.TEfficiency.kFCP)
    gEff_ST = convert2TGraph(eff_ST)
    styles.stStyle.apply(gEff_ST)
    Graph_ST = histograms.HistoGraph(gEff_ST, "Single t", "p", "P")

    # ================================================
    # Plot Misidentification for different samples
    # ================================================
    _kwargs["binList"] = xBins
    _kwargs["ratio"]   = True
    _kwargs["ylabel"]  = "Misidentification rate" 
    _kwargs["xlabel"]  = "p_{T} (GeV/c)"

    # Plot Mis-identification rates
    p = plots.ComparisonManyPlot(Graph_EWK, [Graph_FakeTT, Graph_QCDdd, Graph_QCDmc, Graph_ST], saveFormats=[])
    saveName = "Misidentification_LeadingTrijet_Pt"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])

    # ================================================
    # Plot Efficiency for Genuine TT
    # ================================================
    # Using QCD from data
    _kwargs["ylabel"] = "Efficiency"
    p = plots.ComparisonManyPlot(Graph_Data_QCDdd, [Graph_GenuineTT], saveFormats=[])
    saveName = "Efficiency_LeadingTrijet_Pt_QCDdd"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])

    # Using QCD from MC
    p = plots.ComparisonManyPlot(Graph_Data_QCDmc, [Graph_GenuineTT], saveFormats=[])
    saveName = "Efficiency_LeadingTrijet_Pt_QCDmc"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])
    sys.exit()

#    ##### test 
#    # iro
#    hNum_GenuineTTinData_SR = hNum_Data_SR.Rebin(nx, "", xBins)
#    #hNum_GenuineTTinData_SR = hNum_GenuineTTinData_SR_QCDddData_SR.Rebin(nx, "", xBins)
#    hDen_GenuineTTinData_SR = hDen_Data_SR.Rebin(nx, "", xBins)
#    
#    eff_GenuineTTinData = ROOT.TEfficiency(hNum_GenuineTTinData_SR, hDen_GenuineTTinData_SR)
#    eff_GenuineTTinData.SetStatisticOption(ROOT.TEfficiency.kFCP)
#    
#    gEff_GenuineTTinData = convert2TGraph(eff_GenuineTTinData)
#    styles.dataStyle.apply(gEff_GenuineTTinData)
#    Graph_GenuineTTinData = histograms.HistoGraph(gEff_GenuineTTinData, "Genuine TT (data)", "p", "P")
#
#    _kwargs["ratio"]  = True        
#    _kwargs["ylabel"] = "Efficiency"
#    
#    # Plot the efficiency
#    p = plots.ComparisonManyPlot(Graph_GenuineTTinData, [Graph_GenuineTT], saveFormats=[])
#    
#    saveName = "Efficiency_DataVsMC"
#    savePath = os.path.join(opts.saveDir, opts.optMode)
#    
#    ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")
#    units = "GeV/c"
#    _kwargs["xlabel"] = "p_{T} (%s)" % (units)
#    
#    plots.drawPlot(p, savePath, **_kwargs)
#    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])
#
    ##### test



    
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
                      help="Path to the numerator multicrab directory for input")
    
    parser.add_option("--withQCDSF", dest="withQCDSFcrab", action="store",
                      help="Path to the numerator multicrab directory for input")
    
    parser.add_option("--withEWKFakeTTSF", dest="withEWKFakeTTSFcrab", action="store",
                      help="Path to the denominator multicrab directory for input")
    
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
    if opts.noSFcrab == None or opts.withQCDSFcrab == None or opts.withEWKFakeTTSFcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
        
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.noSFcrab, prefix="", postfix="")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== getEfficiencies.py: Press any key to quit ROOT ...")
