#!/usr/bin/env python
'''
Description:
This script produces QCD normalization factors by employing an ABCD method
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
   <pseudo_mcrab_directory> QCDInvertedNormalizationFactors_Run2016_80to1000.py
in an automatically-generated python class. 

This file/class is later used (read) by the makeInvertedPseudoMulticrab.py in order to normalise
properly the "Control-Region" data.


USAGE:
./getABCD_TF.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES: 
./getABCD_TF.py -m FakeBMeasurement_GE2Medium_GE1Loose0p80_StdSelections_BDT0p70_AllSelections_BDT0p70to0p90_RandomSort_171124_144802/ --url --useMC -e "QCD_HT50to100|QCD_HT100to200|QCD_HT200to300|QCD_HT300to500"
./getABCD_TF.py -m FakeBMeasurement_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180120_092605/ --url --useMC --ratio


LAST USED:
./getABCD_TF.py -m FakeBMeasurement_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180120_092605/ --url --ratio
./getABCD_TF.py -m FakeBMeasurement_NewLeptonVeto_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180125_123834 --ratio --altPlot

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
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.FakeBMeasurement.FakeBNormalization as FakeBNormalization
import HiggsAnalysis.NtupleAnalysis.tools.analysisModuleSelector as analysisModuleSelector

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

def GetListOfEwkDatasets(datasetsMgr):
    Verbose("Getting list of EWK datasets")
    if "noTop" in datasetsMgr.getAllDatasetNames():
        return  ["TT", "noTop", "SingleTop", "ttX"]
    else:
        return  ["TT", "WJetsToQQ_HT_600ToInf", "SingleTop", "DYJetsToQQHT", "TTZToQQ",  "TTWJetsToQQ", "Diboson", "TTTT"]

def GetHistoKwargs(histoName):

    # Definitions
    _opts   = {}
    _cutBox = {}
    _rebinX = 1
    _logY   = True
    _opts   = {"ymin": 1e0, "ymaxfactor": 1.2}
    _ylabel = "Events / %.0f"
    if _logY:
        _opts     = {"ymin": 1e0, "ymaxfactor": 5.0}

    if "mass" in histoName.lower():
        _units        = "GeV/c^{2}"
        _xlabel       = "m_{jjb} (%s)" % (_units)
        _ylabel      += " " + _units
        _opts["xmin"] =  50
        _opts["xmax"] = 300
        _cutBox       = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

        if "tetrajet" in histoName.lower():
            _xlabel       = "m_{jjbb} (%s)" % (_units)
            _opts["xmin"] =    0
            _opts["xmax"] = 3000
            _cutBox       = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            _rebinX       = GetTetrajetMassBins()
            if isinstance(_rebinX, list):
                _ylabel = "Events / bin"

    if "met" in histoName.lower():
        _units        = "GeV"
        _xlabel       = "E_{T}^{miss} (%s)" % (_units)
        _ylabel      += " " + _units
        _opts["xmin"] =   0
        _opts["xmax"] = 300
        _cutBox       = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _rebinX       = 1
                
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
        "createLegend"     : {"x1": 0.66, "y1": 0.78, "x2": 0.92, "y2": 0.92},
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
def main(opts):

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
            
        # Get the PSets:
        thePSets = datasetsMgr.getDataset("TT").getParameterSet()
        if 0:
            Print("Printing the PSet:\n" + thePSets, True)

        # ZJets and DYJets overlap!
        if "ZJetsToQQ_HT600toInf" in datasetsMgr.getAllDatasetNames() and "DYJetsToQQ_HT180" in datasetsMgr.getAllDatasetNames():
            Print("Cannot use both ZJetsToQQ and DYJetsToQQ due to duplicate events? Investigate. Removing ZJetsToQQ datasets for now ..", True)
            datasetsMgr.remove(filter(lambda name: "ZJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 

        # Get luminosity if a value is not specified
        if opts.intLumi < 0:
            opts.intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        
        # Remove datasets
        removeList = ["QCD-b", "Charged"]
        if not opts.useMC:
            removeList.append("QCD")
        for i, d in enumerate(removeList, 0):
            msg = "Removing dataset %s" % d
            Verbose(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), i==0)
            datasetsMgr.remove(filter(lambda name: d in name, datasetsMgr.getAllDatasetNames()))

        # Print summary of datasets to be used
        if 0:
            datasetsMgr.PrintInfo()
        
        # Merge EWK samples
        datasetsMgr.merge("EWK", GetListOfEwkDatasets(datasetsMgr))
            
        # Print dataset information
        datasetsMgr.PrintInfo()
        
        # Do the fit on the histo after ALL selections (incl. topology cuts)
        folder    = "ForFakeBMeasurement" # "ForFakeBNormalization"
        histoList = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folder)
        histoList = [h for h in histoList if "TetrajetMass" in h]
        PlotHistogramsAndCalculateTF(datasetsMgr, histoList, folder, opts)
    return


def GetTetrajetMassBins():
    myBins   = []
    binWidth1=   25
    binWidth2=   50
    binWidth3=  100
    binWidth4=  500
    xMax1    =  600
    xMax2    = 1400
    xMax3    = 2000
    xMax4    = 3000
    for m in range(0, xMax1, binWidth1):
        myBins.append(m)
    for m in range(xMax1, xMax2, binWidth2):
        myBins.append(m)
    for m in range(xMax2, xMax3, binWidth3):
        myBins.append(m)
    for m in range(xMax3, xMax4+binWidth4, binWidth4):
        myBins.append(m)
    return myBins


def PlotHistogramsAndCalculateTF(datasetsMgr, histoList, inclusiveFolder, opts):

    # Get the histogram customisations (keyword arguments)
    _kwargs = GetHistoKwargs(histoList[0])

    # Variable definition
    genuineBFolder  = inclusiveFolder + "EWKGenuineB"
    fakeBFolder     = inclusiveFolder + "EWKFakeB"

    # Histogram names
    if 0:
        hName = "LdgTetrajetMass" #histoList[0].split("_")[1]
    else:
        hName = "MET"
        _kwargs = GetHistoKwargs(hName)

    # Get histogams for the Signal Region (SR) and the 3 Control Regions (CR)
    histoName      = "Baseline_" + hName + "_AfterAllSelections"
    hInclusive_SR  = "%s/%s" % (inclusiveFolder, histoName)
    hGenuineB_SR   = "%s/%s" % (genuineBFolder , histoName)
    hFakeB_SR      = "%s/%s" % (fakeBFolder    , histoName)

    histoName      = "Inverted_" + hName + "_AfterAllSelections"
    hInclusive_VR  = "%s/%s" % (inclusiveFolder, histoName)
    hGenuineB_VR   = "%s/%s" % (genuineBFolder , histoName)
    hFakeB_VR      = "%s/%s" % (fakeBFolder    , histoName)

    histoName      = "Baseline_" + hName + "_AfterCRSelections"
    hInclusive_CR1 = "%s/%s" % (inclusiveFolder, histoName)
    hGenuineB_CR1  = "%s/%s" % (genuineBFolder , histoName) 
    hFakeB_CR1     = "%s/%s" % (fakeBFolder    , histoName) 

    histoName      = "Inverted_" + hName + "_AfterCRSelections"
    hInclusive_CR2 = "%s/%s" % (inclusiveFolder, histoName)
    hGenuineB_CR2  = "%s/%s" % (genuineBFolder , histoName)
    hFakeB_CR2     = "%s/%s" % (fakeBFolder    , histoName)
    Print()

    # Create plots
    pInclusive_SR  = plots.DataMCPlot(datasetsMgr, hInclusive_SR)
    pGenuineB_SR   = plots.DataMCPlot(datasetsMgr, hGenuineB_SR)
    pFakeB_SR      = plots.DataMCPlot(datasetsMgr, hFakeB_SR)

    pInclusive_VR  = plots.DataMCPlot(datasetsMgr, hInclusive_VR)
    pGenuineB_VR   = plots.DataMCPlot(datasetsMgr, hGenuineB_VR)
    pFakeB_VR      = plots.DataMCPlot(datasetsMgr, hFakeB_VR)

    pInclusive_CR1 = plots.DataMCPlot(datasetsMgr, hInclusive_CR1)
    pGenuineB_CR1  = plots.DataMCPlot(datasetsMgr, hGenuineB_CR1)
    pFakeB_CR1     = plots.DataMCPlot(datasetsMgr, hFakeB_CR1)

    pInclusive_CR2 = plots.DataMCPlot(datasetsMgr, hInclusive_CR2)
    pGenuineB_CR2  = plots.DataMCPlot(datasetsMgr, hGenuineB_CR2)
    pFakeB_CR2     = plots.DataMCPlot(datasetsMgr, hFakeB_CR2)


    # Get the desired histograms
    rData_SR        = pInclusive_SR.histoMgr.getHisto("Data").getRootHisto().Clone("Data-SR")
    rEWKGenuineB_SR = pGenuineB_SR.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKGenuineB-SR")
    rEWKFakeB_SR    = pFakeB_SR.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKFakeB-SR")

    rData_VR        = pInclusive_VR.histoMgr.getHisto("Data").getRootHisto().Clone("Data-VR")
    rEWKGenuineB_VR = pGenuineB_VR.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKGenuineB-VR")
    rEWKFakeB_VR    = pFakeB_VR.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKFakeB-VR")

    rData_CR1        = pInclusive_CR1.histoMgr.getHisto("Data").getRootHisto().Clone("Data-CR1")
    rEWKGenuineB_CR1 = pGenuineB_CR1.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKGenuineB-CR1")
    rEWKFakeB_CR1    = pFakeB_CR1.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKFakeB-CR1")

    rData_CR2        = pInclusive_CR2.histoMgr.getHisto("Data").getRootHisto().Clone("Data-CR2")
    rEWKGenuineB_CR2 = pGenuineB_CR2.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKGenuineB-CR2")
    rEWKFakeB_CR2    = pFakeB_CR2.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKFakeB-CR2")

    if opts.useMC:
        rQCD_SR  = pInclusive_SR.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD-SR")
        rQCD_VR  = pInclusive_VR.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD-VR")
        rQCD_CR1 = pInclusive_CR1.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD-CR1")
        rQCD_CR2 = pInclusive_CR2.histoMgr.getHisto("QCD").getRootHisto().Clone("QCD-CR2")

    
    # Convert QCD (Data) histo clones to FakeB using MC (Data-Driven) methods
    if opts.useMC:
        # For MC: FakeB = QCD + EWKFakeB
        rFakeB_SR  = rQCD_SR.Clone("SR-FakeB")
        rFakeB_VR  = rQCD_VR.Clone("VR-FakeB")
        rFakeB_CR1 = rQCD_CR1.Clone("CR1-FakeB")
        rFakeB_CR2 = rQCD_CR2.Clone("CR2-FakeB")

        # Add EWKGenuineB (MC) to QCD (MC) to get FakeB (= QCD_inclusive + EWK_genuineB)
        rFakeB_SR.Add(rEWKFakeB_SR, +1)
        rFakeB_VR.Add(rEWKFakeB_VR, +1)
        rFakeB_CR1.Add(rEWKFakeB_CR1, +1)
        rFakeB_CR2.Add(rEWKFakeB_CR2, +1)
    else:
        # For DataDriven: FakeB = Data -EWKGenuineB
        rFakeB_SR = rData_SR.Clone("SR-FakeB")
        rFakeB_VR = rData_VR.Clone("VR-FakeB")
        rFakeB_CR1 = rData_CR1.Clone("CR1-FakeB")
        rFakeB_CR2 = rData_CR2.Clone("CR2-FakeB")

        # Subtract EWKGenuineB (MC) from Data to get FakeB (= QCD_inclusive + EWK_genuineB)
        rFakeB_SR.Add(rEWKGenuineB_SR, -1)
        rFakeB_VR.Add(rEWKGenuineB_VR, -1)
        rFakeB_CR1.Add(rEWKGenuineB_CR1, -1)
        rFakeB_CR2.Add(rEWKGenuineB_CR2, -1)

    #=========================================================================================
    # Calculate the Transfer Factor (TF) and save to file
    #=========================================================================================
    binLabels = ["Inclusive"]
    moduleInfoString = opts.optMode
    manager = FakeBNormalization.FakeBNormalizationManager(binLabels, opts.mcrab, moduleInfoString)
    manager.CalculateTransferFactor(binLabels[0], rFakeB_CR1, rFakeB_CR2)

    # Get unique a style for each region
    style_SR    = styles.getABCDStyle("SR")
    style_VR    = styles.getABCDStyle("VR")
    style_CR1   = styles.getABCDStyle("CR1")
    style_CR2   = styles.getABCDStyle("CR2")
    style_FakeB = styles.getFakeBStyle()

    # Apply the styles
    style_SR.apply(rFakeB_SR)
    style_VR.apply(rFakeB_VR)
    style_CR1.apply(rFakeB_CR1)
    style_CR2.apply(rFakeB_CR2)

    style_SR.apply(rEWKGenuineB_SR)
    style_VR.apply(rEWKGenuineB_VR)
    style_CR1.apply(rEWKGenuineB_CR1)
    style_CR2.apply(rEWKGenuineB_CR2)

    style_SR.apply(rEWKFakeB_SR)
    style_VR.apply(rEWKFakeB_VR)
    style_CR1.apply(rEWKFakeB_CR1)
    style_CR2.apply(rEWKFakeB_CR2)

    # =========================================================================================
    # Create the final plot object
    # =========================================================================================
    # Clone the VR histogram ( BkgSum = VR )
    rBkgSum_SR = rFakeB_VR.Clone("BkgSum-SR") 

    # Normalise the VR histogram with the Transfer Factor ( BkgSum = VR * (CR1/CR2) )
    VRtoSR_TF = manager.GetTransferFactor("Inclusive")
    rBkgSum_SR.Scale(VRtoSR_TF) 
    
    # Plot histograms    
    if opts.altPlot:
        # Add the SR EWK Genuine-b to the SR FakeB ( BkgSum = [FakeB] + [GenuineB-MC] = [VR * (CR1/CR2)] + [GenuineB-MC] )
        rBkgSum_SR.Add(rEWKGenuineB_SR) 

        # Change style
        styles.getGenuineBStyle().apply(rBkgSum_SR)

        # Remove unsupported settings of kwargs
        _kwargs["stackMCHistograms"] = False
        _kwargs["addLuminosityText"] = False

        # Create the plot
        p = plots.ComparisonManyPlot(rData_SR, [rBkgSum_SR], saveFormats=[])

        # Set draw / legend style
        p.histoMgr.setHistoDrawStyle("Data-SR", "P")
        p.histoMgr.setHistoLegendStyle("Data-SR" , "LP")
        p.histoMgr.setHistoDrawStyle("BkgSum-SR", "HIST")
        p.histoMgr.setHistoLegendStyle("BkgSum-SR" , "F")

        # Set legend labels
        p.histoMgr.setHistoLegendLabelMany({
                "Data-SR"       : "Data",
                "BkgSum-SR"     : "Fake-b + Gen-b",
                })
    else:
        myStackList = []
        
        # Add the FakeB data-driven background to the histogram list    
        hFakeB = histograms.Histo(rFakeB_SR, "FakeB", "Fake-b")
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
    plots.drawPlot(p, hName, **_kwargs)
    SavePlot(p, hName, os.path.join(opts.saveDir, "TransferFactor", opts.optMode) ) 

    #=========================================================================================
    # Calculate the Transfer Factor (TF) and save to file
    #=========================================================================================
    Verbose("Write the normalisation factors to a python file", True)
    fileName = os.path.join(opts.mcrab, "QCDInvertedNormalizationFactors%s.py"% ( getModuleInfoString(opts) ) )
    manager.writeNormFactorFile(fileName, opts)
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
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE      = False
    USEMC        = False
    RATIO        = False

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

    parser.add_option("--ratio", dest="ratio", action="store_true", default=RATIO,
                      help="Draw ratio canvas for Data/MC curves? [default: %s]" % (RATIO) )

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

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== getABCD_TF.py: Press any key to quit ROOT ...")
