#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
./plotDataDriven.py -m <pseudo_mcrab_directory> [opts]


EXAMPLES:
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_HLTBJetTrgMatch_TopCut10_H2Cut0p5_170720_104648 --url -o ""
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_170817_025841/ --url --signalMass 500
./plotDataDriven.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_HLTBJetTrgMatch_TopCut10_H2Cut0p5_170720_104648 --url --signalMass 800


LAST USED:
./plotDataDriven.py -m Hplus2tbAnalysis_3bjets40_MVA0p88_MVA0p88_TopMassCutOff600GeV_180113_050540 -n FakeBMeasurement_PreSel_3bjets40_SigSel_MVA0p85_InvSel_EE2CSVM_MVA0p60to085_180120_092605/FakeB/ --gridX --gridY --logY --signal 500
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

def rchop(myString, endString):
  if myString.endswith(endString):
    return myString[:-len(endString)]
  return myString

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
    return  ["TT", "WJetsToQQ_HT_600ToInf", "SingleTop", "DYJetsToQQHT", "TTZToQQ",  "TTWJetsToQQ", "Diboson", "TTTT"]

def GetDatasetsFromDir(opts, otherDir=False):
    
    myDir    = opts.mcrab1
    analysis = opts.analysisName
    if otherDir:
        myDir    = opts.mcrab2        
        #analysis = "FakeBMeasurement"
    datasets = dataset.getDatasetsFromMulticrabDirs([myDir],
                                                    dataEra=opts.dataEra,
                                                    searchMode=opts.searchMode, 
                                                    analysisName=analysis,
                                                    optimizationMode=opts.optMode)
    return datasets
    
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

def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(False)
    style.setGridX(opts.gridX)
    style.setGridY(opts.gridY)
    style.setLogX(opts.logX)
    style.setLogY(opts.logY)

    #optModes = ["", "OptChiSqrCutValue50", "OptChiSqrCutValue100"]
    optModes = [""]

    if opts.optMode != None:
        optModes = [opts.optMode]
        
    # For-loop: All opt Mode
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        dsetMgr1 = GetDatasetsFromDir(opts, False) 
        dsetMgr2 = GetDatasetsFromDir(opts, True)

        # Setup the dataset managers
        dsetMgr1.updateNAllEventsToPUWeighted()
        dsetMgr2.updateNAllEventsToPUWeighted()

        # Load luminosities
        dsetMgr1.loadLuminosities() # from lumi.json
        # dsetMgr2.loadLuminosities()

        # Print PSets. Perhaps i can use this to ensure parameters are matching!
        if 0:
            dsetMgr1.printSelections()
            dsetMgr2.printSelections()
            PrintPSet("FakeBMeasurement", dsetMgr1)
            PrintPSet("TopSelectionBDT" , dsetMgr2)

        # Remove datasets with overlap?
        removeList = ["QCD-b"]
        dsetDY     = "DYJetsToQQ_HT180"
        dsetZJ     = "ZJetsToQQ_HT600toInf"
        dsetRM     = dsetZJ # datasets with overlap
        removeList.append(dsetRM)
        #if opts.useMC: #fixme
        #    removeList.append("FakeB")

        # Set/Overwrite cross-sections. Remove all but 1 signal mass 
        for d in dsetMgr1.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                dsetMgr1.getDataset(d.getName()).setCrossSection(1.0) # ATLAS 13 TeV H->tb exclusion limits
                if d.getName() != opts.signal:
                    removeList.append(d.getName())

        # Print useful information?
        if opts.verbose:
            dsetMgr1.PrintCrossSections()
            dsetMgr1.PrintLuminosities()
            dsetMgr2.PrintCrossSections()
            dsetMgr2.PrintLuminosities()

        # Merge histograms
        plots.mergeRenameReorderForDataMC(dsetMgr1) 
        # plots.mergeRenameReorderForDataMC(dsetMgr2) 
   
        # Get the luminosity
        if opts.intLumi < 0:
            opts.intLumi = dsetMgr1.getDataset("Data").getLuminosity()

        # Custom Filtering of datasets 
        for i, d in enumerate(removeList, 1):
            msg = "Removing datasets %s from dataset manager" % (ShellStyles.NoteStyle() + d + ShellStyles.NormalStyle())
            Verbose(msg, i==1)
            dsetMgr1.remove(filter(lambda name: d == name, dsetMgr1.getAllDatasetNames()))

        # Replace MC datasets with data-driven
        if not opts.useMC: #fixme
            replaceQCD(dsetMgr1, dsetMgr2, "FakeBTrijetMass", "FakeB") #dsetMgr1 now contains "FakeB" pseudo-dataset

        # Print dataset information
        dsetMgr1.PrintInfo()
        dsetMgr2.PrintInfo()

        # Do Data-MC histograms with DataDriven QCD
        PlotHistograms(dsetMgr1, dsetMgr2, opts)
    return

