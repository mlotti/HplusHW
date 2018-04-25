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
./getEfficiencies_withQCDdd.py -num <pseudo_nummcrab_directory> -den <pseudo_dencrab_directory> [opts]


EXAMPLES: 


LAST USED:
./getEfficiencies_withQCDdd.py --noSF SystTopBDT_180422_MET50_MuIso0p1_InvMET30_InvMuIso0p2_noSF --withQCDSF SystTopBDT_180417_102133_noSF_withTopPtRew --withEWKFakeTTSF SystTopBDT_180417_035158_withSF_withTopPtRew -e "TTWJetsToLNu_|TTWJetsToQQ" --url

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
import HiggsAnalysis.FakeBMeasurement.QCDInvertedResult as fakeBResult

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
        print "i=", i, " x=", h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i), "  Efficiency=", tefficiency.GetEfficiency(i)
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
        "createLegend"     : {"x1": 0.70, "y1": 0.70, "x2": 0.95, "y2": 0.92},
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
    Verbose("Getting datasets")
    
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
    style.setOptStat(True)
    style.setGridX(True)
    style.setGridY(True)
    
    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.noSFcrab)

    # Get list of eras, modes, and optimisation modes
    erasList      = dsetMgrCreator.getDataEras()
    modesList     = dsetMgrCreator.getSearchModes()
    optList       = dsetMgrCreator.getOptimizationModes()
    sysVarList    = dsetMgrCreator.getSystematicVariations()
    sysVarSrcList = dsetMgrCreator.getSystematicVariationSources()
        
    # If user does not define optimisation mode do all of them
    if opts.optMode == None:
        if len(optList) < 1:
            optList.append("")
        optModes = optList
    else:
        optModes = [opts.optMode]

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
        
        if 0:#opts.verbose:
            noSF_datasetsMgr.PrintCrossSections()
            noSF_datasetsMgr.PrintLuminosities()
 
        # Get the PSets:
        if 0:
            noSF_datasetsMgr.printSelections()
            noSF_datasetsMgr.PrintInfo()
        
        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(noSF_datasetsMgr) 
        plots.mergeRenameReorderForDataMC(withQCDSF_datasetsMgr) 
        plots.mergeRenameReorderForDataMC(withEWKFakeTTSF_datasetsMgr) 
        
        # Get luminosity if a value is not specified
        if opts.intLumi < 0:
            opts.intLumi = noSF_datasetsMgr.getDataset("Data").getLuminosity()
            
        # Remove datasets
        removeList = ["TTWJetsToLNu_", "TTWJetsToQQ"]
