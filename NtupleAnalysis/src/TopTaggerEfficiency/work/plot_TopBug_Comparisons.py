#!/usr/bin/env python
'''
Description:

Usage:
./plot_TopBug_Comparisons.py -m <pseudo_mcrab> [opts]

Examples:
./plot_TopBug_Comparisons.py -m TopTaggerEfficiency_180609_TopRecoBugFixed/ --mcrab1 TopTaggerEfficiency_180608_MassCut300_BeforeBugFix/ --url -v

Last Used:
./plot_TopBug_Comparisons.py -m /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_14June18_BDT0p40_Masscut300_NewTop_BugFix --mcrab1 /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_14June18_BDT0p40_Masscut300_NewTop_BUG --url -v

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import math
import copy
import os
import getpass
from optparse import OptionParser
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

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


import warnings
warnings.filterwarnings("ignore")

ROOT.gErrorIgnoreLevel = ROOT.kError

kwargs = {
    "verbose"          : False,
    "dataEra"          : None,
    "searchMode"       : None,
    "analysis"         : "TopTaggerEfficiency",
    "optMode"          : "",
    "savePath"         : None,
    "saveFormats"      : [".pdf"],
    "xlabel"           : None,
    "ylabel"           : "Probability",
    "rebinX"           : 2,
    "rebinY"           : 2,
    "xlabelsize"       : None,
    "ratio"            : True,
    "ratioYlabel"      : None,
    "ratioInvert"      : False,
    "addMCUncertainty" : False,
    "addLuminosityText": False,
    "addCmsText"       : True,
    "errorBarsX"       : True,
    "logX"             : False,
    "logY"             : False,
    "gridX"            : True,
    "gridY"            : True,
    "cmsExtraText"     : "Simulation",
    "removeLegend"     : False,
    "moveLegend"       : {"dx": -0.1, "dy": +0.0, "dh": +0.1},
    "cutValue"         : None,
    "cutLine"          : False,
    "cutBox"           : False,
    "cutLessthan"      : False,
    "cutFillColour"    : ROOT.kAzure-4,
    }

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
    aux.Print(msg, printHeader)
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


def GetListOfEwkDatasets():
    Verbose("Getting list of EWK datasets")
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]


def GetDatasetsFromDir(opts, mcrab):
    Verbose("Getting datasets")
    
    if (not opts.includeOnlyTasks and not opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode, 
                                                        analysisName=opts.analysisName,
                                                        optimizationMode=opts.optMode)
    elif (opts.includeOnlyTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        includeOnlyTasks=opts.includeOnlyTasks,
                                                        optimizationMode=opts.optMode)
    elif (opts.excludeTasks):
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                        dataEra=opts.dataEra,
                                                        searchMode=opts.searchMode,
                                                        analysisName=opts.analysisName,
                                                        excludeTasks=opts.excludeTasks,
                                                        optimizationMode=opts.optMode)
    else:
        raise Exception("This should never be reached")
    return datasets
    

def main(opts, signalMass):

    optModes = ["OptChiSqrCutValue100"]                                                                                                                             

    if opts.optMode != None:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts, opts.mcrab)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json

        datasetsMgrRef = GetDatasetsFromDir(opts, opts.mcrab1)
        datasetsMgrRef.updateNAllEventsToPUWeighted()
        datasetsMgrRef.loadLuminosities() # from lumi.json

        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
                datasetsMgrRef.getDataset(d.getName()).setCrossSection(1.0)
               
        
        # Determine integrated Lumi before removing data
        #intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        intLumi = 35920
        
        # Remove datasets
        if 1:
            datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "SingleTop" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "DYJetsToQQHT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTZToQQ" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTWJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "WJetsToQQ" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "Diboson" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "TTTT" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "FakeBMeasurementTrijetMass" in name, datasetsMgr.getAllDatasetNames()))
            #datasetsMgr.remove(filter(lambda name: "M_" in name and "M_" + str(opts.signalMass) not in name, datasetsMgr.getAllDatasetNames()))

        # Merge histograms (see NtupleAnalysis/python/tools/plots.py) 
        plots.mergeRenameReorderForDataMC(datasetsMgr) 
        plots.mergeRenameReorderForDataMC(datasetsMgrRef) 

        # Re-order datasets
        datasetOrder = []
        for d in datasetsMgr.getAllDatasets():
            if "M_" in d.getName():
                if d not in signalMass:
                    continue
            datasetOrder.append(d.getName())
            #newOrder = ["TT", "QCD"]
            #newOrder = ["TT", "QCD"]
        for m in signalMass:
            #newOrder.insert(0, m)
            datasetOrder.insert(0, m)
            #datasetsMgr.selectAndReorder(newOrder)
        datasetsMgr.selectAndReorder(datasetOrder)
        datasetsMgrRef.selectAndReorder(datasetOrder)

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(False)
        style.setGridY(False)

        # Do the topSelection histos
        folder      = opts.folder 
        histoPaths1 = []
        if folder != "":
            histoList  = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folder)
            # hList0     = [x for x in histoList if "TrijetMass" in x]
            # hList1     = [x for x in histoList if "TetrajetMass" in x]
            # hList2     = [x for x in histoList if "TetrajetBJetPt" in x]
            # histoPaths1 = [os.path.join(folder, h) for h in hList0+hList1+hList2]
            histoPaths1 = [os.path.join(folder, h) for h in histoList]
        
        folderTarg     = "topbdtSelection_" #topSelectionBDT_
        folderRef      = "topbdtSelection_"
        #folderTarg = "counters/weighted"
        #folderRef  = "counters/weighted"
        #folderTarg = "counters"
        #folderRef  = "counters"

        histoListTarg = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folderTarg)
        histoListRef  = datasetsMgrRef.getDataset(datasetOrder[0]).getDirectoryContent(folderRef)

        histoPathsTarg = [os.path.join(folderTarg, h) for h in histoListTarg]
        histoPathsRef  = [os.path.join(folderRef, h) for h in histoListRef]

        for i in range(len(histoPathsTarg)):
            hT = histoPathsTarg[i]
            hR = histoPathsRef[i]
            print "TYPE", type(hT), hT
            if "Vs" in hT: # Skip TH2D
                continue
            if "weighted" in hT:
                continue
            #PlotMC(datasetsMgr, h, intLumi)
            Plot_Comparisons(datasetsMgr, datasetsMgrRef, hT, hR, intLumi)


    return

def GetHistoKwargs(histoName, opts):
    '''                                                                                                                                                                                                                 
    Dictionary with                                                                                                                                                                                                     
    key   = histogram name                                                                                                                                                                                              
    value = kwargs                                                                                                                                                                                                      
    '''
    h = histoName.lower()
    kwargs     = {
        "xlabel"           : "x-axis",
        "ylabel"           : "Efficiency / ", #/ %.1f ",                                                                                                                                                                
        # "rebinX"           : 1,                                                                                                                                                                                       
        "ratioYlabel"      : "Ratio",
        "ratio"            : False,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        #"opts"             : {"ymin": 0.0, "ymax": 1.09},                                                                                                                                                              
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.1},
        "opts2"            : {"ymin": 0.6, "ymaxfactor": 1.1},
        "log"              : False,
#        "moveLegend"       : {"dx": -0.08, "dy": -0.01, "dh": -0.08},                                                                                                                                                  
        "moveLegend"       : {"dx": -0.05, "dy": -0.005, "dh": -0.08},
#        "moveLegend"       : {"dx": -0.57, "dy": -0.007, "dh": -0.18},                                                                                                                                                 
        "cutBoxY"          : {"cutValue": 1.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True, "mainCanvas": True, "ratioCanvas": False}
        }



def Plot_Comparisons(datasetsMgr, datasetsMgrRef, hT, hR, intLumi):
    #kwargs = {}
    _kwargs = {}
    #kwargs = GetHistoKwargs(hG, opts)

    print 
    if opts.normaliseToOne:
        pT = plots.MCPlot(datasetsMgr, hT, normalizeToOne=True, saveFormats=[], **_kwargs)
        pR = plots.MCPlot(datasetsMgrRef, hR, normalizeToOne=True, saveFormats=[], **_kwargs)
    else:
        pT = plots.MCPlot(datasetsMgr, hT, normalizeToLumi=intLumi, saveFormats=[], **_kwargs)
        pR = plots.MCPlot(datasetsMgrRef, hR, normalizeToLumi=intLumi, saveFormats=[], **_kwargs)

    # Draw the histograms                                                                                                                                                                
    _cutBox = None
    _rebinX = 1
    _format = "%0.2f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}


    print "HT", hT

    xMax = 200
    _kwargs = {
        "xlabel"           : _xlabel,
        "ylabel"           : "Events / %s" % (_format),
        "ratioYlabel"      : "Ratio ",
        "ratio"            : False,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        #"opts"             : {"ymin": 0.1, "ymaxfactor": 1.2},
        "opts"             : {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":xMax},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : True,
        #"createLegend"     : {"x1": 0.5, "y1": 0.75, "x2": 0.9, "y2": 0.9},                                                                                                                                         
        "createLegend"     : {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.82}, 
        "rebinX"           : 1,
        }


    if "counters" in hT.lower():
        print "HERE"
        ROOT.gStyle.SetLabelSize(16.0, "X")
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":6}
        _kwargs["createLegend"] = {"x1": 0.65, "y1": 0.6, "x2": 0.90, "y2": 0.77}, 

    if "pt" in hT.lower():
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _xlabel = "p_{T} (%s)" % _units
        _kwargs["xmax"] = 800
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":800}

    if "mass" in hT.lower():
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "M (%s)" % _units
        _kwargs["xmax"] = 800
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":800}
        if "tetrajet" in hT.lower():
            _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":2000}
            _kwargs["rebinX"] = 8
    if "trijetmass" in hT.lower():
        print "mass"
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{top} (%s)" % _units
        #_cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _kwargs["xmax"] = 400 #1005
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":400}

    if "eta" in hT.lower():
        _units  = ""
        _format = "%0.1f " + _units
        _xlabel = "#eta (%s)" % _units
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":-5.0, "xmax":+5.0}

    if "mult" in hT.lower():
        _format = "%0.0f"
        if "cleaned" in hT.lower():
            _kwargs["xmax"] = 10
            _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":10}
        else:
            _kwargs["xmax"] = 60
            _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":60}

    if "bdisc" in hT.lower():
        _format = "%0.2f"
        _kwargs["xmax"] = 1
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":1}

    if "topbdt" in hT.lower():
        _format = "%0.2f"
        _kwargs["xmax"] = 1
        _kwargs["xmin"] = 0.3
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0.3, "xmax":1.0}
            
    if "dijetmass" in hT.lower():
        print "dijet-mass"
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{W} (%s)" % _units
        _opts["xmax"] = 600
        _kwargs["opts"] = {"ymin": 0.1  ,"ymaxfactor": 1.2, "xmin":0, "xmax":300}


    else:
        pass


    if logY:
        yMaxFactor = 2.0
    else:
        yMaxFactor = 1.5

    _opts["ymaxfactor"] = yMaxFactor
    if opts.normaliseToOne:
        _opts["ymin"] = 1e-3
    else:
        _opts["ymin"] = 1e0

        
    myList = []
    # Customise styling
    pT.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
    pR.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))


    datasetTarg = datasetsMgr.getDataset("QCD") #ChargedHiggs_HplusTB_HplusToTB_M_500
    datasetRef  = datasetsMgrRef.getDataset("QCD") #ChargedHiggs_HplusTB_HplusToTB_M_500
    
    h = datasetTarg.getDatasetRootHisto(hT)
    #h.normalizeToOne()
    h.normalizeToLuminosity(intLumi)
    HT = h.getHistogram()

    h = datasetRef.getDatasetRootHisto(hR)
    #h.normalizeToOne()
    h.normalizeToLuminosity(intLumi)
    HR = h.getHistogram()


    altSignalBDTGStyle  = styles.StyleCompound([styles.StyleMarker(markerSize=1.2, markerColor=ROOT.kAzure+9, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                                styles.StyleLine(lineColor=ROOT.kAzure+9, lineStyle=ROOT.kSolid, lineWidth=3),
                                                styles.StyleFill(fillColor=ROOT.kAzure+9, fillStyle=3001)])

    altBackgroundBDTGStyle = styles.StyleCompound([styles.StyleMarker(markerSize=1.2, markerColor=ROOT.kRed-4, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                                   styles.StyleLine(lineColor=ROOT.kRed-4, lineStyle=ROOT.kSolid, lineWidth=3),
                                                   #styles.StyleFill(fillColor=ROOT.kRed-4)
                                                   ])

    signalStyle = styles.StyleCompound([styles.StyleMarker(markerSize=1.2, markerColor=ROOT.kTeal+2, markerSizes=None, markerStyle=ROOT.kFullTriangleUp),
                                        styles.StyleLine(lineColor=ROOT.kTeal+2, lineStyle=ROOT.kSolid, lineWidth=3),
                                        styles.StyleFill(fillColor=ROOT.kTeal+2, fillStyle=3001)])


    p = plots.ComparisonPlot(histograms.Histo(HT,"Target", "pl", "PL"), histograms.Histo(HR,"Reference", "pl", "PL"),) 
    p.histoMgr.setHistoLegendLabelMany({"Target": "bug fixed", "Reference": "bug"}) 

    if ("TT" in datasetTarg.getName()):    
        p.histoMgr.forHisto("Target", altBackgroundBDTGStyle ) 
        p.histoMgr.forHisto("Reference", altSignalBDTGStyle) 
    elif ("QCD" in datasetTarg.getName()):
        p.histoMgr.forHisto("Target"  , altBackgroundBDTGStyle)#styles.getABCDStyle("VR"))
        p.histoMgr.forHisto("Reference", styles.qcdFillStyle)
    elif ("Charged" in datasetTarg.getName()):
        p.histoMgr.forHisto("Target", altBackgroundBDTGStyle) 
        p.histoMgr.forHisto("Reference", signalStyle)

    p.histoMgr.setHistoDrawStyle("Target", "HIST") 
    p.histoMgr.setHistoLegendStyle("Target", "LP") #F

    p.histoMgr.setHistoDrawStyle("Reference" , "HIST") 
    p.histoMgr.setHistoLegendStyle("Reference", "F") #LP

    '''
    histoG = histograms.Histo(HT, "TT", "Signal")
    histoG.setIsDataMC(isData=False, isMC=True)
    
    histoF = histograms.Histo(HR, "QCD", "Signal")
    histoF.setIsDataMC(isData=False, isMC=True)
    '''
    #styleT = styles.ttStyle
    #styleR = styles.signalStyleHToTB1000

    #styleT.apply(HT)
    #styleR.apply(HR)

    '''
    myList.append(histoT)
    myList.append(histoR)
    '''
    

    # Save plot in all formats    
    #saveName = hT.split("/")[-1]
    #plots.drawPlot(p, saveName, **_kwargs)
    #savePath = os.path.join(opts.saveDir, "HplusMasses", hT.split("/")[0], opts.optMode)
    #plots.drawPlot(p, savePath, **_kwargs)
    #SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf", ".C"])
    dName = datasetTarg.getName()
    dName = dName.replace("ChargedHiggs_HplusTB_HplusToTB_", "")

    saveName = hT.split("/")[-1] + "_" + dName
    #print saveName, hT, opts.saveDir
    savePath = os.path.join(opts.saveDir, hT.split("/")[0], opts.optMode)
    print "TYPE", type(hT), type(savePath), type(p)
    plots.drawPlot(p, savePath, **_kwargs)

    #leg = ROOT.TLegend(0.2, 0.8, 0.81, 0.87)
    leg = ROOT.TLegend(0.2, 0.8, 0.51, 0.87)
    leg.SetFillStyle( 0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    #{"dx": -0.55, "dy": -0.55, "dh": -0.08}
    datasetName = datasetTarg.getName()
    datasetName = datasetName.replace("TT", "t#bar{t}")
    if "ChargedHiggs" in datasetName:
        datasetName = datasetName.replace("ChargedHiggs_HplusTB_HplusToTB_M_", "m_{H+} = ")
        datasetName = datasetName+"GeV"
    #leg.SetHeader("t#bar{t}")

    leg.SetHeader(datasetName)
    leg.Draw()
    
    #print savePath
    #savePath = os.path.join(opts.saveDir,  opts.optMode)

    SavePlot(p, saveName, savePath)


    return
    


def PlotMC(datasetsMgr, histo, intLumi):

    kwargs = {}
    if opts.normaliseToOne:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToOne=True, saveFormats=[], **kwargs)
    else:
        p = plots.MCPlot(datasetsMgr, histo, normalizeToLumi=intLumi, saveFormats=[], **kwargs)

    # Draw the histograms
    _cutBox = None
    _rebinX = 1
    _format = "%0.0f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}


    if "ChiSqr" in histo:
        _rebinX = 1
        logY    = True
        _units  = ""
        _format = "%0.1f " + _units
        _xlabel = "#chi^{2}"
        _cutBox = {"cutValue": 10.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 100
    elif "trijetmass" in histo.lower():
        _rebinX = 4
        logY    = False
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjb} (%s)" % _units
        _cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 805 #1005
    elif "ht" in histo.lower():
        _rebinX = 2
        logY    = False
        _units  = "GeV"
        _format = "%0.0f " + _units
        _xlabel = "H_{T} (%s)" % _units
        _cutBox = {"cutValue": 500, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        #_opts["xmin"] = 500
        _opts["xmax"] = 2000
    elif "tetrajetmass" in histo.lower():
        _rebinX = 5 #5 #10 #4
        logY    = False
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{jjbb} (%s)" % (_units)
        _format = "%0.0f " + _units
        _cutBox = {"cutValue": 500.0, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 1500 #3500.0
        #_rebinX = 10
        #_opts["xmax"] = 3500
    elif "tetrajetbjetpt" in histo.lower():
        _rebinX = 2
        logY    = False
        _units  = "GeV/c"
        _format = "%0.0f " + _units
        _xlabel = "p_{T}  (%s)" % (_units)
        _format = "%0.0f " + _units
        _opts["xmax"] = 600
    elif "foxwolframmoment" in histo.lower():
        _format = "%0.1f"
        _cutBox = {"cutValue": 0.5, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
    else:
        pass

    if logY:
        yMaxFactor = 2.0
    else:
        yMaxFactor = 1.2

    _opts["ymaxfactor"] = yMaxFactor
    if opts.normaliseToOne:
        _opts["ymin"] = 1e-3
    else:
        _opts["ymin"] = 1e0

    # Customise styling
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))

    
    if "QCD" in datasetsMgr.getAllDatasets():
        p.histoMgr.forHisto("QCD", styles.getQCDFillStyle() )
        p.histoMgr.setHistoDrawStyle("QCD", "HIST")
        p.histoMgr.setHistoLegendStyle("QCD", "F")

    if "TT" in datasetsMgr.getAllDatasets():
        p.histoMgr.setHistoDrawStyle("TT", "AP")
        p.histoMgr.setHistoLegendStyle("TT", "LP")

    # Customise style
    signalM = []
    for m in signalMass:
        signalM.append(m.rsplit("M_")[-1])
    for m in signalM:
        p.histoMgr.forHisto("ChargedHiggs_HplusTB_HplusToTB_M_%s" %m, styles.getSignalStyleHToTB_M(m))

    plots.drawPlot(p, 
                   histo,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    # Save plot in all formats    
    saveName = histo.split("/")[-1]
    savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)
    SavePlot(p, saveName, savePath) 
    return

#Fit(datasetsMgr.getAllDatasets(), folder+"/"+HistoFit[i], "gaus")
def Fit (datasets, histo, function):
    
    
    FitList = []
    for dataset in datasets:

        datasetName = dataset.getName()
        print "Dataset = ", datasetName
        hh = dataset.getDatasetRootHisto(histo)
 
        hh.normalizeToOne()
        h = hh.getHistogram()

        #h = dataset.getDatasetRootHisto(histo).getHistogram()
        xMin  = h.GetXaxis().GetXmin()
        xMax  = h.GetXaxis().GetXmax()
        yMin  = 0
        yMax  = 1.2
        #statOption = ROOT.TEfficiency.kFNormal
        if "TT" in datasetName:
            if function == "gaus":
                fitGauss = ROOT.TF1("fitGauss", "gaus", -2.5, 2.5)
#                TF1 *fitBoFreq = new TF1("fitBoFreq","[0]*x+[1]",0,20);
#                h.Fit("gaus")
                #fitTest = ROOT.TF1("fitTest", "0.01", -2.5, 2.5)
                
                h.Fit("fitGauss","SRBM")
                #h.GetListOfFunctions().Add(fitTest)
                legend = "TT"

        legend = "a legend"
        print "Legend", legend
        saveName = histo.split("/")[-1]+"_Fit"

        print saveName

        xTitle = "fixXTitle"
        yTitle = "fixYTitle"
    
        yMin = 0.
        yMax = 0.03
        xMin = -2.3
        xMax = 2.3
        kwargs = {}

        options = {"ymin": yMin  , "ymax": yMax, "xmin":xMin, "xMax":xMax}
        FitList.append(h)
        #p = plots.MCPlot(dataset, h, normalizeToLumi=0, saveFormats=[], **kwargs)

        p = plots.PlotBase(datasetRootHistos=FitList, saveFormats=kwargs.get("saveFormats"))
        p.createFrame(saveName, opts=options)
        
        p.getFrame().GetXaxis().SetTitle(xTitle)
        p.getFrame().GetYaxis().SetTitle(yTitle)
        #p.histoMgr.setHistoDrawStyle(datasetName, "AP")
        
# Set range                                                                                                                                                                          
        p.getFrame().GetXaxis().SetRangeUser(xMin, xMax)

        
        moveLegend = {"dx": -0.55, "dy": -0.01, "dh": -0.1}

        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        # Add Standard Texts to plot        
        histograms.addStandardTexts()
    
        p.draw()
    
    # Save plot in all formats                                                                                                                                                           
        savePath = os.path.join(opts.saveDir, "HplusMasses", histo.split("/")[0], opts.optMode)
        save_path = savePath 
        SavePlot(p, saveName, save_path)
    return

        

def SavePlot(plot, plotName, saveDir, saveFormats = [".C", ".png", ".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )

     # Check that path exists                                                                                                                                                                               
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # Create the name under which plot will be saved                                                                                                                                                        
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))
    saveName = saveName.replace("(", "_")
    saveName = saveName.replace(")", "")
    saveName = saveName.replace(" ", "")

    # For-loop: All save formats                                                                                                                                                                            
    for i, ext in enumerate(saveFormats):
        saveNameURL = saveName + ext
        saveNameURL = aux.convertToURL(saveNameURL, opts.url)
        Verbose(saveNameURL, i==0)
        plot.saveAs(saveName, formats=saveFormats)
    return

'''
def SavePlot(plot, saveName, saveDir, saveFormats = [".pdf"]):
    Verbose("Saving the plot in %s formats: %s" % (len(saveFormats), ", ".join(saveFormats) ) )
    
    # Check that path exists
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
        
    savePath = os.path.join(saveDir, saveName)

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats):
        saveNameURL = savePath + ext
        saveNameURL = saveNameURL.replace("/publicweb/s/skonstan/", "http://home.fnal.gov/~skonstan/")
        if opts.url:
            Print(saveNameURL, i==0)
        else:
            Print(savePath + ext, i==0)
        plot.saveAs(savePath, formats=saveFormats)
    return

