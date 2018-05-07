#!/usr/bin/env python
'''
Description:

Usage:
./plotMC_HPlusMass.py -m <pseudo_mcrab> [opts]

Examples:
./plotMC_HPlusMass.py -m <peudo_mcrab> -o "" --url --normaliseToOne
./plotMC_HPlusMass.py -m <peudo_mcrab> --folder topologySelection_ --url --normaliseToOne
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url --signalMass 500
./plotMC_HPlusMass.py -m <peudo_mcrab> --normaliseToOne --url --signalMass 500

Last Used:
./plotMC_HPlusMass.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_InvMassFix_170822_074229/ --normaliseToOne --url --mergeEWK
./plotMC_HPlusMass.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_InvMassFix_170822_074229/ --normaliseToOne --folder ""
./plotMC_HPlusMass.py -m Hplus2tbAnalysis_StdSelections_TopCut100_AllSelections_NoTrgMatch_TopCut10_H2Cut0p5_InvMassFix_170822_074229/ --folder topSelection_ --url --normaliseToOne

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
import HiggsAnalysis.NtupleAnalysis.tools.styles_Soti as styles
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
    "analysis"         : "MyHplus2tbKInematics",
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
    

def main(opts, signalMass):

    optModes = ["OptChiSqrCutValue100"]                                                                                                                             

    if opts.optMode != None:
        optModes = [opts.optMode]

    # For-loop: All optimisation modes
    for opt in optModes:
        opts.optMode = opt

        # Setup & configure the dataset manager 
        datasetsMgr = GetDatasetsFromDir(opts)
        datasetsMgr.updateNAllEventsToPUWeighted()
        datasetsMgr.loadLuminosities() # from lumi.json
        if opts.verbose:
            datasetsMgr.PrintCrossSections()
            datasetsMgr.PrintLuminosities()

        # Set/Overwrite cross-sections
        for d in datasetsMgr.getAllDatasets():
            if "ChargedHiggs" in d.getName():
                datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)
               
        
        # Determine integrated Lumi before removing data
        #intLumi = datasetsMgr.getDataset("Data").getLuminosity()
        intLumi = 35920
        
        # Remove datasets
        if 1:
            datasetsMgr.remove(filter(lambda name: "Data" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD-b" in name, datasetsMgr.getAllDatasetNames()))
            datasetsMgr.remove(filter(lambda name: "QCD" in name, datasetsMgr.getAllDatasetNames()))
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


        # Merge EWK samples
        if opts.mergeEWK:
            datasetsMgr.merge("EWK", GetListOfEwkDatasets())
            plots._plotStyles["EWK"] = styles.getAltEWKStyle()

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

        # Print dataset information
        datasetsMgr.PrintInfo()

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(True)
        style.setGridX(True)
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
        
        folderG     = "TrijetCandidateGenuine"
        folderFake     = "TrijetCandidateFake"

        histoListG  = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folderG)
        histoListF  = datasetsMgr.getDataset(datasetOrder[0]).getDirectoryContent(folderFake)

        histoPathsG = [os.path.join(folderG, h) for h in histoListG]
        histoPathsF = [os.path.join(folderFake, h) for h in histoListF]
        '''
        hList0     = [x for x in histoList if "TrijetMass" in x]
        hList1     = [x for x in histoList if "TetrajetMass" in x]
        hList2     = [x for x in histoList if "TetrajetBjetPt" in x]
        histoPaths2 = [os.path.join(folder, h) for h in hList0+hList1+hList2]
        histoPaths = histoPaths1 + histoPaths2
        '''

        for i in range(len(histoPathsG)):
            hG = histoPathsG[i]
            hF = histoPathsF[i]
            if "Vs" in hG: # Skip TH2D
                continue
            #PlotMC(datasetsMgr, h, intLumi)
            PlotSignalBackground(datasetsMgr, hG, hF, intLumi)
            #HistoFit = ["TrijetDPtOverGenPt",]

            #for i in range(len(HistoFit)):
            #Fit(datasetsMgr.getAllDatasets(), folder+"/"+HistoFit[i], "gaus")

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



def PlotSignalBackground(datasetsMgr, hG, hF, intLumi):
    kwargs = {}
    _kwargs = {}
    #kwargs = GetHistoKwargs(hG, opts)


    if opts.normaliseToOne:
        pG = plots.MCPlot(datasetsMgr, hG, normalizeToOne=True, saveFormats=[], **_kwargs)
        pF = plots.MCPlot(datasetsMgr, hF, normalizeToOne=True, saveFormats=[], **_kwargs)
    else:
        pG = plots.MCPlot(datasetsMgr, hG, normalizeToLumi=intLumi, saveFormats=[], **_kwargs)
        pF = plots.MCPlot(datasetsMgr, hF, normalizeToLumi=intLumi, saveFormats=[], **_kwargs)

    # Draw the histograms                                                                                                                                                                
    _cutBox = None
    _rebinX = 1
    _format = "%0.2f"
    _xlabel = None
    logY    = False
    _opts   = {"ymin": 1e-3, "ymaxfactor": 1.0}



    if "mass" in hG.lower():
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "M (%s)" % _units
         
    if "trijetmass" in hG.lower():
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{top} (%s)" % _units
        #_cutBox = {"cutValue": 173.21, "fillColor": 16, "box": False, "line": True, "greaterThan": True}
        _opts["xmax"] = 805 #1005

    if "bjetmass" in hG.lower():
        _xlabel = "m_{b-tagged jet} (%s)" % _units
        _opts["xmax"] = 50
    if "bjetldgjet_mass" in hG.lower():
        _xlabel = "m_{b, ldg jet} (%s)" % _units
    if "bjetsubldgjet_mass" in hG.lower():
        _xlabel = "m_{b-tagged, subldg jet} (%s)" % _units

    if "jet_mass" in hG.lower():
        _opts["xmax"] = 750

    if "mult" in hG.lower():
        _format = "%0.0f"
        _xlabel = "Leading jet mult"
        if "subldg" in hG.lower():
            _xlabel = "Subleading jet mult"
            
    if "cvsl" in hG.lower():
        _format = "%0.0f"
        _xlabel = "Leading jet CvsL"
        if "subldg" in hG.lower():
             _xlabel = "Subleading jet CvsL"

    if "axis2" in hG.lower():
        _format = "%0.3f"
        _xlabel = "Leading jet axis2"
        if "subldg" in hG.lower():
            _xlabel = "Subleading jet axis2"

    if "dijetmass" in hG.lower():
        _units  = "GeV/c^{2}"
        _format = "%0.0f " + _units
        _xlabel = "m_{W} (%s)" % _units
        _opts["xmax"] = 600

    if "trijetptdr" in hG.lower():
        _opts["xmax"] =800
        _format = "%0.0f"
        _xlabel = "p_{T}#Delta R_{t}"

    if "dijetptdr" in hG.lower():
        _opts["xmax"] =800
        _format = "%0.0f"
        _xlabel = "p_{T}#Delta R_{W}"

    if "dgjetptd" in hG.lower():
        _format = "%0.2f"
        _xlabel = "Leading jet p_{T}D"
        if "subldg" in hG.lower():
            _xlabel = "Subleading jet p_{T}D"
    

    else:
        pass

    '''
    if "bdisc" in hG.lower():
        _format = "%0.2f"
        if "subldg" in hG.lower():
            _xlabel = "Subleading jet CSV"
        elif "ldg" in hG.lower():
            _xlabel = "Leading jet CSV"
        else:
            _xlabel = "b-tagged jet CSV"
    '''
    

    if logY:
        yMaxFactor = 2.0
    else:
        yMaxFactor = 1.2

    _opts["ymaxfactor"] = yMaxFactor
    if opts.normaliseToOne:
        _opts["ymin"] = 1e-3
    else:
        _opts["ymin"] = 1e0

    if "bdisc" in hG.lower():
        _format = "%0.2f"
        if "subldg" in hG.lower():
            _xlabel = "Subleading jet CSV"
            _opts   = {"ymin": 1e-3, "ymax": 0.06}
        elif "ldg" in hG.lower():
            _xlabel = "Leading jet CSV"
            _opts   = {"ymin": 1e-3, "ymax": 0.06}
        else:
            _xlabel = "b-tagged jet CSV"
            _opts   = {"ymin": 1e-3, "ymax": 0.35}

        
    myList = []
    # Customise styling
    pG.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))
    pF.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineStyle(ROOT.kSolid))



    '''
    plots.drawPlot(pG, 
                   hG,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    plots.drawPlot(pF, 
                   hF,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.92},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymax": 1.4},
                   cutBox       = _cutBox,
                   )

    '''


    dataset = datasetsMgr.getDataset("TT")
    
    h = dataset.getDatasetRootHisto(hG)
    h.normalizeToOne()
    HG = h.getHistogram()

    h = dataset.getDatasetRootHisto(hF)
    h.normalizeToOne()
    HF = h.getHistogram()



    p = plots.ComparisonPlot(histograms.Histo(HF,"Fake", "p", "P"), histograms.Histo(HG,"Genuine", "pl", "PL"),) 
    p.histoMgr.setHistoLegendLabelMany({"Fake": "Unmatched", "Genuine": "Truth-matched"}) 
    p.histoMgr.forHisto("Fake", styles.getAltBackgroundBDTGStyle() ) 
    p.histoMgr.setHistoDrawStyle("Fake", "LP") 
    p.histoMgr.setHistoLegendStyle("Fake", "LP") #F
    
    p.histoMgr.forHisto("Genuine", styles.getAltSignalBDTGStyle()) 
    p.histoMgr.setHistoDrawStyle("Genuine" , "HIST") 
    p.histoMgr.setHistoLegendStyle("Genuine", "LP") #LP


    #HF = dataset.getDatasetRootHisto(hF).getHistogram()
    #HG = dataset.getDatasetRootHisto(hG).getHistogram()

    histoG = histograms.Histo(HG, "TT", "Signal")
    histoG.setIsDataMC(isData=False, isMC=True)
    
    histoF = histograms.Histo(HF, "QCD", "Signal")
    histoF.setIsDataMC(isData=False, isMC=True)
   
    styleG = styles.ttStyle
    styleF = styles.signalStyleHToTB1000

    #hG = histograms.Histo(histoBkg3, legNameBkg3, "F", "HIST9" )
    #background3_histo = histograms.Histo(histoBkg3, legNameBkg3, "F", "HIST9" )

    styleG.apply(HG)
    styleF.apply(HF)

    myList.append(histoG)
    myList.append(histoF)
    

    
    #myList.append(HF)
    #myList.append(HG)
    
#    p = plots.PlotBase(datasetRootHistos=myList, saveFormats=[])
    
    _kwargs = {
        "xlabel"           : _xlabel,
        "ylabel"           : "Arbitrary Units / %s" % (_format),
        "ratioYlabel"      : "Ratio ",
        "ratio"            : False,
        "ratioInvert"      : False,
        "stackMCHistograms": False,
        "addMCUncertainty" : False,
        "addLuminosityText": False,
        "addCmsText"       : True,
        "cmsExtraText"     : "Preliminary",
        "opts"             : {"ymin": 0.0, "ymaxfactor": 1.1},
        "opts2"            : {"ymin": 0.6, "ymax": 1.5},
        "log"              : False,
        #"createLegend"     : {"x1": 0.5, "y1": 0.75, "x2": 0.9, "y2": 0.9},                                                                                                                                         
        "createLegend"     : {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.82}, 
        }

    '''
    plots.drawPlot(p, 
                   hG,  
                   xlabel       = _xlabel,
                   ylabel       = "Arbitrary Units / %s" % (_format),
                   log          = logY,
                   rebinX       = _rebinX, cmsExtraText = "Preliminary", 
                   createLegend = {"x1": 0.58, "y1": 0.65, "x2": 0.92, "y2": 0.82},
                   opts         = _opts,
                   opts2        = {"ymin": 0.6, "ymaxfactor": 1.1},
                   cutBox       = _cutBox,
                   )


    '''
    # Save plot in all formats    
    saveName = hG.split("/")[-1]
    #plots.drawPlot(p, saveName, **_kwargs)
    savePath = os.path.join(opts.saveDir, "HplusMasses", hG.split("/")[0], opts.optMode)
    plots.drawPlot(p, savePath, **_kwargs)
    SavePlot(p, saveName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png", ".pdf"])

    #SavePlot(p, saveName, savePath) 

    #p = plots.DataMCPlot2( myList, saveFormats=[])
    #p.setLuminosity(opts.intLumi)
    #p.setDefaultStyles()

    # Draw the plot and save it                                                                                                                                                          
    #hName = hG
    #plots.drawPlot(p, hName, **_kwargs)
    #SavePlot(p, hName, os.path.join(opts.saveDir, opts.optMode), saveFormats = [".png"])

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
    ANALYSISNAME = "TopRecoTree"
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
    SAVEDIR      = "/publicweb/s/skonstan/" + ANALYSISNAME
    VERBOSE      = False
    HISTOLEVEL   = "Vital" # 'Vital' , 'Informative' , 'Debug'
    NORMALISE    = False
    FOLDER       = "" #"topSelection_" #"ForDataDrivenCtrlPlots" #"topologySelection_"

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

    # Sanity check
    allowedMass = [180, 200, 220, 250, 300, 350, 400, 500, 800, 1000, 2000, 3000]
    signalMass = []
    for m in sorted(SIGNALMASS, reverse=True):
        signalMass.append("ChargedHiggs_HplusTB_HplusToTB_M_%.f" % m)

    # Call the main function
    main(opts, signalMass)

    if not opts.batchMode:
        raw_input("=== plotMC_HPlusMass.py: Press any key to quit ROOT ...")