#        if not opts.useMC:
#            removeList.append("QCD")
        for i, d in enumerate(removeList, 0):
            msg = "Removing dataset %s" % d
            Verbose(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
            noSF_datasetsMgr.remove(filter(lambda name: d in name, noSF_datasetsMgr.getAllDatasetNames()))
            withQCDSF_datasetsMgr.remove(filter(lambda name: d in name, withQCDSF_datasetsMgr.getAllDatasetNames()))
            withEWKFakeTTSF_datasetsMgr.remove(filter(lambda name: d in name, withEWKFakeTTSF_datasetsMgr.getAllDatasetNames()))
            

        # Print summary of datasets to be used
        if 0:
            print "No SF datasets:"
            noSF_datasetsMgr.PrintInfo()
            print "With QCD SF datasets:"
            withQCDSF_datasetsMgr.PrintInfo()
            
        # Merge EWK samples
        EwkDatasets = ["Diboson", "DYJetsToLL", "WJetsHT"]
        noSF_datasetsMgr.merge("EWK", EwkDatasets)
        withQCDSF_datasetsMgr.merge("EWK", EwkDatasets)
        withEWKFakeTTSF_datasetsMgr.merge("EWK", EwkDatasets)
        
        # Print dataset information
        if 1:
            noSF_datasetsMgr.PrintInfo()
            #withQCDSF_datasetsMgr.PrintInfo()
            #withEWKFakeTTSF_datasetsMgr.PrintInfo()
        
        # Do the fit on the histo after ALL selections (incl. topology cuts)
        folderListIncl = withQCDSF_datasetsMgr.getDataset(withQCDSF_datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        folderList = [h for h in folderListIncl if "AfterAllSelections_LeadingTrijet_Pt" in h ]
        
        for h in folderList:
            if "lowMET" in h:
                folderList.remove(h)
        
        folderPath = os.path.join(opts.folder, "")
        folderPathGen = os.path.join(opts.folder+"Genuine", "")
        folderPathFake =os.path.join(opts.folder+"Fake", "")
        
        histoList = folderList
        num_pathList = [os.path.join(folderPath, h) for h in histoList]
        num_pathList.extend([os.path.join(folderPathGen, h) for h in histoList])
        num_pathList.extend([os.path.join(folderPathFake, h) for h in histoList])
        
        # Denominator Histogram (To be used in the estimation of QCD Data-Driven)
        histoList = [h for h in folderListIncl if "AfterStandardSelections_LeadingTrijet_Pt" in h]
        den_pathList = [os.path.join(folderPath, h) for h in histoList]
        den_pathList.extend([os.path.join(folderPathGen, h) for h in histoList])
        den_pathList.extend([os.path.join(folderPathFake, h) for h in histoList])
        
        for h in den_pathList:
            if "lowMET" in h:
                den_pathList.remove(h)
        
                
        PlotHistosAndCalculateTF(noSF_datasetsMgr, withQCDSF_datasetsMgr, withEWKFakeTTSF_datasetsMgr, num_pathList, den_pathList,  opts)
        
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

def PlotHistosAndCalculateTF(noSF_datasetsMgr, withQCDSF_datasetsMgr, withEWKFakeTTSF_datasetsMgr, num_histoList, den_histoList,  opts):    
    
    Print("====== PlotHistosAndCalculateTF")
    
    # Get the histogram customisations (keyword arguments)
    _kwargs = GetHistoKwargs(num_histoList[0])
    
    # Get the root histos for all datasets and Control Regions (CRs)
    regions = ["SR", "VR", "CR1", "CR2"]
    
    print "Numerator List = ", num_histoList
    print "Denominator List = ", den_histoList


    #==========================================================================================
    # Get Dictionaries
    #==========================================================================================
    Print("Get Denominator Dictionary with Histograms")
    rhDict_den_noSF = GetRootHistos(noSF_datasetsMgr, den_histoList, regions)
    
    #Print("Get Numerator Dictionary with Histograms from the pseudomulticrab with QCD SF APPLIED")
    rhDict_num_withQCDSF = GetRootHistos(withQCDSF_datasetsMgr, num_histoList, regions)
    
    #Print("Get Numerator Dictionary with Histograms from the pseudomulticrab with EWK & Fake TT SF APPLIED")
    rhDict_num_withEWKFakeTTSF = GetRootHistos(withEWKFakeTTSF_datasetsMgr, num_histoList, regions)
    
    #Print("Get Numerator Dictionary with Histograms from the pseudomulticrab with no SF NOT APPLIED")
    rhDict_num_noSF = GetRootHistos(noSF_datasetsMgr, num_histoList, regions)
    
    #=========================================================================================
    # Normalization Factors
    #=========================================================================================
    f1 = 0.611351   # QCD Normalization factor

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
    # Get the QCD in denominator  -  Data Driven
    #=========================================================================================
    rhDict_den_noSF["QCDdd-SR-Inclusive"] = rhDict_den_noSF["QCDinData-VR-Inclusive"].Clone("QCDdd-SR-Inclusive")
    rhDict_den_noSF["QCDdd-SR-Inclusive"].Reset()
    
    binHisto_VR = rhDict_den_noSF["QCDinData-VR-Inclusive"]
    VRtoSR_TF   = manager.GetTransferFactor("Inclusive")
    Print("Applying TF = %s%0.6f%s to VR shape" % (ShellStyles.NoteStyle(), VRtoSR_TF, ShellStyles.NormalStyle()), True)
    binHisto_VR.Scale(VRtoSR_TF)
    rhDict_den_noSF["QCDdd-SR-Inclusive"].Add(binHisto_VR, +1)
    # => rhDict_den_noSF["QCDdd-SR-Inclusive"] is the QCD Data Driven Estimation in SR
    
    
    #==========================================================================================
    # Get the QCD in denominator - Normalized MC
    #==========================================================================================
    rhDict_den_noSF["NormQCD-SR-Inclusive"] = rhDict_den_noSF["QCD-SR-Inclusive"].Clone("NormQCD-SR-Inclusive")
    rhDict_den_noSF["NormQCD-SR-Inclusive"].Scale(f1)
    # => rhDict_den_noSF["NormQCD-SR-Inclusive"] is the QCD MC Estimation (Normalized by a factor f1)

    # ============================================================
    # Get the normalization of TT subtracting now Single Top
    # ===========================================================
    #  f2 = 0.940785   # OLD TT Normalization factor
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"] = rhDict_den_noSF["Data-SR-Inclusive"].Clone("ForF2-TTinData-SR-Inclusive")
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"].Add(rhDict_den_noSF["EWK-SR-Inclusive"]       , -1)
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"].Add(rhDict_den_noSF["NormQCD-SR-Inclusive"]   , -1)
    rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"].Add(rhDict_den_noSF["SingleTop-SR-Inclusive"] , -1)
    
    h_InclusiveTT_Data = rhDict_den_noSF["ForF2-TTinData-SR-Inclusive"]
    h_InclusiveTT_MC   = rhDict_den_noSF["TT-SR-Inclusive"]
        
    styles.stStyle.apply(h_InclusiveTT_Data)
    hTT_Data = histograms.Histo(h_InclusiveTT_Data, "TT (Data)", "Data")
    hTT_Data.setIsDataMC(isData=True, isMC=False)
    
    styles.ttStyle.apply(h_InclusiveTT_MC)
    hTT_MC =  histograms.Histo(h_InclusiveTT_MC, "TT (MC)", "TT")
    hTT_MC.setIsDataMC(isData=False, isMC=True)
    
    nTT_SR_data = h_InclusiveTT_Data.Integral(0, h_InclusiveTT_Data.GetXaxis().GetNbins()+1)
    nTT_SR_MC   = h_InclusiveTT_MC.Integral(0, h_InclusiveTT_MC.GetXaxis().GetNbins()+1)

    f2 = float(nTT_SR_data)/float(nTT_SR_MC)
    Print("TT Normalization factor: = %s%0.6f%s in SR" % (ShellStyles.NoteStyle(), f2, ShellStyles.NormalStyle()), True)
    
    # Create plot
    p = plots.ComparisonManyPlot(hTT_Data, [hTT_MC], saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()

    _kwargs["stackMCHistograms"] = False
    _kwargs["ratioInvert"] = True
    
    # Draw the plot and save it
    hName = "Normalize_Inclusive_TT"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    _kwargs["ratioInvert"] = False
    _kwargs["stackMCHistograms"] = True
    
    
    # ===========================================================================================
    # Get the TT in denominator - Normalized TT
    # ===========================================================================================    
    rhDict_den_noSF["NormTT-SR-Fake"] = rhDict_den_noSF["TT-SR-Fake"].Clone("NormTT-SR-Fake")
    rhDict_den_noSF["NormTT-SR-Fake"].Scale(f2)
    
    #=========================================================================================
    # Denominator (Data, EWK, Normalized QCD, Normalized Fake TT, Genuine TT)
    #=========================================================================================
    # Data
    hDen_Data_SR        = rhDict_den_noSF["Data-SR-Inclusive"]
    # Single Top (no SF or Normalization factor applied)
    hDen_SingleTop_SR   = rhDict_den_noSF["SingleTop-SR-Inclusive"]
    # EWK (no SF or Normalization factor applied)
    hDen_EWK_SR         = rhDict_den_noSF["EWK-SR-Inclusive"]
    # QCD (Data Driven)
    hDen_QCDdd_SR       = rhDict_den_noSF["QCDdd-SR-Inclusive"]
    # QCD (Normalized Factor)
    hDen_Norm_QCD_SR    = rhDict_den_noSF["NormQCD-SR-Inclusive"]
    # Fake TT (Normalized by factor f2)
    hDen_Norm_FakeTT_SR = rhDict_den_noSF["NormTT-SR-Fake"]
    # Genuine TT
    hDen_GenuineTT_SR   = rhDict_den_noSF["TT-SR-Genuine"]
    
    # ========================================================================================
    # Plot Denominator - with QCD Data-Driven
    # ========================================================================================
    # Create empty histogram stack list
    _kwargs["stackMCHistograms"] = True
    myStackList = []
    
    # Data
    hDen_Data = histograms.Histo(hDen_Data_SR, "Data", "Data")
    hDen_Data.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hDen_Data)
    
    # Fake TT
    hDen_FakeTT = histograms.Histo(hDen_Norm_FakeTT_SR, "Fake TT", "Fake TT")
    hDen_FakeTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_FakeTT)
    
    # Genuine TT
    hDen_GenuineTT= histograms.Histo(hDen_GenuineTT_SR, "TT", "Genuine TT")
    hDen_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_GenuineTT)
    
    # QCD (Data Driven)
    hDen_QCDdd = histograms.Histo(hDen_QCDdd_SR, "QCD (Data)", "QCD")
    hDen_QCDdd.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_QCDdd)
    
    # Single Top
    hDen_SingleTop = histograms.Histo(hDen_SingleTop_SR, "ST", "ST")
    hDen_SingleTop.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_SingleTop)
    
    # EWK
    hDen_EWK = histograms.Histo(hDen_EWK_SR, "EWK", "EWK")
    hDen_EWK.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_EWK)
    
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    
    # Draw the plot and save it
    hName = "Denominator_LeadingTrijet_Pt_QCDdd"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # ========================================================================================
    # Plot Denominator - with QCD MC Normalized 
    # ========================================================================================
    # Create empty histogram stack list
    myStackList = []
    
    # Data
    hDen_Data = histograms.Histo(hDen_Data_SR, "Data", "Data")
    hDen_Data.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hDen_Data)
    
    # Fake TT
    hDen_FakeTT = histograms.Histo(hDen_Norm_FakeTT_SR, "Fake TT", "Fake TT")
    hDen_FakeTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_FakeTT)
    
    # Genuine TT
    hDen_GenuineTT= histograms.Histo(hDen_GenuineTT_SR, "TT", "Genuine TT")
    hDen_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_GenuineTT)
    
    # QCD (Normalized MC)
    hDen_QCDmc = histograms.Histo(hDen_Norm_QCD_SR, "QCD", "QCD")
    hDen_QCDmc.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_QCDmc)
    
    # Single Top
    hDen_SingleTop = histograms.Histo(hDen_SingleTop_SR, "ST", "ST")
    hDen_SingleTop.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_SingleTop)
    
    # EWK
    hDen_EWK = histograms.Histo(hDen_EWK_SR, "EWK", "EWK")
    hDen_EWK.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_EWK)
    
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    
    # Draw the plot and save it
    hName = "Denominator_LeadingTrijet_Pt_NormalizdQCDmc"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    #=========================================================================================
    # Get the QCD in numerator -  Data Driven
    #=========================================================================================
    rhDict_num_noSF["QCDdd-SR-Inclusive"] = rhDict_num_noSF["QCDinData-VR-Inclusive"].Clone("QCDdd-SR-Inclusive")
    rhDict_num_noSF["QCDdd-SR-Inclusive"].Reset()
    
    binHisto_VR = rhDict_num_noSF["QCDinData-VR-Inclusive"]
    VRtoSR_TF   = manager.GetTransferFactor("Inclusive")
    Print("Applying TF = %s%0.6f%s to VR shape" % (ShellStyles.NoteStyle(), VRtoSR_TF, ShellStyles.NormalStyle()), True)
    binHisto_VR.Scale(VRtoSR_TF)
    rhDict_num_noSF["QCDdd-SR-Inclusive"].Add(binHisto_VR, +1)
    # => rhDict_num_noSF["QCDdd-SR-Inclusive"] is the QCD Data Driven Estimation in SR
    
    #==========================================================================================
    # Get the QCD in numerator - Normalized MC
    #==========================================================================================
    rhDict_num_withQCDSF["NormQCD-SR-Inclusive"] = rhDict_num_withQCDSF["QCD-SR-Inclusive"].Clone()
    rhDict_num_withQCDSF["NormQCD-SR-Inclusive"].Scale(f1)
    
    #==========================================================================================
    # Get the Fake-TT in numerator - Normalized MC
    #==========================================================================================
    rhDict_num_withEWKFakeTTSF["NormTT-SR-Fake"] = rhDict_num_withEWKFakeTTSF["TT-SR-Fake"].Clone()
    rhDict_num_withEWKFakeTTSF["NormTT-SR-Fake"].Scale(f2)
    
    
    # Get the Fake-TT in denominator - Normalized
    hFakeTT_Denominator_normalized = rhDict_den_noSF["TT-SR-Fake"].Clone()
    hFakeTT_Denominator_normalized.Scale(f2)
    
    # Get the Fake-TT in numerator - Normalized
    hFakeTT_Numerator_normalized_noSF = rhDict_num_noSF["TT-SR-Fake"].Clone()
    hFakeTT_Numerator_normalized_noSF.Scale(f2)


    #=========================================================================================
    # Numerator (Data, EWK, Single Top, Normalized QCD, Normalized Fake TT, Genuine TT)
    #=========================================================================================
    # Data
    hNum_Data_SR        = rhDict_num_noSF["Data-SR-Inclusive"]
    # Single Top (using the same SF as for QCD and EWK)
    hNum_SingleTop_SR   = rhDict_num_withQCDSF["SingleTop-SR-Inclusive"]
    # EWK (using the same SF as for QCD and Single Top)
    hNum_EWK_SR         = rhDict_num_withQCDSF["EWK-SR-Inclusive"]
    # QCD (Normalized Factor and using the same SF as for EWK and Single Top)
    hNum_Norm_QCD_SR    = rhDict_num_withQCDSF["NormQCD-SR-Inclusive"]
    # QCD (Data Driven)  -> Marina auto prepei na exei apply ta SF tis QCD
    hNum_QCDdd_SR       = rhDict_num_noSF["QCDdd-SR-Inclusive"]
    # Fake TT (Normalized by factor f2)
    hNum_Norm_FakeTT_SR = rhDict_num_withEWKFakeTTSF["NormTT-SR-Fake"]
    # Genuine TT
    hNum_GenuineTT_SR   = rhDict_num_noSF["TT-SR-Genuine"]
    
    # ========================================================================================
    # Plot Numerator - with QCD Data-Driven
    # ========================================================================================
    # Create empty histogram stack list
    myStackList = []
    
    # Data
    hNum_Data = histograms.Histo(hNum_Data_SR, "Data", "Data")
    hNum_Data.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hNum_Data)
    
    # Fake TT
    hNum_FakeTT = histograms.Histo(hNum_Norm_FakeTT_SR,"Fake TT", "Fake TT")
    hNum_FakeTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_FakeTT)
    
    # Genuine TT
    hNum_GenuineTT= histograms.Histo(hNum_GenuineTT_SR, "TT", "Genuine TT")
    hNum_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_GenuineTT)
    
    # QCD (Data Driven)
    hNum_QCDdd = histograms.Histo(hNum_QCDdd_SR, "QCD (Data)", "QCD")
    hNum_QCDdd.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_QCDdd)
    
    # Single Top
    hNum_SingleTop = histograms.Histo(hNum_SingleTop_SR, "ST", "ST")
    hNum_SingleTop.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_SingleTop)
    
    # EWK
    hNum_EWK = histograms.Histo(hNum_EWK_SR, "EWK", "EWK")
    hNum_EWK.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_EWK)
    
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    
    # Draw the plot and save it
    hName = "Numerator_LeadingTrijet_Pt_QCDdd"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])



    # ========================================================================================
    # Plot Numerator - with QCD Normalized MC
    # ========================================================================================
    # Create empty histogram stack list
    myStackList = []
    
    # Data
    hNum_Data = histograms.Histo(hNum_Data_SR, "Data", "Data")
    hNum_Data.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hNum_Data)
    
    # Fake TT
    hNum_FakeTT = histograms.Histo(hNum_Norm_FakeTT_SR,"Fake TT", "Fake TT")
    hNum_FakeTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_FakeTT)
    
    # Genuine TT
    hNum_GenuineTT= histograms.Histo(hNum_GenuineTT_SR, "TT", "Genuine TT")
    hNum_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_GenuineTT)
    
    # QCD (Normalized MC)
    hNum_QCDmc = histograms.Histo(hNum_Norm_QCD_SR, "QCD", "QCD")
    hNum_QCDmc.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_QCDmc)
    
    # Single Top
    hNum_SingleTop = histograms.Histo(hNum_SingleTop_SR, "ST", "ST")
    hNum_SingleTop.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_SingleTop)
    
    # EWK
    hNum_EWK = histograms.Histo(hNum_EWK_SR, "EWK", "EWK")
    hNum_EWK.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_EWK)
    
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    
    # Draw the plot and save it
    hName = "Numerator_LeadingTrijet_Pt_NormalizdQCDmc"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    print " "
    print " "
    print " "
    print "       Estimate Genuine TT in Data (SR) --> Denominator "
    print " "
    
    
    # ================================================
    # Estimate Genuine TT in Data (SR) - Denominator
    # ================================================
    # Get the Data from SR
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"] = hDen_Data_SR.Clone("TTinData-SR-Genuine-withQCD")
    
    # Subtract Single Top + EK + FakeTT + QCD (Estimated by Normalized MC or data)
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Add(hDen_SingleTop_SR,    -1)
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Add(hDen_EWK_SR,          -1)
    rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Add(hDen_Norm_FakeTT_SR,  -1)
    
    # Cleaned Genuine TT in Data (Data-Driven QCD is removed) 
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDdd"] = rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDdd")
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDdd"].Add(hDen_QCDdd_SR, -1)
    
    # Cleaned Genuine TT in Data (Normalized QCD is removed)
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDmc"] = rhDict_den_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDmc")
    rhDict_den_noSF["TTinData-SR-Genuine-noQCDmc"].Add(hDen_Norm_QCD_SR, -1)
    
    # Plot what goes into the efficiency plot 
    # 
    # Denominator
    hDen_GenuineTTinData_SR_QCDdd = rhDict_den_noSF["TTinData-SR-Genuine-noQCDdd"]
    hDen_GenuineTTinData_SR_QCDmc = rhDict_den_noSF["TTinData-SR-Genuine-noQCDmc"]
    hDen_GenuineTTinMC_SR = hDen_GenuineTT_SR
    
    # Plot Denominator - QCD dd
    myStackList = []
    # Data 
    hDen_Data_QCDdd = histograms.Histo(hDen_GenuineTTinData_SR_QCDdd, "Data", "Data")
    hDen_Data_QCDdd.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hDen_Data_QCDdd)
    # TT Genuine
    hDen_GenuineTT = histograms.Histo(hDen_GenuineTTinMC_SR, "TT", "Genuine TT")
    hDen_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_GenuineTT)
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()

    # Draw the plot and save it
    hName = "GenuineTT_Denominator_LeadingTrijet_Pt_QCDdd"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # Plot Denominator - QCD MC
    myStackList = []
    # Data 
    hDen_Data_QCDmc = histograms.Histo(hDen_GenuineTTinData_SR_QCDmc, "Data", "Data")
    hDen_Data_QCDmc.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hDen_Data_QCDmc)
    # TT Genuine
    hDen_GenuineTT = histograms.Histo(hDen_GenuineTTinMC_SR, "TT", "Genuine TT")
    hDen_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hDen_GenuineTT)
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    # Draw the plot and save it
    hName = "GenuineTT_Denominator_LeadingTrijet_Pt_QCDmc"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    


    



    print "ALL Data in the Denominator:"
    for i in range(1, hDen_Data_SR.GetNbinsX()+1):
        print "i=", i, hDen_Data_SR.GetBinContent(i), "  after removing everything: ",  hDen_GenuineTTinData_SR_QCDdd.GetBinContent(i)





    # ================================================
    # Estimate Genuine TT in Data (SR) - Numerator
    # ================================================
    
    # Get the Data from SR
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"] = hNum_Data_SR.Clone("TTinData-SR-Genuine-withQCD")
    
    # Subtract Single Top + EK + FakeTT + QCD (Estimated by Normalized MC or data)
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Add(hNum_SingleTop_SR, -1)
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Add(hNum_EWK_SR, -1)
    rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Add(hNum_Norm_FakeTT_SR, -1)
    
    # Cleaned Genuine TT in Data (Data-Driven QCD is removed)
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDdd"] = rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDdd")
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDdd"].Add(hNum_QCDdd_SR, -1)
    
    # Cleaned Genuine TT in Data (Normalized QCD is removed)
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDmc"] = rhDict_num_noSF["TTinData-SR-Genuine-withQCD"].Clone("TTinData-SR-Genuine-noQCDmc")
    rhDict_num_noSF["TTinData-SR-Genuine-noQCDmc"].Add(hNum_Norm_QCD_SR, -1)
    
    
    hNum_GenuineTTinData_SR_QCDdd = rhDict_num_noSF["TTinData-SR-Genuine-noQCDdd"]
    hNum_GenuineTTinData_SR_QCDmc = rhDict_num_noSF["TTinData-SR-Genuine-noQCDmc"]
    hNum_GenuineTTinMC_SR         = hNum_GenuineTT_SR

    # Plot Numerator - QCD dd
    myStackList = []
    # Data 
    hNum_Data_QCDdd = histograms.Histo(hNum_GenuineTTinData_SR_QCDdd, "Data", "Data")
    hNum_Data_QCDdd.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hNum_Data_QCDdd)
    # TT Genuine
    hNum_GenuineTT = histograms.Histo(hNum_GenuineTTinMC_SR, "TT", "Genuine TT")
    hNum_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_GenuineTT)
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    # Draw the plot and save it
    hName = "GenuineTT_Numerator_LeadingTrijet_Pt_QCDdd"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    # Plot Denominator - QCD MC
    myStackList = []
    # Data 
    hNum_Data_QCDmc = histograms.Histo(hNum_GenuineTTinData_SR_QCDmc, "Data", "Data")
    hNum_Data_QCDmc.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hNum_Data_QCDmc)
    # TT Genuine
    hNum_GenuineTT = histograms.Histo(hNum_GenuineTTinMC_SR, "TT", "Genuine TT")
    hNum_GenuineTT.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_GenuineTT)
    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    # Draw the plot and save it
    hName = "GenuineTTNumerator__LeadingTrijet_Pt_QCDmc"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
    
    
    #================================================================================================
    # Plot Fake Tops
    #=================================================================================================
    
    
    h_FakeTop_Denominator      = hFakeTT_Denominator_normalized
    h_FakeTop_Numerator_noSF   = hFakeTT_Numerator_normalized_noSF
    h_FakeTop_Numerator_withSF = hNum_Norm_FakeTT_SR

    # Create empty histogram stack list
    myStackList = []

    #styles.zzStyle.apply(h_FakeTop_Denominator)
    #hDen_FakeTT = histograms.Histo( h_FakeTop_Denominator, "Fake TT (Den)", "FakeTT")
    #hDen_FakeTT.setIsDataMC(isData=False, isMC=True)
    #myStackList.append(hDen_FakeTT)

    
    # Data
    hNum_Data = histograms.Histo(hNum_Data_SR, "Data", "Data")
    hNum_Data.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, hNum_Data)
    
    hNum_FakeTT_noSF = histograms.Histo(h_FakeTop_Numerator_noSF, "Fake TT noSF", "FakeTT")
    hNum_FakeTT_noSF.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_FakeTT_noSF)
    
    styles.stStyle.apply(h_FakeTop_Numerator_withSF)
    hNum_FakeTT_withSF = histograms.Histo(h_FakeTop_Numerator_withSF, "Fake TT with SF", "FakeTT")
    hNum_FakeTT_withSF.setIsDataMC(isData=False, isMC=True)
    myStackList.append(hNum_FakeTT_withSF)
    
    


    # Create plot
    p = plots.DataMCPlot2(myStackList, saveFormats=[])
    p.setLuminosity(opts.intLumi)
    p.setDefaultStyles()
    # Draw the plot and save it
    hName = "FakeTops_withSFvsSF"
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    
                       











    # ================================================================================================
    #                                    Calculate Efficiencies
    # ================================================================================================
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
        "opts2"            : {"ymin": 0.6, "ymax": 1.4},
        "log"              : False,
        "createLegend"     : {"x1": 0.70, "y1": 0.70, "x2": 0.95, "y2": 0.92},
        
        #"moveLegend"       : {"dx": -0.12, "dy": -0.40, "dh": +0.05*(-4+opts.nDatasets)}, 
        }
    
    
    nx= 8
    bins = [0, 50, 100, 200, 300, 400, 500, 600, 800]
    if len(bins) > 0:
        _kwargs["binList"] = array.array('d', bins)
       
    nx = 0
    if len(_kwargs["binList"]) > 0:
        xBins   = _kwargs["binList"]
        nx      = len(xBins)-1
    counter     = 0
        
    #--------------------------------------------------------
    # Efficiency in Data (using the QCD Data-Driven Method)
    #--------------------------------------------------------
    hNum_GenuineTTinData_SR_QCDdd = hNum_GenuineTTinData_SR_QCDdd.Rebin(nx, "", xBins)
    hDen_GenuineTTinData_SR_QCDdd = hDen_GenuineTTinData_SR_QCDdd.Rebin(nx, "", xBins)
    
    num_Data_QCDdd = hNum_GenuineTTinData_SR_QCDdd
    den_Data_QCDdd = hDen_GenuineTTinData_SR_QCDdd
    
    print "Numerator Bins = ", num_Data_QCDdd.GetNbinsX(), " Denominator Bins =", den_Data_QCDdd.GetNbinsX()
    for i in range (1, num_Data_QCDdd.GetNbinsX()+1):
        print "Bin = ", i, "  Num = ", num_Data_QCDdd.GetBinContent(i), "  Den=", den_Data_QCDdd.GetBinContent(i)

        
    eff_Data_QCDdd = ROOT.TEfficiency(num_Data_QCDdd, den_Data_QCDdd)
    eff_Data_QCDdd.SetStatisticOption(ROOT.TEfficiency.kFCP)
    
    gEff_Data_QCDdd = convert2TGraph(eff_Data_QCDdd)
    Graph_Data_QCDdd = histograms.HistoGraph(gEff_Data_QCDdd, "Data", "p", "P")
    
    #--------------------------------------------------------
    # Efficiency in Data (using the QCD MC Method)
    #--------------------------------------------------------
    hNum_GenuineTTinData_SR_QCDmc = hNum_GenuineTTinData_SR_QCDmc.Rebin(nx, "", xBins)
    hDen_GenuineTTinData_SR_QCDmc = hDen_GenuineTTinData_SR_QCDmc.Rebin(nx, "", xBins)
    
    num_Data_QCDmc = hNum_GenuineTTinData_SR_QCDmc
    den_Data_QCDmc = hDen_GenuineTTinData_SR_QCDmc
    
    print "Numerator Bins = ", num_Data_QCDmc.GetNbinsX(), " Denominator Bins =", den_Data_QCDmc.GetNbinsX()
    
    for i in range (1, num_Data_QCDmc.GetNbinsX()+1):
        print "Bin = ", i, "  Num = ", num_Data_QCDmc.GetBinContent(i), "  Den=", den_Data_QCDmc.GetBinContent(i)



    eff_Data_QCDmc = ROOT.TEfficiency(num_Data_QCDmc, den_Data_QCDmc)
    eff_Data_QCDmc.SetStatisticOption(ROOT.TEfficiency.kFCP)
    
    gEff_Data_QCDmc = convert2TGraph(eff_Data_QCDmc)
    Graph_Data_QCDmc = histograms.HistoGraph(gEff_Data_QCDmc, "Data", "p", "P")
    
    #-------------------------------------------------------
    # Efficiency in Genuine TT MC
    #-------------------------------------------------------
    hNum_GenuineTTinMC_SR = hNum_GenuineTTinMC_SR.Rebin(nx, "", xBins)
    hDen_GenuineTTinMC_SR = hDen_GenuineTTinMC_SR.Rebin(nx, "", xBins)

    num_GenuineTT = hNum_GenuineTTinMC_SR
    den_GenuineTT = hDen_GenuineTTinMC_SR
    
    eff_GenuineTT = ROOT.TEfficiency(num_GenuineTT, den_GenuineTT)
    eff_GenuineTT.SetStatisticOption(ROOT.TEfficiency.kFCP)
    
    gEff_GenuineTT = convert2TGraph(eff_GenuineTT)
    styles.ttStyle.apply(gEff_GenuineTT)
    Graph_GenuineTT = histograms.HistoGraph(gEff_GenuineTT, "Genuine TT", "p", "P")
    
    # -------------------------------------------------------
    # Efficiency in FakeTT
    # -------------------------------------------------------
    hNum_Norm_FakeTT_SR = hNum_Norm_FakeTT_SR.Rebin(nx, "", xBins)
    hDen_Norm_FakeTT_SR = hDen_Norm_FakeTT_SR.Rebin(nx, "", xBins)
    
    num_FakeTT = hNum_Norm_FakeTT_SR
    den_FakeTT = hDen_Norm_FakeTT_SR
    
    eff_FakeTT = ROOT.TEfficiency(num_FakeTT, den_FakeTT)
    eff_FakeTT.SetStatisticOption(ROOT.TEfficiency.kFCP)
    
    gEff_FakeTT = convert2TGraph(eff_FakeTT)
    styles.zzStyle.apply(gEff_FakeTT)
    Graph_FakeTT = histograms.HistoGraph(gEff_FakeTT, "Fake TT", "p", "P")

    #--------------------------------------------------------
    # Efficiency in EWK
    #--------------------------------------------------------
    hNum_EWK_SR = hNum_EWK_SR.Rebin(nx, "", xBins)
    hDen_EWK_SR = hDen_EWK_SR.Rebin(nx, "", xBins)

    num_EWK = hNum_EWK_SR
    den_EWK = hDen_EWK_SR

    eff_EWK = ROOT.TEfficiency(num_EWK, den_EWK)
    eff_EWK.SetStatisticOption(ROOT.TEfficiency.kFCP)

    gEff_EWK = convert2TGraph(eff_EWK)
    styles.ttjetsStyle.apply(gEff_EWK)
    Graph_EWK =  histograms.HistoGraph(gEff_EWK, "EWK", "p", "P")

    #---------------------------------------------------------
    # Efficiency in QCD (Normalized MC)
    #---------------------------------------------------------
    hNum_Norm_QCD_SR = hNum_Norm_QCD_SR.Rebin(nx, "", xBins)
    hDen_Norm_QCD_SR = hDen_Norm_QCD_SR.Rebin(nx, "", xBins)
    
    num_QCDmc = hNum_Norm_QCD_SR
    den_QCDmc = hDen_Norm_QCD_SR
    
    eff_QCDmc = ROOT.TEfficiency(num_QCDmc, den_QCDmc)
    eff_QCDmc.SetStatisticOption(ROOT.TEfficiency.kFCP)

    gEff_QCDmc = convert2TGraph(eff_QCDmc)
    styles.qcdStyle.apply(gEff_QCDmc)
    Graph_QCDmc = histograms.HistoGraph(gEff_QCDmc, "QCD (MC)", "p", "P")

    #---------------------------------------------------------
    # Efficiency in QCD (Data-Driven)
    #---------------------------------------------------------
    hNum_QCDdd_SR = hNum_QCDdd_SR.Rebin(nx, "", xBins)
    hDen_QCDdd_SR = hDen_QCDdd_SR.Rebin(nx, "", xBins)
    
    num_QCDdd = hNum_QCDdd_SR
    den_QCDdd = hDen_QCDdd_SR
    
    eff_QCDdd = ROOT.TEfficiency(num_QCDdd, den_QCDdd)
    eff_QCDdd.SetStatisticOption(ROOT.TEfficiency.kFCP)

    gEff_QCDdd = convert2TGraph(eff_QCDdd)
    #styles.wwStyle.apply(gEff_QCDdd)
    Graph_QCDdd = histograms.HistoGraph(gEff_QCDdd, "QCD (Data)", "p", "P")

    #---------------------------------------------------------
    # Efficiency in Single Top
    #---------------------------------------------------------
    hNum_SingleTop_SR = hNum_SingleTop_SR.Rebin(nx, "", xBins)
    hDen_SingleTop_SR = hDen_SingleTop_SR.Rebin(nx, "", xBins)
    
    num_ST = hNum_SingleTop_SR
    den_ST = hDen_SingleTop_SR
    
    eff_ST =  ROOT.TEfficiency(num_ST, den_ST)
    eff_ST.SetStatisticOption(ROOT.TEfficiency.kFCP)
    
    gEff_ST = convert2TGraph(eff_ST)
    styles.stStyle.apply(gEff_ST)
    Graph_ST = histograms.HistoGraph(gEff_ST, "Single Top", "p", "P")
    


    # --------------------------------------------------------------------------------------------
    # Create plot comparing efficiency in EWK, QCD (MC and Data-Driven), Fake TT and Single Top
    # --------------------------------------------------------------------------------------------

    # Plot the efficiency
    _kwargs["ratio"]  = False
    _kwargs["ylabel"] = "Misidentification rate" 
    p = plots.ComparisonManyPlot(Graph_EWK, [Graph_FakeTT, Graph_QCDdd, Graph_QCDmc, Graph_ST], saveFormats=[])
    saveName = "MisID_EWK_FakeTT_QCD_ST"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    
    ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")

    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])

    # =============================================================
    # Plot Efficiency Genuine TT in Data (with QCDdd) Vs Genuine TT
    # =============================================================
    
    _kwargs["ratio"]  = True        
    _kwargs["ylabel"] = "Efficiency"
    
    # Plot the efficiency
    p = plots.ComparisonManyPlot(Graph_Data_QCDdd, [Graph_GenuineTT], saveFormats=[])
    
    saveName = "GenuineTT_DataVsMC_Efficiency_LeadingTrijet_Pt_withQCDdd"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    
    ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")
    units = "GeV/c"
    _kwargs["xlabel"] = "p_{T} (%s)" % (units)
    
    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])

    

    # =============================================================
    # Plot Efficiency Genuine TT in Data (with QCDmc) Vs Genuine TT
    # =============================================================
    
    _kwargs["ratio"]  = True        
    _kwargs["ylabel"] = "Efficiency"
    
    # Plot the efficiency
    p = plots.ComparisonManyPlot(Graph_Data_QCDmc, [Graph_GenuineTT], saveFormats=[])
    
    saveName = "GenuineTT_DataVsMC_Efficiency_LeadingTrijet_Pt_withQCDmc"
    savePath = os.path.join(opts.saveDir, opts.optMode)
    
    ROOT.gStyle.SetNdivisions(6 + 100*5 + 10000*2, "X")
    units = "GeV/c"
    _kwargs["xlabel"] = "p_{T} (%s)" % (units)
    
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
        #print __doc__
        sys.exit(1)
        
    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.noSFcrab, prefix="", postfix="")

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== getABCD_TF_Efficiencies_MethodB.py: Press any key to quit ROOT ...")