def GetHistoKwargs(histoList, opts):
    '''
    Dictionary with 
    key   = histogramName
    value = kwargs
    '''
    
    histoKwargs = {}
    _moveLegend = {"dx": -0.1, "dy": -0.01, "dh": 0.1}
    if opts.logY:
        ymaxF = 4
    else:
        ymaxF = 1.2
    step1 = 20
    step2 = 50
    step3 = 100
    step4 = 200
    step5 = 2000

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
        "opts"             : {"ymin": 2e-1, "ymaxfactor": ymaxF},
        "opts2"            : {"ymin": 0.6, "ymax": 2.0-0.6},
        "log"              : opts.logY,
        "moveLegend"       : _moveLegend,
        "cutBoxY"          : {"cutValue": 1.2, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": False, "ratioCanvas": True}
        }

    for h in histoList:
        kwargs = copy.deepcopy(_kwargs)
        if "met" in h.lower():
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units            
            kwargs["xlabel"] = "E_{T}^{miss} (%s)" % units
            kwargs["rebinX"] = 2
        if "NVertices" in h:
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "Vertices"
        if "Njets" in h:                
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "Jets Multiplicity"
            kwargs["cutBox"] = {"cutValue": 7.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 7.0, "xmax": +16.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
            ROOT.gStyle.SetNdivisions(10, "X")
        if "JetPt" in h:                
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "JetEta" in h:                
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "#eta"
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "NBjets" in h:                
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "b-Jets Multiplicity"
            kwargs["cutBox"] = {"cutValue": 3.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 10.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "BjetPt" in h:                
            units = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 30.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        if "BjetEta" in h:                
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "#eta"
            kwargs["cutBox"] = {"cutValue": 0.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "BtagDiscriminator" in h:                
            kwargs["ylabel"]     = "Events / %.2f"
            kwargs["xlabel"]     = "b-Tag Discriminator"
            kwargs["cutBox"]     = {"cutValue": 0.8484, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["moveLegend"] = {"dx": -0.5, "dy": -0.01, "dh": 0.0}
            kwargs["opts"]       = {"xmin": 0.0, "xmax": 1.05, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "HT" in h:
            units            = "GeV"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "H_{T} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["rebinX"] = 5
            kwargs["opts"]   = {"xmin": 500.0, "xmax": 3000, "ymin": 1e+0, "ymaxfactor": ymaxF}
            # kwargs["opts"]   = {"xmin": 500.0, "xmax": 4100, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "MHT" in h:
            units            = "GeV"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "MHT (%s)"  % units
            kwargs["rebinX"] = 2
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 400, "ymin": 1e+0, "ymaxfactor": ymaxF}
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
            kwargs["opts"]   = {"xmin": 0.0, "xmax": +1.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
            kwargs["moveLegend"] = {"dx": +0.0}
            #kwargs["moveLegend"] = {"dx": -0.53, "dy": -0.5, "dh": 0.0}
        if "Centrality" in h:
            kwargs["ylabel"] = "Events / %.2f"
            kwargs["xlabel"] = "Centrality"
            kwargs["moveLegend"] = {"dx": -0.53, "dy": 0.0, "dh": 0.0}
        if "TopFitChiSqr" in h:
            kwargs["ylabel"] = "Events / %.0f"
            kwargs["xlabel"] = "#chi^{2}"
            kwargs["cutBox"] = {"cutValue": 100.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["rebinX"] = 2
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 180.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "LdgTrijetPt" in h:
            units = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "LdgTrijetDijetPt" in h:
            units = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 700.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "LdgTrijetMass" in h:
            startBlind       = 115 #135 v. sensitive to bin-width!
            endBlind         = 225 #205 v. sensitive to bin-width!
            kwargs["rebinX"] = 4
            units            = "GeV/c^{2}"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "m_{jjb} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 1200.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
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
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": ymaxF}
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
            kwargs["opts"]   = {"xmin": 0.0, "xmax": 1200.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
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
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "LdgTetrajetPt" in h:
            units            = "GeV/c"
            kwargs["ylabel"] = "Events / %.0f " + units
            kwargs["xlabel"] = "p_{T} (%s)"  % units
        if "LdgTetrajetMass" in h:
            myBins = []
            for j in range(0, 1000, step2):
                myBins.append(j)
            for k in range(1000, 2000, step3):
                myBins.append(k)
            for l in range(2000, 4000+step5, step4):
                myBins.append(l)

            ROOT.gStyle.SetNdivisions(5, "X")
            startBlind       = 150  # 135 v. sensitive to bin-width!
            endBlind         = 2500 #v. sensitive to bin-width!
            kwargs["rebinX"] = myBins
            units            = "GeV/c^{2}"
            #kwargs["ylabel"] = "Events / %.0f " + units
            binWmin, binWmax = GetBinWidthMinMax(myBins)
            kwargs["ylabel"] = "Events / %.0f-%.0f %s" % (binWmin, binWmax, units)
            kwargs["xlabel"] = "m_{jjbb} (%s)"  % units
            kwargs["cutBox"] = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            kwargs["opts"]   = {"xmin": 0.0, "xmax": endBlind, "ymin": 1e+0, "ymaxfactor": ymaxF}
            #kwargs["opts"]   = {"xmin": 0.0, "xmax": 2000, "ymin": 1e+0, "ymaxfactor": ymaxF}
            if "AllSelections" in h:
                # kwargs["blindingRangeString"] = "%s-%s" % (startBlind, endBlind) #ale
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
            kwargs["opts"]   = {"xmin": 0.0, "xmax": endBlind, "ymin": 1e+0, "ymaxfactor": ymaxF}
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
            kwargs["opts"]   = {"xmin": -2.5, "xmax": +2.5, "ymin": 1e+0, "ymaxfactor": ymaxF}
        if "TopMassWMassRatio" in h:
            kwargs["ylabel"] = "Events / %.1f"
            kwargs["xlabel"] = "R_{3/2}"
            kwargs["cutBox"] = {"cutValue": (173.21/80.385), "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            # kwargs["cutBox"] = {"cutValue": (172.5/80.385), "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            #kwargs["cutBox"] = {"cutValue": 2.1, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
            #kwargs["opts"]   = {"xmin": 0, "xmax": +10.0, "ymin": 1e+0, "ymaxfactor": 1.2}
            kwargs["opts"]   = {"xmin": 0, "xmax": +10.0, "ymin": 1e+0, "ymaxfactor": ymaxF}
            kwargs["log"]    = True#False

        histoKwargs[h] = kwargs
    return histoKwargs
    
def PlotHistograms(datasetMgr, datasetMgr2, opts):

    # Definitions
    histoNames  = []    
    allHistos   = datasetMgr2.getAllDatasets()[0].getDirectoryContent(opts.folder)
    histoList1  = [h for h in allHistos if "MCEWK" not in h]
    histoList2  = [h for h in histoList1 if "Purity" not in h]
    histoList3  = [h for h in histoList2 if "Bjet" not in h]
    histoList4  = [h for h in histoList3 if "Jet" not in h]
    histoList5  = [h for h in histoList4 if "Njet" not in h]
    histoList6  = [h for h in histoList5 if "Njet" not in h]
    histoList7  = [h for h in histoList6 if "MVA" not in h]
    histoList8  = [h for h in histoList7 if "Sub" not in h]
    histoPaths  = [opts.folder + "/" + h for h in histoList8]

    # Get histogram<->kwargs dictionary 
    histoKwargs = GetHistoKwargs(histoPaths, opts)

    # For-loop: All histograms in list
    for histoName in histoPaths:

        #if "MET_" not in histoName:
        #    continue
        if "TetrajetMass_" not in histoName:
            continue

        kwargs_  = histoKwargs[histoName]
        saveName = histoName.replace(opts.folder + "/", "")

        # Create the plotting object (Data, "FakeB")
        p1 = plots.DataMCPlot(datasetMgr, histoName, saveFormats=[])
        
        # Keep only EWK (GenuineB) datasets
        datasetMgr.selectAndReorder(GetListOfEwkDatasets())
        
        # Create the MCPlot for the EWKGenuineB histograms
        histoNameGenuineB = histoName.replace(opts.folder, opts.folder + "EWKGenuineB")
        p2 = plots.MCPlot(datasetMgr, histoNameGenuineB, normalizeToLumi=opts.intLumi, saveFormats=[])

        # Add the datasets to be included in the plot
        myStackList = []
        # Data-driven FakeB background
        if not opts.useMC:
            hFakeB  = p1.histoMgr.getHisto("FakeB").getRootHisto()
            hhFakeB = histograms.Histo(hFakeB, "FakeB", legendLabel="Fake-b")
            hhFakeB.setIsDataMC(isData=False, isMC=True)
            myStackList.append(hhFakeB)
        else:
            hQCD  = p1.histoMgr.getHisto("QCD").getRootHisto()
            hhQCD = histograms.Histo(hQCD, "QCD", legendLabel="QCD")
            hhQCD.setIsDataMC(isData=False, isMC=True)
            myStackList.append(hhQCD)
            pass

        # EWK GenuineB background (Replace all EWK histos with GenuineB histos)
        ewkNameList  = GetListOfEwkDatasets()
        ewkHistoList = []
        # For-loop: All EWK datasets 
        for dataset in ewkNameList:
            h = p2.histoMgr.getHisto(dataset).getRootHisto()
            hh = histograms.Histo(h, dataset,  plots._legendLabels[dataset])
            hh.setIsDataMC(isData=False, isMC=True)
            myStackList.append(hh)

        # Collision data
        hData  = p1.histoMgr.getHisto("Data").getRootHisto()
        hhData = histograms.Histo(hData, "Data")
        hhData.setIsDataMC(isData=True, isMC=False)
        myStackList.insert(0, hhData)

        # Signal
        hSignal  = p1.histoMgr.getHisto(opts.signal).getRootHisto()
        hhSignal = histograms.Histo(hSignal, opts.signal, plots._legendLabels[opts.signal])
        hhSignal.setIsDataMC(isData=False, isMC=True)
        myStackList.insert(1, hhSignal)

        p3 = plots.DataMCPlot2(myStackList, saveFormats=[])
        p3.setLuminosity(opts.intLumi)
        # p3.setEnergy("%d"%self._config.OptionSqrtS)
        p3.setDefaultStyles()

#        # Apply QCD data-driven style
#        if opts.signalMass != 0:
#            signal = "ChargedHiggs_HplusTB_HplusToTB_M_%.0f" % opts.signalMass
#            mHPlus = "%s" % int(opts.signalMass)
#            p.histoMgr.forHisto(signal, styles.getSignalStyleHToTB_M(mHPlus))
#
#        #p.histoMgr.forHisto(opts.signalMass, styles.getSignalStyleHToTB())
#        if opts.useMC:
#            pass
#        else:
#            p.histoMgr.forHisto("FakeB", styles.getFakeBStyle())
#            p.histoMgr.setHistoDrawStyle("FakeB", "HIST")
#            p.histoMgr.setHistoLegendStyle("FakeB", "F")
#
#        if not opts.useMC:
#            p.histoMgr.setHistoLegendLabelMany({
#                    "FakeB"   : "Fake b",
#                    })
#        else:
#            p.histoMgr.setHistoLegendLabelMany({
#                    "QCD": "QCD (MC)",
#                    })            
#                              
#        # Apply blinding of signal region
#        if "blindingRangeString" in kwargs_:
#            startBlind = float(kwargs_["blindingRangeString"].split("-")[1])
#            endBlind   = float(kwargs_["blindingRangeString"].split("-")[0])
#            plots.partiallyBlind(p, maxShownValue=startBlind, minShownValue=endBlind, invert=True, moveBlindedText=kwargs_["moveBlindedText"])
#
        # Draw and save the plot
        plots.drawPlot(p3, saveName, **kwargs_) #the "**" unpacks the kwargs_ dictionary
        SavePlot(p3, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])
    return

def PrintPSet(selection, dsetMgr):
    selection = "\"%s\":"  % (selection)
    thePSets = dsetMgr.getAllDatasets()[0].getParameterSet()

    # First drop everything before the selection
    thePSet_1 = thePSets.split(selection)[-1]

    # Then drop everything after the selection
    thePSet_2 = thePSet_1.split("},")[0]

    # Final touch
    thePSet = selection + thePSet_2

    Print(thePSet, True)
    return

def getHisto(dsetMgr, datasetName, histoName):
    Verbose("getHisto()", True)

    h1 = dsetMgr.getDataset(datasetName).getDatasetRootHisto(histoName)
    h1.setName(datasetName)
    return h1

def replaceQCD(dMgr1, dMgr2, newName, newLabel="FakeB"):
    '''
    Replaces the QCD dataset with 
    a data-driven pseudo-dataset
    '''
    
    # Define variables
    oldName    = "QCD"
    newDataset = dMgr2.getDataset(newName)
    dMgr1.append(newDataset)
    newDataset.setName(newLabel)

    # Get list of dataset names
    names = dMgr1.getAllDatasetNames()

    # Return the index in the list of the first dataset whose name is oldName.
    index = names.index(oldName)

    # Remove the dataset at the given position in the list, and return it. 
    names.pop(index)
    
    # Insert the dataset to the given position  (index) of the list
    names.insert(index, newDataset.getName())

    # Remove from the dataset manager the oldName
    dMgr1.remove(oldName)
    names.pop(names.index(newDataset.getName()))
    
    # Select and reorder Datasets. 
    # This method can be used to either select a set of dataset.Dataset objects. reorder them, or both.
    dMgr1.selectAndReorder(names)
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
    USEMC        = False
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = None
    BATCHMODE    = True
    INTLUMI      = -1.0
    SIGNALMASS   = 0
    SIGNAL       = None
    URL          = False
    SAVEDIR      = "/publicweb/a/aattikis/DataDriven/"
    VERBOSE      = False
    GRIDX        = False
    GRIDY        = False
    LOGX         = False
    LOGY         = False
    FOLDER       = "ForDataDrivenCtrlPlots"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab1", dest="mcrab1", action="store", 
                      help="Path to the multicrab directory with the Hplus2tbAnalysis")

    parser.add_option("-n", "--mcrab2", dest="mcrab2", action="store", 
                      help="Path to the multicrab directory with the data-driven pseudo-datasets (e.g. FakeB)")

    parser.add_option("-o", "--optMode", dest="optMode", type="string", default=OPTMODE, 
                      help="The optimization mode when analysis variation is enabled  [default: %s]" % OPTMODE)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--analysisName", dest="analysisName", type="string", default=ANALYSISNAME,
                      help="Override default analysisName [default: %s]" % ANALYSISNAME)

    parser.add_option("--useMC", dest="useMC", action="store_true", default=USEMC,
                      help="Use all backgrounds from MC. Do not use data-driven background estimation [default: %s]" % USEMC)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--searchMode", dest="searchMode", type="string", default=SEARCHMODE,
                      help="Override default searchMode [default: %s]" % SEARCHMODE)

    parser.add_option("--dataEra", dest="dataEra", type="string", default=DATAERA, 
                      help="Override default dataEra [default: %s]" % DATAERA)

    parser.add_option("--signalMass", dest="signalMass", type=float, default=SIGNALMASS, 
                     help="Mass value of signal to use [default: %s]" % SIGNALMASS)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--gridX", dest="gridX", action="store_true", default=GRIDX,
                      help="Enable the x-axis grid lines [default: %s]" % GRIDX)

    parser.add_option("--gridY", dest="gridY", action="store_true", default=GRIDY,
                      help="Enable the y-axis grid lines [default: %s]" % GRIDY)

    parser.add_option("--logX", dest="logX", action="store_true", default=LOGX,
                      help="Set x-axis to logarithm scale [default: %s]" % LOGX)

    parser.add_option("--logY", dest="logY", action="store_true", default=LOGY,
                      help="Set y-axis to logarithm scale [default: %s]" % LOGY)

    parser.add_option("--folder", dest="folder", action="store_true", default=FOLDER,
                      help="Folder inside the ROOT files where all histograms for plotting are located [default: %s]" % FOLDER)


    (opts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    if opts.mcrab1 == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)
    elif opts.mcrab2 == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        #print __doc__
        sys.exit(1)
    else:
        mcrabDir = rchop(opts.mcrab1, "/")
        if len(mcrabDir.split("/")) > 1:
            mcrabDir = mcrabDir.split("/")[-1]
        opts.saveDir += mcrabDir + "/" + "DataDriven/" #opts.folder


    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 1500, 2000, 2500, 3000, 5000, 7000]
    if opts.signalMass!=0 and opts.signalMass not in allowedMass:
        Print("Invalid signal mass point (=%.0f) selected! Please select one of the following:" % (opts.signalMass), True)
        for m in allowedMass:
            Print(m, False)
        sys.exit()
    else:
        opts.signal = "ChargedHiggs_HplusTB_HplusToTB_M_%i" % opts.signalMass

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== plotDataDriven.py: Press any key to quit ROOT ...")
