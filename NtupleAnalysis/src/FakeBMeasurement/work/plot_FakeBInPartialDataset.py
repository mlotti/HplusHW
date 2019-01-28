#!/usr/bin/env python
'''
DESCRIPTION:
This script produces FakeB normalization factors by employing an ABCD method
using regions created by inverting the b-jets selections and the MVA2 top 
(i.e. subleading in BDT discrimant) as follows:
         MVA2max
              ^
              |
              |--------------|--------------|--------------|
        >=0.8 |      CR3     |      VR      |      SR      |
              |--------------|--------------|--------------|
0.4 < && <0.8 |      CR4     |      CR2     |      CR1     |
              |--------------|--------------|--------------|----> CSVv2
              | ==1M, >= 2L  | ==2M, >= 1L  |      >=3M    |

The assumption is that MVA2max and CSVv2-M and NOT (at least strongly) correlated
and that the shapes in SR and CR1 (VR and CR2, and CR3 and CR4) are similar.
In that was one can write the following relation:
SR/VR = CR1/CR2
Therefore:
SR = (CR1/CR2)*VR

We call the ratio f=(CR1/CR2) the transfer factor that gets us from VR to the SR. This
is needed to ensure the normalisation of the sample obtained from VR is corrected.
Then, if we want the predicted FakeB shape of the tetrajet mass in the signal region (m_SR) 
we do the following:
m_SR = f * m_VR
where m_CR1 is is the shape of mjjbb and f=(CR1/CR2) is the transfer factor
needed to correctly normalise the shape obtained from VR.


The steps followed are the following:
1) The user defines the histogram that will be used to extract the transfer factor (f)
These normalisation factor are saved under:
   <pseudo_mcrab_directory> FakeBTranserFactors_Run2016_80to1000.py
in an automatically-generated python class. 

This file/class is later used (read) by the makeInvertedPseudoMulticrab.py in order to normalise
properly the "Control-Region" data.


USAGE:
./plot_FakeBInPartialDataset.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --url
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey "TetrajetPt"  --url
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey "TetrajetMass"  --url
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey "TetrajetBJetPt"  --url
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey "TetrajetBJetEta"  --url
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey "LdgTrijetMass"  --url
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey "LdgTrijetPt"  --url
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey "TetrajetMass"
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_Test_22Nov2018 --histoKey TetrajetMass --url


LAST USED:
./plot_FakeBInPartialDataset.py -m FakeBMeasurement_TopMassLE400_BDT0p40_Binning4Eta5Pt_Syst_NoTopPtReweightCorrXML_10Jan2019 --histoKey TetrajetMass --url

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
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.FakeBMeasurement.FakeBNormalization as FakeBNormalization
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

def GetHistoKwargs(histoName):

    # Definitions
    _opts   = {}
    _cutBox = {}
    _rebinX = 1
    _logY   = True
    _opts   = {"ymin": 1e0, "ymaxfactor": 1.2}
    #_ylabel = "Events / %.0f"
    _ylabel = "< Events %s >"
    _units  = ""
    if _logY:
        #_opts = {"ymin": 1e0, "ymaxfactor": 5.0}
        _opts = {"ymin": 1e-2, "ymaxfactor": 5.0}

    if "pt" in histoName.lower():
        _units        = "GeV" #"GeV/c"
        _xlabel       = "p_{T} (%s)" % (_units)
        _cutBox       = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _rebinX       = 1 #2
        if "tetrajetbjet" in histoName.lower():
            _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            _rebinX = 2
            _opts["xmax"] = 800
        if "trijet" in histoName.lower():
            _rebinX = 2 #10
            _opts["xmax"] = 800 #600

    if "mass" in histoName.lower():
        _units        = "GeV" #/c^{2}"
        _xlabel       = "m_{jjb} (%s)" % (_units)
        _opts["xmin"] =  50
        _opts["xmax"] = 3000
        _cutBox       = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

        if "tetrajet" in histoName.lower():
            _xlabel       = "m_{jjbb} (%s)" % (_units)
            _opts["xmin"] =    0
            _opts["xmax"] = 3000
            _cutBox       = {"cutValue": 180.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            _rebinX       = systematics.getBinningForTetrajetMass(18) #systematics.getBinningForTetrajetMass(1) systematics.getBinningForTetrajetMass(13)
            #if isinstance(_rebinX, list):
            #    _ylabel = "< Events / GeV >"
        if "trijet" in histoName.lower():
            _opts["xmax"] = 300                

    if "tetrajetbjeteta" in histoName.lower():
        _units   = ""
        _xlabel  = "#eta"
        _cutBox  = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e0, "ymax": 1e3}
        _rebinX  = 1
        _ylabel  = "Events / %.2f"
                
    # Define plotting options
    if _units == "":
        ylabel = "< Events >"
    else:
        ylabel =  "< Events / %s >" % _units

    kwargs = {
        "xlabel"           : _xlabel,
        "rebinX"           : _rebinX,
        "divideByBinWidth" : True,
        "ylabel"           : ylabel, #_ylabel,
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
        "createLegend"     : {"x1": 0.66, "y1": 0.78, "x2": 0.92, "y2": 0.92},
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
        Verbose(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return

#================================================================================================ 
# Main
#================================================================================================ 
def main(count, runRange, dsetList, opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(True)
    style.setGridY(True)
    
    # Obtain dsetMgrCreator and register it to module selector
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=opts.mcrab)

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

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()
            
        # Remove datasets        
        removeList   = ["QCD-b", "Charged", "QCD", "ZJetsToQQ_HT600toInf"]
        opts.intLumi = 0.0

        # For-loop: All datasets in the manager
        for d in datasetsMgr.getAllDatasets():
            if d.isMC():
                continue

            # Inclusive data
            if len(dsetList) == 1 and dsetList[0] == "Run2016":
                Verbose("Inclusive data. Will not remove anything", True)
                opts.intLumi += GetLumi(datasetsMgr)
                break

            # Special combinations
            for rr in dsetList:
                if rr not in d.getName():
                    Verbose("\"%s\" is not in dataset name \"%s\"" % (rr, d.getName()), False)
                    if d.getName() not in removeList:
                        # Ensure dataset to be removed is not in the dsetList
                        if not any(rr in d.getName() for rr in dsetList):
                            removeList.append(d.getName())
                else:
                    Verbose("\"%s\" is in dataset name \"%s\"" % (rr, d.getName()), False)
                    # Get luminosity if a value is not specified
                    opts.intLumi += d.getLuminosity()

        # For-loop: All dataset names to be removed
        for i, d in enumerate(removeList, 0):
            Verbose(ShellStyles.HighlightAltStyle() + "Removing dataset %s" % d + ShellStyles.NormalStyle(), False)
            datasetsMgr.remove(filter(lambda name: d in name, datasetsMgr.getAllDatasetNames()))

        # Inform user of dataset and corresponding integrated lumi
        Print("%d) %s (%.1f 1/pb)" % (count, runRange, opts.intLumi), count==1)
        #Print("%d) %s (%.1f 1/pb)" % (count, ", ".join(dsetList), opts.intLumi), count==1)

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Print dataset information
        if 0:
            datasetsMgr.PrintInfo()

        # Merge EWK samples
        datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
            
        # Do the fit on the histo after ALL selections (incl. topology cuts)
        folderList = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        folderList1 = [h for h in folderList if opts.histoKey in h]
        folderList2 = [h for h in folderList1 if "VR" in h or "SR" in h or "CRone" in h or "CRtwo" in h  or "CRthree" in h  or "CRfour" in h]

        # For-loop: All folders
        histoPaths = []
        for f in folderList2:
            folderPath = os.path.join(opts.folder, f)
            histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folderPath)            
            pathList   = [os.path.join(folderPath, h) for h in histoList]
            histoPaths.extend( pathList )

        binLabels = GetBinLabels("CRone", histoPaths)
        PlotHistosAndCalculateTF(runRange, datasetsMgr, histoPaths, binLabels, opts)
    return


def GetBinLabels(region, histoPaths):
    binLabels = []

    # Determine bin labels
    for h in histoPaths:
        region = "_CRone"
        if region not in h:
            continue
        else:
            binLabels.append(h.split(region)[-1])
    return binLabels
        
def GetHistoPathDict(histoList, printList=False):
    histoDict = {}

    # For-loop: All histograms (full paths)
    for h in histoList:
        if "_SR" in h:
            region = "SR"
        elif "_VR" in h:
            region = "VR"
        elif "_CRone" in h:
            region = "CRone"
        elif "_CRtwo" in h:
            region = "CRtwo"
        elif "_CRthree" in h:
            region = "CRthree"
        elif "_CRfour" in h:
            region = "CRfour"
        else:
            raise Exception("Could not determine Control Region for histogram %s" % (h) )
        # Save histogram in dictionary
        binLabel = h.split(region)[-1]
        label1 = "%s-%s" % (region, binLabel)
        label2 = "%s-%s-%s" % (region, binLabel, "EWKGenuineB")
        label3 = "%s-%s-%s" % (region, binLabel, "EWKFakeB")
        histoDict[label1] = h
        histoDict[label2] = h.replace(opts.folder, opts.folder + "EWKGenuineB")
        histoDict[label3] = h.replace(opts.folder, opts.folder + "EWKFakeB")

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

    if printList:
        for i, row in enumerate(rows, 1):
            Print(row, i==1)
    return histoDict

def GetRootHistos(datasetsMgr, histoList, regions, binLabels):
    # Definition
    hPathDict = GetHistoPathDict(histoList, printList=False)
    rhDict    = {}

    # For-loop: All Control Regions (CR)
    for region in regions:
        # For-loop: All bins 
        for binLabel in binLabels:

            # Define labels
            lIncl  = "%s-%s" % (region, binLabel)
            lGenB  = "%s-%s-%s" % (region, binLabel, "EWKGenuineB")
            lFakeB = "%s-%s-%s" % (region, binLabel, "EWKFakeB")

            # Get the desired histograms
            pIncl  = plots.DataMCPlot(datasetsMgr, hPathDict[lIncl])
            pGenB  = plots.DataMCPlot(datasetsMgr, hPathDict[lGenB])
            pFakeB = plots.DataMCPlot(datasetsMgr, hPathDict[lFakeB])
                        
            # Clone and Save the root histograms
            rhDict["Data-" + lIncl] = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("Data-" + lIncl)
            rhDict["EWK-"  + lGenB] = pGenB.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK-"   + lGenB)
            rhDict["EWK-"  + lFakeB] = pFakeB.histoMgr.getHisto("EWK").getRootHisto().Clone("EWK-" + lFakeB)
            if opts.useMC:
                rhDict["QCD-" + lIncl] = pIncl.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD-" + lIncl)
                # Add EWKFakeB (MC) to QCD (MC) to get FakeB (= QCD_inclusive + EWK_fakeB)
                rhDict["FakeB-" + lIncl] = rhDict["QCD-"+ lIncl].Clone("FakeB-" + lIncl)
                rhDict["FakeB-" + lIncl].Add( rhDict["EWK-" + lFakeB], +1 )
            else:
                # Subtract EWKGenuineB (MC) from Data to get FakeB (= Data - EWK_genuineB)
                rhDict["FakeB-" + lIncl] = rhDict["Data-" + lIncl].Clone("FakeB-" + lIncl)
                rhDict["FakeB-" + lIncl].Add( rhDict["EWK-" + lGenB], -1 )

    # For debugging:
    if 0:
        for k in rhDict:
            if "FakeB" not in k:
                continue
            fakeBResult.PrintTH1Info(rhDict[k])
    return rhDict


def PlotHistosAndCalculateTF(runRange, datasetsMgr, histoList, binLabels, opts):

    # Get the histogram customisations (keyword arguments)
    _kwargs = GetHistoKwargs(histoList[0])

    # Get the root histos for all datasets and Control Regions (CRs)
    regions = ["SR", "VR", "CRone", "CRtwo", "CRthree", "CRfour"]
    rhDict  = GetRootHistos(datasetsMgr, histoList, regions, binLabels)

    #=========================================================================================
    # Calculate the Transfer Factor (TF) and save to file
    #=========================================================================================
    manager = FakeBNormalization.FakeBNormalizationManager(binLabels, opts.mcrab, opts.optMode, verbose=False)
    if opts.inclusiveOnly:
        binLabel = "Inclusive"
        manager.CalculateTransferFactor("Inclusive", rhDict["FakeB-CRone-Inclusive"], rhDict["FakeB-CRtwo-Inclusive"], rhDict["FakeB-CRthree-Inclusive"], rhDict["FakeB-CRfour-Inclusive"])
    else:
        for bin in binLabels:
            manager.CalculateTransferFactor(bin, rhDict["FakeB-CRone-%s" % bin], rhDict["FakeB-CRtwo-%s" % bin], rhDict["FakeB-CRthree-%s" % bin], rhDict["FakeB-CRfour-%s" % bin])

    # Get unique a style for each region
    for k in rhDict:
        dataset = k.split("-")[0]
        region  = k.split("-")[1]
        styles.getABCDStyle(region).apply(rhDict[k])
        if "FakeB" in k:
            styles.getFakeBStyle().apply(rhDict[k])
        # sr.apply(rhDict[k])

    # =========================================================================================
    # Create the final plot object
    # =========================================================================================
    rData_SR        = rhDict["Data-SR-Inclusive"] 
    rEWKGenuineB_SR = rhDict["EWK-SR-Inclusive-EWKGenuineB"]
    rBkgSum_SR      = rhDict["FakeB-VR-Inclusive"].Clone("BkgSum-SR-Inclusive")
    rBkgSum_SR.Reset()

    if opts.inclusiveOnly:
        bin = "Inclusive"
        # Normalise the VR histogram with the Transfer Factor ( BkgSum = VR * (CR1/CR2) )
        binHisto_VR = rhDict["FakeB-VR-%s" % (bin)]
        VRtoSR_TF   = manager.GetTransferFactor(bin)
        Verbose("Applying TF = %s%0.6f%s to VR shape" % (ShellStyles.NoteStyle(), VRtoSR_TF, ShellStyles.NormalStyle()), True)
        binHisto_VR.Scale(VRtoSR_TF) 
        # Add the normalised histogram to the final Inclusive SR (predicted) histo
        rBkgSum_SR.Add(binHisto_VR, +1)
    else:
        # For-loop: All bins
        for i, bin in enumerate(binLabels, 1):
            if bin == "Inclusive":
                continue
            # Normalise the VR histogram with the Transfer Factor ( BkgSum = VR * (CR1/CR2) )
            binHisto_VR = rhDict["FakeB-VR-%s" % (bin)]
            VRtoSR_TF   = manager.GetTransferFactor(bin)
            Verbose("Applying TF = %s%0.6f%s to VR shape" % (ShellStyles.NoteStyle(), VRtoSR_TF, ShellStyles.NormalStyle()), i==1)
            binHisto_VR.Scale(VRtoSR_TF) 
            # Add the normalised histogram to the final Inclusive SR (predicted) histo
            rBkgSum_SR.Add(binHisto_VR, +1)

    # Plot histograms    
    if opts.altPlot:
        # Add the SR EWK Genuine-b to the SR FakeB ( BkgSum = [FakeB] + [GenuineB-MC] = [VR * (CR1/CR2)] + [GenuineB-MC] )
        rBkgSum_SR.Add(rEWKGenuineB_SR, +1) 

        # Change style
        styles.getGenuineBStyle().apply(rBkgSum_SR)

        # Remove unsupported settings of kwargs
        _kwargs["stackMCHistograms"] = False
        _kwargs["addLuminosityText"] = False

        # Create the plot
        p = plots.ComparisonManyPlot(rData_SR, [rBkgSum_SR], saveFormats=[])

        # Set draw / legend style
        p.histoMgr.setHistoDrawStyle("Data-SR-Inclusive", "P")
        p.histoMgr.setHistoLegendStyle("Data-SR-Inclusive" , "LP")
        p.histoMgr.setHistoDrawStyle("BkgSum-SR-Inclusive", "HIST")
        p.histoMgr.setHistoLegendStyle("BkgSum-SR-Inclusive" , "F")

        # Set legend labels
        p.histoMgr.setHistoLegendLabelMany({
                "Data-SR"       : "Data",
                "BkgSum-SR"     : "Fake-b + Gen-b",
                })
    else:
        # Create empty histogram stack list
        myStackList = []
        
        # Add the FakeB data-driven background to the histogram list    
        hFakeB = histograms.Histo(rBkgSum_SR, "FakeB", "Fake-b")
        hFakeB.setIsDataMC(isData=False, isMC=True)
        myStackList.append(hFakeB)
        
        # Add the EWKGenuineB MC background to the histogram list
        hGenuineB = histograms.Histo(rEWKGenuineB_SR, "GenuineB", "EWK Genuine-b")
        hGenuineB.setIsDataMC(isData=False, isMC=True)
        myStackList.append(hGenuineB)

        # Add the collision datato the histogram list        
        hData = histograms.Histo(rData_SR, "Data", "Data")
        hData.setIsDataMC(isData=True, isMC=False)
        myStackList.insert(0, hData)
        
        p = plots.DataMCPlot2( myStackList, saveFormats=[])
        p.setLuminosity(opts.intLumi)
        p.setDefaultStyles()

    # Draw the plot and save it
    hName = opts.histoKey
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

    #=========================================================================================
    # Calculate the Transfer Factor (TF) and save to file
    #=========================================================================================
    Verbose("Write the normalisation factors to a python file", True)
    fileName = os.path.join(opts.mcrab, "FakeBTransferFactors_%s.py" % ( runRange ) )
    manager.writeTransferFactorsToFile(fileName, opts)
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
    ANALYSISNAME = "FakeBMeasurement"
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
    FOLDER       = "ForFakeBMeasurement"
    INCLUSIVE    = False
    HISTOKEY     = "TetrajetBJetEta" #options: "MET", "TetrajetBJetPt", "TetrajetBJetEta", "TetrajetMass", "LdgTrijetMass", "LdgTrijetPt"

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

    parser.add_option("--altPlot", dest="altPlot", action="store_true", default=ALTPLOT, 
                      help="Draw alternative plot with Data and Bkg-Sum [default: %s]" % ALTPLOT)

    parser.add_option("--histoKey", dest="histoKey", type="string", default=HISTOKEY, 
                      help="Keyword string to uniquely identify the histogram to use in extracting the Transfer Factors (TFs) [default: %s]" % HISTOKEY)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

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
    if opts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="TransferFactor")

    # Call the main function
    dsetSets = {
        "Run2016"  : ["Run2016B", "Run2016C", "Run2016D", "Run2016E", "Run2016F", "Run2016G", "Run2016H"],
        ### Individual Runs (too small statistics)
        # "Run2016B" : ["Run2016B"],
        # "Run2016C" : ["Run2016C"],
        # "Run2016D" : ["Run2016D"],
        # "Run2016E" : ["Run2016E"],
        # "Run2016F" : ["Run2016F"],
        # "Run2016G" : ["Run2016G"],
        # "Run2016H" : ["Run2016H"],
        ### Custom-tailor dataset sets (4 groups)
        # "Run2016BC" : ["Run2016B", "Run2016C"],
        # "Run2016DEF": ["Run2016D", "Run2016E", "Run2016F"], 
        # "Run2016G"  : ["Run2016G"], # up to 30% wrt "Run2016"
        # "Run2016H"  : ["Run2016H"],
        ### Custom-tailor dataset sets (3 groups)
        # "Run2016BCD": ["Run2016B", "Run2016C", "Run2016D"],
        # "Run2016EF" : ["Run2016E", "Run2016F"], 
        # "Run2016GH" : ["Run2016G", "Run2016H"],
        ### Custom-tailor dataset sets (4 groups)
        "Run2016BC": ["Run2016B", "Run2016C"],
        "Run2016DE": ["Run2016D", "Run2016E"], 
        "Run2016FG": ["Run2016F", "Run2016G"], 
        "Run2016H" : ["Run2016H"],
        }

    # Do partial data dataset (closure attempt)
    for i, rr in enumerate(dsetSets, 1):
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="TransferFactor_%s" % rr)
        dsetList     = dsetSets[rr]
        Verbose("%d) %s" % (i, ", ".join(dsetList) ), i==1)
        main(i, rr, dsetList, opts)

    Print("%sAll plots saved under %s%s" % (ShellStyles.SuccessStyle(), opts.saveDir, ShellStyles.NormalStyle()), True)

    if not opts.batchMode:
        raw_input("=== plot_FakeBInPartialDataset.py: Press any key to quit ROOT ...")