'''
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
    ANALYSISNAME = "TopTaggerEfficiency"
    SEARCHMODE   = "80to1000"
    DATAERA      = "Run2016"
    OPTMODE      = ""
    BATCHMODE    = True
    PRECISION    = 3
    #SIGNALMASS   = [200, 500, 800, 2000]
    #SIGNALMASS   = [300, 500, 800, 1000]
    SIGNALMASS   = []
    #SIGNALMASS   = [200, 500, 800, 1000, 2000, 3000]
    INTLUMI      = -1.0
    SUBCOUNTERS  = False
    LATEX        = False
    MERGEEWK     = False
    URL          = False
    NOERROR      = True
    SAVEDIR      = None #"/publicweb/s/skonstan/" + ANALYSISNAME
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-m", "--mcrab", dest="mcrab", action="store", 
                      help="Path to the multicrab directory for input")

    parser.add_option("--m1", "--mcrab1", dest="mcrab1", action="store", 
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

    #parser.add_option("--signalMass", dest="signalMass", type=float, default=SIGNALMASS, 
                      #help="Mass value of signal to use [default: %s]" % SIGNALMASS)

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

    parser.add_option("-n", "--normaliseToOne", dest="normaliseToOne", action="store_true", 
                      help="Normalise the histograms to one? [default: %s]" % (NORMALISE) )

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

    # Sanity check
    if opts.mergeEWK:
        Print("Merging EWK samples into a single Datasets \"EWK\"", True)

    if opts.saveDir == None:
        opts.saveDir = aux.getSaveDirPath(opts.mcrab, prefix="", postfix="")

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plotMC_HPlusMass.py: Press any key to quit ROOT ...")

