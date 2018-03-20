#!/usr/bin/env python
'''
DESCRIPTION:
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
   <pseudo_mcrab_directory> FakeBTranserFactors_Run2016_80to1000.py
in an automatically-generated python class. 

This file/class is later used (read) by the makeInvertedPseudoMulticrab.py in order to normalise
properly the "Control-Region" data.


USAGE:
./plot_ClosureBinned.py.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plot_ClosureBinned.py -m FakeBMeasurement_NewLeptonVeto_PreSel_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_3BinsEta0p6Eta1p4_180203_14315 --normaliseToOne --url


LAST USED:
./plot_ClosureBinned.py -m FakeBMeasurement_NewLeptonVeto_PreSel_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_3BinsEta0p6Eta1p4_180203_14315 -m

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import array
import getpass
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
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.multicrabConsistencyCheck as consistencyCheck
import HiggsAnalysis.FakeBMeasurement.FakeBNormalization as FakeBNormalization
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
    _ylabel = "Events / %.0f"
    if opts.normaliseToOne:
        _opts   = {"ymin": 0.7e-4, "ymaxfactor": 2.0}
    else:
        _opts   = {"ymin": 1e0, "ymaxfactor": 2.0}
    if _logY:
        _opts["ymaxfactor"] = 5.0

    if "pt" in histoName.lower():
        _units        = "GeV/c"
        _xlabel       = "p_{T} (%s)" % (_units)
        _ylabel      += " " + _units
        #_opts["xmin"] =  50
        #_opts["xmax"] = 300
        _cutBox       = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _rebinX       = 2
        if "trijet" in histoName.lower():
            _opts["xmax"] = 800
            _rebinX = 2 #getBinningForPt(0)
        if "tetrajetbjet" in histoName.lower():
            _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            _rebinX = systematics._dataDrivenCtrlPlotBinning["TetrajetBjetPt_AfterAllSelections"] #2 #getBinningForPt(0)
        if "tetrajet" in histoName.lower():
            _rebinX = systematics._dataDrivenCtrlPlotBinning["LdgTetrajetPt_AfterAllSelections"] #2 #getBinningForPt(0)
            _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
            if "tetrajetbjet" in histoName.lower():
                _cutBox = {"cutValue": 40.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        if isinstance(_rebinX, list):
            binWmin, binWmax = GetBinWidthMinMax(_rebinX)
            _ylabel = "Events / %.0f-%.0f %s" % (binWmin, binWmax, _units)

    if "mass" in histoName.lower():
        _units        = "GeV/c^{2}"
        _xlabel       = "m_{jjb} (%s)" % (_units)
        _ylabel      += " " + _units
        _opts["xmin"] =  50
        _opts["xmax"] = 300
        _cutBox       = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}

        if "trijet" in histoName.lower():
            _rebinX = 2

        if "tetrajet" in histoName.lower():
            _xlabel       = "m_{jjbb} (%s)" % (_units)
            _opts["xmin"] =    0
            _opts["xmax"] = 3000
            _rebinX       = systematics.getBinningForTetrajetMass(0)
            _cutBox       = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        if isinstance(_rebinX, list):
            binWmin, binWmax = GetBinWidthMinMax(_rebinX)
            _ylabel = "Events / %.0f-%.0f %s" % (binWmin, binWmax, _units)

    if "met" in histoName.lower():
        _units        = "GeV"
        _xlabel       = "E_{T}^{miss} (%s)" % (_units)
        _cutBox       = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _opts["xmin"] =   0
        _opts["xmax"] = 400
        _rebinX = systematics._dataDrivenCtrlPlotBinning["MET_AfterAllSelections"]
        binWmin, binWmax = GetBinWidthMinMax(myBins)
        _ylabel = "Events / %.0f-%.0f %s" % (binWmin, binWmax, _units)

    if "ht" in histoName.lower():
        _rebinX = systematics._dataDrivenCtrlPlotBinning["MET_AfterAllSelections"]

    if "tetrajetbjeteta" in histoName.lower():
        _units   = ""
        _xlabel  = "#eta"
        _cutBox  = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": False, "greaterThan": True}
        _rebinX  = 1
        _ylabel  = "Events / %.2f"
        _opts["xmin"] = -2.5
        _opts["xmax"] = +2.5

    if "bdisc" in histoName.lower():
        _format = "%0.2f"
        _ylabel = "Events / " + _format
        _rebinX = 2
        _opts["xmin"] = 0.8
        _opts["xmax"] = 1.0
        _cutBox = {"cutValue": +0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _xlabel = "b-tag discriminant"
        ROOT.gStyle.SetNdivisions(8, "X")

    # Define plotting options
    kwargs = {
        "ratioCreateLegend": True,
        "ratioType"        : None, #"errorScale", #"errorScale", #binomial #errorPropagation
        "ratioErrorOptions": {"numeratorStatSyst": False, "denominatorStatSyst": False}, # Include stat.+syst. to numerator (if syst globally enabled)      
        "ratioMoveLegend"  : {"dx": -0.51, "dy": 0.03, "dh": -0.05},
        "errorBarsX"       : True,
        "xlabel"           : _xlabel,
        "rebinX"           : _rebinX,
        "ylabel"           : _ylabel,
        "log"              : _logY,
        "opts"             : _opts,
        #"opts2"            : {"ymin": 0.6, "ymax": 2.0-0.6},
        "opts2"            : {"ymin": 0.30, "ymax": 1.70},
        "stackMCHistograms": False,
        "addLuminosityText": True,
        "ratio"            : opts.ratio, 
        "ratioYlabel"      : "CR1/CR2",
        "ratioInvert"      : True, 
        "cutBox"           : _cutBox,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "createLegend"     : {"x1": 0.80, "y1": 0.78, "x2": 0.98, "y2": 0.92},
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
    datasets = dataset.getDatasetsFromMulticrabDirs([opts.mcrab],
                                                    dataEra=opts.dataEra,
                                                    searchMode=opts.searchMode, 
                                                    analysisName=opts.analysisName,
                                                    optimizationMode=opts.optMode)
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

    h1 = datasetsMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(analysisType + "-" + datasetName)
    return h1

def getModuleInfoString(opts):

    moduleInfoString = "_%s_%s" % (opts.dataEra, opts.searchMode)
    if len(opts.optMode) > 0:
        moduleInfoString += "_%s" % (opts.optMode)
    return moduleInfoString

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists
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

def GetBinText(bin):
    #return "bin-" + str(bin)
    if bin == "0":
        return "|#eta| < 0.4"
    elif bin == "1":
        return "0.4 < |#eta| < 0.8"
    elif bin == "2":
        return "0.8 < |#eta| < 1.6"
    elif bin == "3":
        return "1.6 < |#eta| < 2.0"
    elif bin == "4":
        return "2.0 < |#eta| < 2.2"
    elif bin == "5":
        return "|#eta| > 2.2"
    elif bin == "Inclusive":
        return bin
    else:
        raise Exception(ShellStyles.ErrorStyle() + "Unexpected bin %s" % (bin)  + ShellStyles.NormalStyle())

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
        if 0:
            datasetsMgr.printSelections()
            #PrintPSet("BJetSelection", datasetsMgr, depth=150)

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
        datasetsMgr.merge("EWK", aux.GetListOfEwkDatasets())
            
        # Print dataset information
        datasetsMgr.PrintInfo()
        
        # List of TDirectoryFile (_CRone, _CRtwo, _VR, _SR)
        tdirs  = ["LdgTrijetPt_"   , "LdgTrijetMass_"  , "LdgTrijetBJetBdisc_", "TetrajetBJetPt_",
                  "TetrajetBJetEta_", "TetrajetBJetBdisc_" , "LdgTetrajetPt_", "LdgTetrajetMass_"]
        region = ["CRone", "CRtwo"]
        hList  = []
        for d in tdirs:
            for r in region:
                hList.append(d + r)

        # Get the folders with the binned histograms
        folderList_ = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(opts.folder)
        folderList  = [h for h in folderList_ if h in hList]
        
        # For-loop: All folders
        histoPaths = []
        for f in folderList:
            folderPath = os.path.join(opts.folder, f)
            histoList  = datasetsMgr.getDataset(datasetsMgr.getAllDatasetNames()[0]).getDirectoryContent(folderPath)            
            pathList   = [os.path.join(folderPath, h) for h in histoList]
            histoPaths.extend( pathList )

        # Get all the bin labels 
        binLabels = GetBinLabels("CRone", histoPaths)
    
        for i, t in enumerate(tdirs, 1):
            myList = []
            for p in histoPaths:
                if t in p:
                    myList.append(p)
            msg   = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i, "/", "%s:" % (len(tdirs)), t.replace("_", ""))
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)

            PlotHistograms(datasetsMgr, myList, binLabels, opts)

    # Save the plots
    Print("All plots saved under directory %s" % (ShellStyles.NoteStyle() + aux.convertToURL(opts.saveDir, opts.url) + ShellStyles.NormalStyle()), True)
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
        
def getBinningForPt(binLevel=0):
    myBins = []
    if binLevel == 0:  #default binning
        for i in range(0, 300, 25):
            myBins.append(i)
        for i in range(300, 600, 50):
            myBins.append(i)
        for i in range(600, 1000+100, 100):
            myBins.append(i)
    elif binLevel == 1: #finer
        for i in range(0, 300, 10):
            myBins.append(i)
        for i in range(300, 600, 20):
            myBins.append(i)
        for i in range(600, 1000+100, 40):
            myBins.append(i)
    else:
        raise Exception(ShellStyles.ErrorStyle() + "Please choose bin-level from 0 to 1" + ShellStyles.NormalStyle())
    return myBins

def GetHistoPathDict(histoList, printList=False):
    '''
    Maps keys to histogram paths in the ROOT files
    The key naming is in the form 
    region - bin (- Triplet)
    for example:
    CRone - Inclusive
    CRone - Inclusive - EWKGenuineB
    CRone - Inclusive - EWKFakeB
    or:
    CRone - 0
    CRone - 0 - EWKGenuineB
    CRone - 0 - EWKFakeB
    '''
    histoDict = {}

    # For-loop: All histograms (full paths)
    for h in histoList:

        inclu, genuB, fakeB = GetHistoLabelTriplet(h)
        histoDict[inclu] = h
        histoDict[genuB] = h.replace(opts.folder, opts.folder + "EWKGenuineB")
        histoDict[fakeB] = h.replace(opts.folder, opts.folder + "EWKFakeB")

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

def GetHistoLabelTriplet(histoName):
    if "_SR" in histoName:
        region = "SR"
    elif "_VR" in histoName:
        region = "VR"
    elif "_CRone" in histoName:
        region = "CRone"
    elif "_CRtwo" in histoName:
        region = "CRtwo"
    else:
        raise Exception("Could not determine Control Region for histogram %s" % (h) )

    # Save histogram in dictionary
    binLabel = histoName.split(region)[-1]
    inclu = "%s-%s" % (region, binLabel)
    genuB = "%s-%s-%s" % (region, binLabel, "EWKGenuineB")
    fakeB = "%s-%s-%s" % (region, binLabel, "EWKFakeB")
    return inclu, genuB, fakeB


def GetRootHistos(datasetsMgr, histoList):
    hPathDict = GetHistoPathDict(histoList, printList=False)
    rhDict    = {}

    # For-loop: All histograms
    for h in histoList:
        inclu, genuB, fakeB = GetHistoLabelTriplet(h)

        pIncl  = plots.DataMCPlot(datasetsMgr, hPathDict[inclu])
        pGenB  = plots.DataMCPlot(datasetsMgr, hPathDict[genuB])
        pFakeB = plots.DataMCPlot(datasetsMgr, hPathDict[fakeB])

        # Define mapping keys: "Datasets-Region-Bin-Triplet"
        key1 = "Data-%s" % (inclu)
        key2 = "EWKGenuineB-%s" % (genuB)
        key3 = "EWKFakeB-%s" % (fakeB)
        key4 = "FakeB-%s" % (inclu)

        # Clone and Save the root histograms
        rhDict[key1] = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("Data-" + h)
        rhDict[key2] = pGenB.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKGenuineB-" + h)
        rhDict[key3] = pFakeB.histoMgr.getHisto("EWK").getRootHisto().Clone("EWKFakeB-" + h)
        rhDict[key4] = pIncl.histoMgr.getHisto("Data").getRootHisto().Clone("FakeB-" + h)
        rhDict[key4].Add( rhDict[key2], -1 )
            
    # For debugging:
    if 0:
        for k in rhDict:
            if "FakeB" not in k:
                continue
            fakeBResult.PrintTH1Info(rhDict[k])
    return rhDict


def PlotHistograms(datasetsMgr, histoList, binLabels, opts):

    '''
    histoList contains all histograms for all bins for CR1 and CR2 
    
    '''
    # Get the root histos for all datasets and Control Regions (CRs)
    rhDict  = GetRootHistos(datasetsMgr, histoList)

    # Get unique a style for each region
    for key1 in rhDict:

        # Definitions
        region1      = "CRone"
        region2      = "CRtwo"
        key2         = key1.replace(region1, region2)
        dataset      = key1.split("-")[0]
        region       = key1.split("-")[1]
        bin          = key1.split("-")[2]
        hName1       = rhDict[key1].GetName()
        hName2       = rhDict[key2].GetName()
        bInclusive   = "Inclusive" in key1

        # Dataset and Region filter
        if dataset != "FakeB":
            continue
        if region != region1:
            continue
        
        # Normalise to unity
        if bInclusive:
            rFakeB_CRone = rhDict[key1].Clone()
            w1 = rFakeB_CRone.Integral()
            rFakeB_CRone.Reset()

            rFakeB_CRtwo = rhDict[key2].Clone()
            w2 = rFakeB_CRtwo.Integral()
            rFakeB_CRtwo.Reset()

            for i, b in enumerate(binLabels, 1):
                if "Inclusive" in b:
                    continue
                # Determine keys
                k1 = key1.replace("Inclusive", b)
                k2 = key2.replace("Inclusive", b)

                # Normalise bin histo to one (before adding to inclusive histo)
                h1 = rhDict[k1].Clone()
                h2 = rhDict[k2].Clone()
                h1.Scale(1.0/h1.Integral())
                h2.Scale(1.0/h2.Integral())

                # Add this binned histo to the inclusive histo
                Verbose("Adding %s" % k1, True)
                rFakeB_CRone += h1 #rhDict[k1]
                rFakeB_CRtwo += h2 #rhDict[k2]
        else:
            # Get the histos
            rFakeB_CRone = rhDict[key1]
            rFakeB_CRtwo = rhDict[key2]

        # Normalise the histos?
        if opts.normaliseToOne:
            rFakeB_CRone.Scale(1.0/rFakeB_CRone.Integral())
            rFakeB_CRtwo.Scale(1.0/rFakeB_CRtwo.Integral())


        # Apply histogram styles          
        styles.getABCDStyle("CRone").apply(rFakeB_CRone)
        styles.getABCDStyle("CRtwo").apply(rFakeB_CRtwo)
        
        # Create the plot
        p = plots.ComparisonManyPlot(rFakeB_CRone, [rFakeB_CRtwo], saveFormats=[])
        p.setLuminosity(opts.intLumi)
    
        # Set draw/legend style
        p.histoMgr.setHistoDrawStyle(hName1, "AP")
        p.histoMgr.setHistoDrawStyle(hName2, "HIST")
        p.histoMgr.setHistoLegendStyle(hName1, "LP")
        p.histoMgr.setHistoLegendStyle(hName2, "F")
        
        # Set legend labels
        p.histoMgr.setHistoLegendLabelMany({
                hName1 : "CR1",
                hName2 : "CR2",
                })

        # Draw the plot and save it
        if bin == "Inclusive":
            histoName = histoList[0] + "_CR1vCR2"
        else:
            histoName = histoList[0] + "_CR1vCR2_bin%s" % (bin)
        saveName = histoName.split("/")[-1].replace("CRone0_", "").replace("CRtwo0_", "")
        
        # Get the histogram customisations (keyword arguments)
        p.appendPlotObject(histograms.PlotText(0.20, 0.88, GetBinText(bin), bold=True, size=22))
        plots.drawPlot(p, saveName, **GetHistoKwargs(saveName))
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
    ANALYSISNAME = "FakeBMeasurement"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    INTLUMI      = -1.0
    URL          = False
    SAVEDIR      = None
    VERBOSE      = False
    USEMC        = False
    RATIO        = False
    FOLDER       = "ForFakeBMeasurement"
    NORMALISE    = False

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

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", default=NORMALISE,
                      help="Normalise the baseline and inverted shapes to one? [default: %s]" % (NORMALISE) )

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store", 
                      help="List of datasets in mcrab to exclude")

    parser.add_option("--useMC", dest="useMC", action="store_true", default=USEMC,
                      help="Use QCD MC instead of QCD=Data-EWK? [default: %s]" % (USEMC) )

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
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="Closure/Binned")

    main(opts)

    if not opts.batchMode:
        raw_input("=== plot_ClosureBinned.py: Press any key to quit ROOT ...")
